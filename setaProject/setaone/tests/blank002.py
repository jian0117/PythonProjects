import pandas as pd
import requests
import time
from tqdm import tqdm
import json

# ---------------------- 豆包模型核心配置（重点！全部替换为豆包信息） ----------------------
API_KEY = "6d4490f5-268a-4873-9a76-e31a3413d7e7 "  # 必须替换成自己的豆包API Key
API_URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"  # 豆包官方API地址（不是火山的）
MODEL_NAME = "doubao-seed-1-8-251228"  # 你指定的豆包模型名
RETRY_COUNT = 3  # 重试次数
TIMEOUT = 30  # 超时时间（秒）
QPS = 2  # 每秒调用次数（防止限流）


# ---------------------- 豆包模型调用函数（修复f-string冲突+优化JSON解析） ----------------------
def get_llm_multi_sentiment(comment_id, comment_text):
    # 校验评论内容是否有效
    if not comment_text or pd.isna(comment_text):
        # 返回全中性字典
        analysis_dimensions = [
            "外观设计", "气味", "持久度", "扩散力", "喷头效果",
            "便捷性", "成分", "规格分量", "除味效果", "除菌效果",
            "除螨效果", "驱虫效果", "商品包装", "品相", "安全性"
        ]
        return {dim: "中性" for dim in analysis_dimensions}

    # 定义需要分析的所有板块（与Excel字段对应）
    analysis_dimensions = [
        "外观设计", "气味", "持久度", "扩散力", "喷头效果",
        "便捷性", "成分", "规格分量", "除味效果", "除菌效果",
        "除螨效果", "驱虫效果", "商品包装", "品相", "安全性"
    ]
    dimensions_str = "、".join(analysis_dimensions)

    # 豆包适配的Prompt，修复f-string大括号冲突（用双大括号{{}}转义为普通大括号）
    prompt = f"""
    任务：分析以下评论的多个维度情感倾向，严格按照要求返回结果。
    评论ID：{comment_id}
    评论内容：{comment_text}
    分析维度：{dimensions_str}
    要求：
    1. 每个维度仅输出「正向」「逆向」「中性」其中一个标签，中性表示评论未提及该维度或无明显情感倾向；
    2. 必须以JSON格式返回，key为维度名称，value为情感标签，无任何额外文字、标点、注释；
    3. 严格遵循维度名称，不得增减、修改维度，确保JSON可直接解析。
    示例输出：
    {{
        "外观设计": "中性",
        "气味": "正向",
        "持久度": "逆向"
    }}
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,  # 固定温度，保证输出稳定
        "max_tokens": 500  # 增加token数，容纳15个维度的JSON输出
    }

    # 重试机制
    for i in range(RETRY_COUNT):
        try:
            response = requests.post(API_URL, headers=headers, json=data, timeout=TIMEOUT)
            print(f"状态码：{response.status_code} | 评论ID：{comment_id}")

            if response.status_code == 200:
                result = response.json()
                sentiment_content = result["choices"][0]["message"]["content"].strip()
                # 解析JSON结果（用标准json模块，比eval更安全，避免语法错误）
                try:
                    # 修复：用json.loads解析，兼容标准JSON格式
                    sentiment_dict = json.loads(sentiment_content)
                    # 校验维度完整性，缺失维度填充为中性
                    for dim in analysis_dimensions:
                        if dim not in sentiment_dict or sentiment_dict[dim] not in ["正向", "逆向", "中性"]:
                            sentiment_dict[dim] = "中性"
                    return sentiment_dict
                except Exception as json_e:
                    print(f"JSON解析失败（评论ID：{comment_id}）：{str(json_e)[:60]}")
                    break
            else:
                print(f"错误响应（评论ID：{comment_id}）：{response.text[:80]}")
                time.sleep(3)
        except Exception as e:
            print(f"调用失败（第{i + 1}次，评论ID：{comment_id}）：{str(e)[:60]}")
            time.sleep(3)

    # 调用失败时，返回全中性字典
    return {dim: "中性" for dim in analysis_dimensions}


# ---------------------- 批量分析主函数（适配新字段结构） ----------------------
def analyze_reviews_with_llm(input_file_path, output_file_path):
    # 读取Excel文件（openpyxl引擎支持.xlsx格式）
    df = pd.read_excel(input_file_path, engine="openpyxl")

    # 校验必要字段是否存在
    required_columns = ["评论ID", "comment_text"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Excel文件缺少必要字段：{','.join(missing_columns)}")

    # 定义所有分析维度（与Excel对应）
    analysis_dimensions = [
        "外观设计", "气味", "持久度", "扩散力", "喷头效果",
        "便捷性", "成分", "规格分量", "除味效果", "除菌效果",
        "除螨效果", "驱虫效果", "商品包装", "品相", "安全性"
    ]

    # 初始化缺失的维度列（若Excel中无对应列，创建并填充默认值）
    for dim in analysis_dimensions:
        if dim not in df.columns:
            df[dim] = "中性"

    # 批量处理每条评论
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="批量分析评论中"):
        comment_id = row["评论ID"]
        comment_text = row["comment_text"]

        # 调用模型获取多维度情感结果
        sentiment_result = get_llm_multi_sentiment(comment_id, comment_text)

        # 填充结果到DataFrame中
        for dim in analysis_dimensions:
            df.loc[idx, dim] = sentiment_result.get(dim, "中性")

        # 严格限流，避免超出API调用限制
        time.sleep(1 / QPS)

        # 每5条保存一次（防止程序中断丢失数据）
        if (idx + 1) % 5 == 0:
            df.to_excel(output_file_path, index=False, engine="openpyxl")

    # 最终保存完整结果
    df.to_excel(output_file_path, index=False, engine="openpyxl")
    print(f"\n✅ 分析完成！结果文件已保存至：{output_file_path}")
    print(f"📊 处理数据量：{len(df)} 条评论，分析维度：{len(analysis_dimensions)} 个")
    return output_file_path


# ---------------------- 执行代码 ----------------------
if __name__ == "__main__":
    input_file = "D:\\ChromeDownload\\空气清新_试标注.xlsx"
    # analyze_reviews_with_llm(input_file, "D:\\ChromeDownload\\空气清新_标注结果AI.xlsx")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    # 新增：打印请求头，验证格式
    print("生成的Authorization头：", headers["Authorization"])