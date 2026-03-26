import pandas as pd
import os
import json


def remove_matched_skus(a_file_path, b_file_path, output_file_path, sku_column='SKUID'):
    """
    从文件A中提取目标SKU列表，在文件B中删除所有匹配该列表的行，并将过滤后的文件B保存

    参数:
        a_file_path: str, 存储待匹配SKU的文件路径（需包含sku_column列）
        b_file_path: str, 需要过滤的源文件路径
        output_file_path: str, 过滤后文件的保存路径
        sku_column: str, SKU编号所在列的列名，默认值为'SKUID'（需确保A、B文件中列名一致）
    """
    try:
        # 读取文件A，仅保留SKU列（减少内存占用）
        # usecols=[sku_column] 表示只读取指定的SKU列
        df_a = pd.read_excel(a_file_path, usecols=[sku_column])

        # 提取SKU列中非空的唯一值，转换为列表（去重避免重复匹配）
        # dropna() 排除空值，unique() 去重，tolist() 转换为Python列表
        sku_list = df_a[sku_column].dropna().unique().tolist()

        # 读取文件B的全部内容
        df_b = pd.read_excel(b_file_path)

        # 检查文件B是否包含指定的SKU列，避免后续索引报错
        if sku_column not in df_b.columns:
            raise ValueError(f"文件 {b_file_path} 中不存在列 {sku_column}，请检查列名是否正确")

        # 记录过滤前的总行数，用于统计删除数量
        original_count = len(df_b)

        # 核心过滤逻辑：保留SKU不在sku_list中的行
        # ~ 表示取反，isin(sku_list) 检查每行SKU是否在目标列表中
        # df_b[...] - 使用布尔索引过滤数据框
        df_b_filtered = df_b[~df_b[sku_column].isin(sku_list)]

        # 计算删除的行数（原始行数 - 过滤后行数）
        removed_count = original_count - len(df_b_filtered)

        # 保存过滤后的文件，index=False 表示不保留DataFrame的索引列
        df_b_filtered.to_excel(output_file_path, index=False)

        # 输出处理结果，方便用户确认
        print(f"处理完成！共删除 {removed_count} 行匹配的数据")
        print(f"处理后的文件已保存至: {output_file_path}")

    except Exception as e:
        # 捕获并显示所有异常（如文件不存在、格式错误等）
        print(f"处理过程中发生错误: {str(e)}")


def filter_excel_by_base_discount(input_file, base_discount=0.85, output_file=None):
    """
    根据价格折扣条件筛选Excel数据，保留符合"基准价×自定义折扣 ≤ 普通快递P3价×0.95"的数据

    适用场景：通常用于价格规则校验，例如筛选满足折扣条件的商品

    参数:
        input_file: str, 输入Excel文件的完整路径
        base_discount: float, 基准价的折扣系数（默认0.85，即85折），可根据需求调整
        output_file: str, 筛选结果的保存路径，若为None则自动生成（在原文件名后添加后缀）

    返回:
        pandas.DataFrame: 筛选后的数据集（便于后续二次处理）
    """
    try:
        # 读取Excel文件，dtype=str 先按字符串类型加载所有列（避免数字格式自动转换导致问题）
        df = pd.read_excel(input_file, dtype=str)
        print(f"成功读取文件，共 {len(df)} 行数据")

        # 定义必须存在的列（用于校验文件格式是否正确）
        required_columns = ['基准价', '普通快递P3价', 'SPUID', '销售SKUID', '商品类型', '销售状态']
        # 检查缺失的列
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Excel文件缺少必要的表头: {', '.join(missing_columns)}，请检查文件格式")

        # 处理特殊符号表示的空值（例如用"/"表示无数据），统一转换为pandas的空值标记pd.NA
        df['基准价'] = df['基准价'].replace('/', pd.NA)
        df['普通快递P3价'] = df['普通快递P3价'].replace('/', pd.NA)

        # 将价格列转换为数值类型（便于计算），errors='coerce' 表示无法转换的值设为pd.NA
        df['基准价_数字'] = pd.to_numeric(df['基准价'], errors='coerce')
        df['普通快递P3价_数字'] = pd.to_numeric(df['普通快递P3价'], errors='coerce')

        # 统计价格无效的行数（空值或无法转换为数字的数据）
        invalid_rows = df[
            df['基准价_数字'].isna() | df['普通快递P3价_数字'].isna()
            ].shape[0]
        if invalid_rows > 0:
            print(f"警告：有 {invalid_rows} 行数据的价格无效（含/、非数字等），已自动排除这些行")

        # 核心筛选条件：基准价×自定义折扣 ≤ 普通快递P3价×0.95（P3价系数固定为0.95）
        p3_fixed_discount = 0.95  # P3价的固定折扣系数（业务规则）
        filtered_df = df[
            (df['基准价_数字'] * base_discount) <= (df['普通快递P3价_数字'] * p3_fixed_discount)
            ]

        # 准备输出列：只保留业务需要的核心字段
        result_df = filtered_df[['SPUID', '销售SKUID', '商品类型', '销售状态', '基准价', '普通快递P3价']]

        # 新增计算列：显示双方折扣后的具体数值，方便人工核对是否符合条件
        result_df[f'基准价*{base_discount}'] = filtered_df['基准价_数字'] * base_discount
        result_df[f'普通快递P3价*0.95（固定）'] = filtered_df['普通快递P3价_数字'] * p3_fixed_discount

        # 自动生成输出路径（若未指定）：在原文件名后添加折扣参数标识
        if output_file is None:
            file_name, file_ext = os.path.splitext(input_file)  # 分离文件名和扩展名
            output_file = f"{file_name}_baseDiscount_{base_discount}_p3Fixed_0.95{file_ext}"

        # 保存结果，index=False 不保留索引
        result_df.to_excel(output_file, index=False)
        print(
            f"筛选完成，共找到 {len(result_df)} 条符合条件的数据（基准价×{base_discount} ≤ P3价×0.95），已保存到：\n{output_file}")

        return result_df  # 返回筛选后的DataFrame，支持后续处理

    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")
        return None  # 出错时返回None


def fill_tag_value(input_file, output_file):
    """
    为Excel文件中SKUID非空的行自动填充标签值（默认填充"中"）

    逻辑：遍历每行，若SKUID有有效值（非空且非空字符串），则检查标签值：
         - 若标签值为空或不合法（不在['是','否']中），则填充为"中"
         - 若标签值已合法，则不修改

    参数:
        input_file: str, 输入Excel文件路径
        output_file: str, 填充后文件的保存路径
    """
    # 读取Excel文件（默认第一行为表头）
    df = pd.read_excel(input_file)

    # 清洗表头：去除列名中可能存在的空格（避免因空格导致列名匹配失败）
    df.columns = df.columns.str.strip()

    # 遍历每行数据（index为行索引，row为行数据）
    for index, row in df.iterrows():
        # 检查SKUID是否有效：非空且不是空字符串（strip()去除首尾空格后判断）
        if pd.notna(row['SKUID']) and str(row['SKUID']).strip() != '':
            # 检查标签值是否为空或不合法（合法值为"是"或"否"）
            if pd.isna(row['标签值']) or row['标签值'] not in ['是', '否']:
                # 填充标签值为"中"（如需修改默认值，可在此处调整）
                df.at[index, '标签值'] = '中'

    # 保存处理后的文件，保留原结构（index=False不保留索引）
    df.to_excel(output_file, index=False)
    print(f"标签值填充完成，已保存至：{output_file}")


def random_sample_xlsx(input_path, output_path, n):
    """
    从Excel文件中随机抽取n行数据（保留表头），用于数据抽样或测试

    参数:
        input_path: str, 输入Excel文件路径
        output_path: str, 抽样结果的保存路径
        n: int, 需抽取的行数（必须为正整数，且不超过文件总行数）
    """
    # 读取Excel文件（默认第一行为表头，读取所有数据）
    df = pd.read_excel(input_path)

    # 校验输入参数n的有效性
    if n <= 0:
        raise ValueError("n必须是正整数（例如n=100表示抽取100行）")
    if n > len(df):
        raise ValueError(f"数据行数不足：文件仅包含{len(df)}行，无法抽取{n}行（n不能超过文件总行数）")

    # 随机抽样n行（默认不重复抽样），sample()方法是pandas的随机抽样函数
    sampled_df = df.sample(n=n)

    # 保存抽样结果，index=False表示不保留原数据的索引列
    sampled_df.to_excel(output_path, index=False)
    print(f"随机抽样完成：成功抽取{n}行数据，已保存至：{output_path}")


def fill_excel_column(
    input_file,
    output_file,
    target_column,
    fill_value,
    overwrite_existing=False
):
    """
    统计Excel文件行数，并按列名填充指定数据（支持选择是否覆盖非空单元格）

    参数:
        input_file: str, 输入Excel文件路径
        output_file: str, 处理后文件的保存路径
        target_column: str, 需要填充数据的目标列名（区分大小写）
        fill_value: 填充的值（支持字符串、数字、布尔值等，根据列类型适配）
        overwrite_existing: bool, 是否覆盖已有的非空值
                            - True: 无论单元格是否有值，都填充为fill_value
                            - False: 只填充空值单元格，非空值保持不变（默认）
    """
    try:
        # 读取Excel文件（保留所有列和数据）
        df = pd.read_excel(input_file)
        total_rows = len(df)  # 统计总行数（不含表头，仅数据行）
        print(f"文件 '{os.path.basename(input_file)}' 共包含 {total_rows} 行数据（不含表头）")

        # 检查目标列是否存在
        if target_column not in df.columns:
            raise ValueError(f"目标列 '{target_column}' 不存在于文件中，请检查列名是否正确")

        # 记录填充前的空值数量（用于结果统计）
        initial_empty = df[target_column].isna().sum()

        # 根据是否覆盖的选项执行填充
        if overwrite_existing:
            # 覆盖模式：所有单元格都填充为目标值
            df[target_column] = fill_value
            filled_count = total_rows  # 覆盖模式下，填充行数等于总行数
        else:
            # 非覆盖模式：只填充空值单元格（使用fillna，不改变已有值）
            df[target_column] = df[target_column].fillna(fill_value)
            filled_count = initial_empty  # 非覆盖模式下，填充行数等于初始空值数

        # 保存处理后的文件
        df.to_excel(output_file, index=False)
        print(f"填充完成！共填充 {filled_count} 个单元格（目标列：'{target_column}'，填充值：{fill_value}）")
        print(f"处理后的文件已保存至：{output_file}")

    except Exception as e:
        print(f"处理失败：{str(e)}")


def excel_column_deduplicate(excel_path, target_column):
    # 读取Excel文件
    df = pd.read_excel(excel_path)

    # 检查指定列是否存在
    if target_column not in df.columns:
        raise ValueError(f"Excel中不存在列名：{target_column}")

    # 按指定列去重，保留重复数据的第一行
    df_deduplicated = df.drop_duplicates(subset=[target_column], keep='first')

    # 先删除原文件（避免覆盖失败）
    if os.path.exists(excel_path):
        os.remove(excel_path)

    # 保存去重后的数据到原文件
    df_deduplicated.to_excel(excel_path, index=False)
    print(f"已完成去重！文件已保存至：{excel_path}")


import pandas as pd


def export_duplicate_rows(excel_path: str, target_column: str, output_path: str):
    """
    导入Excel文件，按指定列查询重复数据，导出所有重复行到新Excel，返回输出文件路径
    :param excel_path: 源Excel文件的路径（如"D:/data/input.xlsx"）
    :param target_column: 要检查重复的列名（如"Id"）
    :param output_path: 输出重复行的Excel路径，默认"duplicate_rows.xlsx"
    :return: 成功返回输出文件路径，失败返回None
    """
    try:
        # 1. 读取Excel文件
        df = pd.read_excel(excel_path, engine="openpyxl")

        # 2. 检查指定列是否存在
        if target_column not in df.columns:
            raise ValueError(f"Excel中不存在列名：{target_column}")

        # 3. 筛选出重复的行（keep=False表示标记所有重复行，包含每一条重复数据）
        duplicate_mask = df.duplicated(subset=target_column, keep=False)
        duplicate_df = df[duplicate_mask]

        # 4. 导出重复行到新Excel并返回文件路径
        if duplicate_df.empty:
            print("指定列中无重复数据")
            return None
        else:
            duplicate_df.to_excel(output_path, index=False, engine="openpyxl")
            print(f"重复行已导出！共导出{len(duplicate_df)}行重复数据")
            # 仅返回输出文件路径（符合你的要求）
            return output_path

    except FileNotFoundError:
        print(f"错误：未找到文件 {excel_path}")
        return None
    except Exception as e:
        print(f"处理失败：{str(e)}")
        return None


import pandas as pd


def delete_rows_by_column_value(excel_input_path, excel_output_path, target_column, delete_values):
    """
    功能：删除Excel中指定列名下含指定值的行
    参数说明：
    - excel_input_path：输入Excel文件的完整地址（如D:/data/原始文件.xlsx）
    - excel_output_path：输出新Excel文件的完整地址（如D:/data/处理后文件.xlsx）
    - target_column：指定列名（如"状态"、"姓名"，需与Excel中列名完全一致）
    - delete_values：要删除的指定值（可单个值或多个值，如"无效"、["无效", "已过期"]）
    """
    # 读取Excel文件
    df = pd.read_excel(excel_input_path)

    # 验证指定列是否存在
    if target_column not in df.columns.tolist():
        raise ValueError(f"Excel中不存在列名：{target_column}，请检查列名是否正确")

    # 转换为列表（统一处理单个/多个值）
    delete_values = [delete_values] if not isinstance(delete_values, list) else delete_values

    # 删除指定值的行（保留不等于指定值的行）
    df_filtered = df[~df[target_column].isin(delete_values)].reset_index(drop=True)

    # 输出新Excel文件（不保留索引）
    df_filtered.to_excel(excel_output_path, index=False)
    print(f"处理完成！新文件已保存至：{excel_output_path}")
    print(f"共删除 {len(df) - len(df_filtered)} 行数据，剩余 {len(df_filtered)} 行数据")


def remove_duplicate_fields(file_path, output_path):
    """
    处理json_match格式的断言行：
    1. 按字段名去重（保留首次出现，删除后续重复）
    2. 时间相关字段的值自动替换为>0（如updateTime/payTime/createTime等）
    :param file_path: 原始数据文件路径（每行一条断言）
    :param output_path: 处理后保存的文件路径
    """
    # 存储已出现的字段名（去重关键）
    field_set = set()
    # 存储处理后的结果行
    result_lines = []
    # 定义时间相关字段的关键词（可根据需要扩展）
    time_field_keywords = ['Time', 'time', 'Date', 'date']  # 匹配updateTime/payTime/createTime等

    # 读取原始文件
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        # 去除行首尾的空格/换行符，空行直接跳过
        line_stripped = line.strip()
        if not line_stripped:
            continue

        # 步骤1：拆分出「字段名」和「值」（核心逻辑）
        parts = line_stripped.split(':', 2)  # 只拆前2个冒号，避免值里有冒号
        if len(parts) < 3:
            # 格式异常的行，直接保留
            result_lines.append(line)
            continue

        # 提取核心字段名和值
        field_name = parts[1].strip()
        field_value = parts[2].strip()

        # 步骤2：判断是否为时间相关字段，若是则替换值为>0
        is_time_field = any(keyword in field_name for keyword in time_field_keywords)
        if is_time_field:
            # 替换时间字段的值为>0
            processed_line = f"{parts[0].strip()}:{field_name}:>0\n"
        else:
            # 非时间字段，保留原始值
            processed_line = line

        # 步骤3：去重逻辑（保留首次出现的字段）
        if field_name not in field_set:
            field_set.add(field_name)  # 记录该字段已出现
            result_lines.append(processed_line)
        # 字段已存在 → 跳过（删除后续重复行）

    # 步骤4：将处理后的内容写入新文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(result_lines)

    # 修正统计逻辑（原统计公式有错误）
    original_valid_lines = len([l for l in lines if l.strip()])  # 原始有效行（排除空行）
    processed_valid_lines = len(result_lines)
    duplicate_count = original_valid_lines - processed_valid_lines

    print(f"处理完成！")
    print(f"原始有效断言数：{original_valid_lines}")
    print(f"处理后断言数：{processed_valid_lines}")
    print(f"去重删除的断言数：{duplicate_count}")
    print(f"结果已保存至：{output_path}")


import json

# ===================== 核心配置 =====================
# 每批条数（你要499）
BATCH_SIZE = 499
# 输出文件路径
OUTPUT_PATH = r"D:\ChromeDownload\校验数据"


# ====================================================

def json_to_match_lines(obj, prefix=""):
    """递归把JSON转换成 json_match:路径:值 格式"""
    lines = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_prefix = f"{prefix}.{k}" if prefix else k
            lines.extend(json_to_match_lines(v, new_prefix))
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            new_prefix = f"{prefix}[{idx}]"
            lines.extend(json_to_match_lines(item, new_prefix))
    else:
        val = "not null" if obj is not None else "null"
        lines.append(f"json_match:{prefix}:{val}")
    return lines


def main():
    print("请粘贴你的【原始完整JSON】，粘贴完按回车：")
    json_str = input().strip()

    # 解析JSON
    data = json.loads(json_str)

    # 转换格式
    lines = json_to_match_lines(data)

    # 分批并写入文件
    total = len(lines)
    batch_num = 1
    for i in range(0, total, BATCH_SIZE):
        batch = lines[i:i + BATCH_SIZE]
        file_name = f"{OUTPUT_PATH}_{batch_num}.txt"

        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(batch))

        print(f"✅ 已生成：{file_name} （{len(batch)}条）")
        batch_num += 1

    print(f"\n🎉 全部完成！共生成 {batch_num - 1} 个文件")
    print(f"📂 路径：D:\\ChromeDownload\\")


if __name__ == "__main__":
    main()





# 函数使用示例（当脚本直接运行时执行）
if __name__ == "__main__":
    # 示例1：从指定Excel中随机抽取5000行并保存
    input_excel = "D:\\ChromeDownload\\清洗数据20260306.txt"
    output_excel = "D:\\ChromeDownload\\清洗完成数据20260306.txt"


    # 断言数据清洗
    # remove_duplicate_fields(input_excel, output_excel)

    # 数据清洗
    # delete_rows_by_column_value(input_excel, output_excel, "选品状态", "已禁用")

    # 查询重复行
    # export_duplicate_rows(input_excel, '履约单号', output_excel)

    # 指定列去重文件，原文件修改
    # excel_column_deduplicate(input_excel, "销售SPUID")

    # 随机筛选出n行数据
    # random_sample_xlsx(input_excel, output_excel, 3000)

    # 示例2：按基准价折扣筛选数据（如需使用，取消注释并修改参数）
    # filter_excel_by_base_discount(
    #     input_file="待筛选文件.xlsx",
    #     base_discount=0.9,  # 自定义基准价折扣为9折
    #     output_file="筛选结果.xlsx"
    # )

    # 提取a的skuId，在b中删除这些skuId的行
    # remove_matched_skus(
    #   a_file_path="D:\\ChromeDownload\\智能选品执行结果SKU导出表_20251021175026.xlsx",
    #   b_file_path="D:\\ChromeDownload\\sku批量打标模板批量600.xlsx",
    #    output_file_path="D:\\ChromeDownload\\过滤后的B文件.xlsx",
    #    sku_column="SKUID"
    # )

    # fill_tag_value(
    #     input_file="输入文件.xlsx",
    #     output_file="填充标签后的文件.xlsx"
    # )

    # 批量填充数据
    # fill_excel_column(input_file=input_excel, output_file=output_excel, target_column="标签值", fill_value="0", overwrite_existing=True)