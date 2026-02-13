# -*- coding:utf-8 -*-

import requests
import pandas as pd
import random
from tqdm import tqdm

cookie = 'DISTRIBUTOR-ID=1; MERCHANT-ID=1; CUSTOMER-ID=6908460; ID-TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiIxNTI2ODYyODE4NyIsImFjdCI6InB0aXA6MCIsIm5hbWUiOiLlraPlkKvlqbciLCJtb2JpbGUiOiIxNTI2ODYyODE4NyIsImlzcyI6Imh0dHBzOi8vdGVzdC1hZG1pbi55YW54dWFua2EuY29tIiwiZXhwIjoxNzQ1NjE2ODY3LCJpYXQiOjE3NDU1NTIwNjcsImFjY291bnQiOiIxNTI2ODYyODE4NyIsImVtYWlsIjoiaHpqaWhhbnRpbmdAY29ycC5uZXRlYXNlLmNvbSJ9.ZoZMtj6lwt96Nll505AezQzSAsOMpG45NMTQcUaivgc; UID=15268628187; NAME=%E5%AD%A3%E5%90%AB%E5%A9%B7; EMAIL=hzjihanting@corp.netease.com; MOBILE=15268628187; ACT=ptip:0; DEPT-ID=73'


def get_some_sku():
    url = "https://test1-admin.yanxuanka.com/tob-operation/operation-base/xhr/galaxy/xhr/sku/price/compare/searchPage"
    headers = {
        "Cookie": cookie

    }
    form_data = {
        "priceGetType": 2,
        "pageParam": {
            "page": 2,
            "pageSize": 5000
        }
    }
    return requests.post(url=url, headers=headers, json=form_data)


def get_productlist():
    url = "https://test-admin.yanxuanka.com/tob-operation/operation-base/xhr/galaxy/xhr/product/operation/list"
    headers = {
        "Cookie": cookie

    }
    form_data = {"page": 1, "pageSize": 10000, "storeHouseType": 3}
    return requests.post(url=url, headers=headers, json=form_data)


def get_daixiao_sku():
    url = "https://test.yx.mail.netease.com/ic-main-web/yanxuan-ic-frontend-base/xhr/proxySalePrice/list.json"
    headers = {
        "Cookie": cookie
    }
    querystring = {
        "csrf_token": "f657a92a9b9a4dbdb2986ece99c3a06d",
        "businessForm": "-1",
        "itemValue": "",
        "masterStatus": "-1",
        "phyCategoryId": "0",
        "manager": "",
        "priceAuditStatus": "-1",
        "page": "1",
        "size": "4000"
    }
    return requests.get(url, headers=headers, params=querystring)


def extract_sku_data_and_save_excel(response):
    if response.status_code == 200:
        data = response.json()
        all_data = []
        for item in data["data"]["result"]:
            for sku in item["skuList"]:
                all_data.append([sku["itemName"], sku["itemId"], sku["skuId"]])

        # Create a DataFrame from the collected data
        df = pd.DataFrame(all_data, columns=["商品名称", "ItemID", "SKUID"])

        # Define the save path for the Excel file
        save_directory = "D:\\test_files\\"
        file_path = save_directory + "daixiao_sku_datas.xlsx"

        # Save the DataFrame to an Excel file
        df.to_excel(file_path, index=False)
    else:
        print("Failed to retrieve data.")


def extract_sku_data_and_save_excel2(response):
    if response.status_code == 200:
        data = response.json()
        all_data = []
        for items in data["data"]["result"]:
            all_data.append([items["spuId"]])

        # Create a DataFrame from the collected data
        df = pd.DataFrame(all_data, columns=["销售SPUID"])

        # Define the save path for the Excel file
        save_directory = "D:\\ChromeDownload\\"
        file_path = save_directory + "area_forbidden_test_page2.xlsx"

        # Save the DataFrame to an Excel file
        df.to_excel(file_path, index=False)
    else:
        print("Failed to retrieve data.")


def select_and_save_random_data(filepath, n, output_filepath):
    data = pd.read_excel(filepath, header=0)  # 读取Excel文件,保留表头
    random_data = data.sample(n)  # 随机选取n行数据
    random_data.to_excel(output_filepath, index=False)  # 将随机选取的数据保存到输出文件中


def merge_and_select_random_data(file_path1, file_path2, n, output_file_path):
    data1 = pd.read_excel(file_path1, header=0)
    data2 = pd.read_excel(file_path2, header=0)
    combined_data = pd.concat([data1, data2])  # Combine the two datasets
    with tqdm(total=n, desc="Processing") as pbar:
        random_data = combined_data.sample(n)
        pbar.update(n)
    random_data.to_excel(output_file_path, index=False)


def get_compareprice_sku_and_save_excel(response, output_file_name):
    if response.status_code == 200:
        data = response.json()
        all_data = []
        for item in data["data"]["result"]:
            all_data.append([item['name'], item['saleSkuId'], 1, 'batch_input_test_gj', 1, 3])

        # 创建 DataFrame
        df = pd.DataFrame(all_data, columns=["商品名称", "销售SKUID", "比价价格平台", "比价价格链接", "价格倍数", "下次比价价格获取方式"])

        # 复制原始数据
        new_data = [row[:] for row in all_data]

        # 修改复制后的数据中的值
        for row in new_data:
            row[2] = 2  # 将第3列（索引为2）的值改为2

        # 转换新数据为 DataFrame
        new_df = pd.DataFrame(new_data, columns=["商品名称", "销售SKUID", "比价价格平台", "比价价格链接", "价格倍数", "下次比价价格获取方式"])

        # 将新数据追加到现有的 DataFrame
        df = pd.concat([df, new_df], ignore_index=True)

        # 保存 DataFrame 到 Excel 文件
        save_directory = "D:\\ChromeDownload\\"
        file_path = save_directory + output_file_name
        df.to_excel(file_path, index=False)

    else:
        print("Failed to retrieve data.")


def merge_excel_files(file_path1, file_path2, output_file_path):
    # 读取两个 Excel 文件
    df1 = pd.read_excel(file_path1)
    df2 = pd.read_excel(file_path2)

    # 合并两个 DataFrame
    merged_df = pd.concat([df1, df2], ignore_index=True)

    # 将合并后的 DataFrame 写入新的 Excel 文件
    merged_df.to_excel(output_file_path, index=False)


def rule_trans_price_excel(input_file_path, output_file_path):
    # 读取 Excel 文件
    df = pd.read_excel(input_file_path)

    # 添加两列并设置默认值为 100
    df['划线价格'] = 1000
    df['优惠/加购价'] = 100
    df = df.drop('下次比价价格获取方式', axis=1)

    # 将修改后的 DataFrame 写入新的 Excel 文件
    df.to_excel(output_file_path, index=False)


def del_any_rows(file: str, n: int):
    # 读取 Excel 文件
    df = pd.read_excel(file)

    # 随机选择要删除的行数
    rows_to_delete = random.sample(range(0, len(df)), n)

    # 删除选定的行
    df = df.drop(df.index[rows_to_delete])

    # 将修改后的数据保存回 Excel 文件
    df.to_excel(file, index=False)


def remove_skuid_in_tcList(input_file_path, tcList):
    df = pd.read_excel(input_file_path)
    # 从 DataFrame 中剔除包含在 tcList 中的 skuId 对应的行
    df = df[~df['销售SKUID'].isin(tcList)]
    # 将修改后的数据保存回 Excel 文件
    df.to_excel(input_file_path, index=False)


def keep_random_rows(file: str, n: int):
    # 读取 Excel 文件
    df = pd.read_excel(file)

    # 生成要保留的行的索引
    rows_to_keep = random.sample(range(0, len(df)), n)

    # 保留选定的行，删除其他行
    df = df.iloc[rows_to_keep]

    # 覆盖源文件，只保留选定的行
    df.to_excel(file, index=False)


def deduplicate_file(filepath):
    try:
        if filepath.endswith('.xls'):
            engine = 'xlrd'
        elif filepath.endswith('.xlsx'):
            engine = 'openpyxl'
        else:
            raise ValueError("不支持的文件格式，请使用 .xls 或 .xlsx 文件。")

        # 明确指定 '销售SPUID' 列的数据类型为字符串
        df = pd.read_excel(filepath, engine=engine, dtype={'销售SPUID': str})

        # 去重
        df = df.drop_duplicates()

        # 排序
        df = df.sort_values(by="销售SPUID")

        # 保存修改后的数据到原文件
        df.to_excel(filepath, index=False)

        print("文件数据去重完成。")
    except FileNotFoundError:
        print(f"错误：未找到文件 {filepath}。")
    except Exception as e:
        print(f"发生未知错误：{e}")


import pandas as pd
import sys
from pathlib import Path


def clean_invalid_rows(input_file, output_file=None):
    """
    从Excel文件中删除校验失败原因列有数据的行

    参数:
        input_file (str): 输入Excel文件路径
        output_file (str): 输出Excel文件路径，默认为在原文件名后添加"_cleaned"
    """
    try:
        # 读取Excel文件
        df = pd.read_excel(input_file)

        # 检查是否存在所需的列
        required_columns = ['校验失败原因']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"文件中缺少以下列: {', '.join(missing_columns)}")

        # 获取原始行数
        original_rows = len(df)

        # 删除校验失败原因列有数据的行
        df_cleaned = df[df['校验失败原因'].isna()]

        # 计算删除的行数
        deleted_rows = original_rows - len(df_cleaned)

        # 如果未指定输出文件名，使用默认格式
        if not output_file:
            file_path = Path(input_file)
            output_file = str(file_path.parent / f"{file_path.stem}_cleaned{file_path.suffix}")

        # 保存清理后的文件
        df_cleaned.to_excel(output_file, index=False)

        print(f"处理完成！")
        print(f"原始数据行数: {original_rows}")
        print(f"已删除行数: {deleted_rows}")
        print(f"清理后数据行数: {len(df_cleaned)}")
        print(f"结果已保存至: {output_file}")

        return output_file

    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")
        return None


def filter_promise_orders(promise_orders: list, target_sku_id: int) -> list:
    # 1. status 枚举映射（数字 → 汉字，与原枚举一致）
    STATUS_MAPPING = {
        -1: "无状态",
        0: "未付款",
        1: "已付款，待发货",
        2: "支付前取消",
        3: "付款后取消",
        4: "取消待确认",
        5: "已发货",
        6: "发货失败"
    }

    # 2. set 存结果实现去重（用 (promiseId, promiseStatus) 作为唯一标识，避免重复）
    unique_results = set()

    try:
        # 3. 遍历每个 promiseOrder 检查匹配
        for order in promise_orders:
            if not isinstance(order, dict):
                print(f"跳过无效数据（非字典）：{order}")
                continue

            # 获取当前订单的 promiseItems 列表
            promise_items = order.get("promiseItems", [])
            if not promise_items:
                continue

            # 4. 匹配 int 型 skuId（将 saleSkuId 转为整数，失败则跳过该 item）
            is_match = False
            for item in promise_items:
                item_sku_str = item.get("saleSkuId", "")  # 先拿到字符串格式的 saleSkuId
                try:
                    # 关键：将 saleSkuId 转为整数（适配 target_sku_id 的 int 类型）
                    item_sku_int = int(item_sku_str)
                except (ValueError, TypeError):
                    # 若 saleSkuId 无法转整数（如空字符串、字母），跳过该 item
                    print(f"跳过无效 saleSkuId（无法转整数）：{item_sku_str}")
                    continue

                # 整数对比：匹配目标 skuId
                if item_sku_int == target_sku_id:
                    is_match = True
                    break

            # 5. 匹配成功：提取字段并整理结果
            if is_match:
                promise_id = order.get("id")
                if not promise_id:
                    print("跳过无 promiseId 的匹配订单")
                    continue

                # 获取原始数字状态（promiseStatus）和汉字状态
                promise_status = order.get("status", -1)  # 原始数字状态，新增字段
                status_text = STATUS_MAPPING.get(promise_status, f"未知状态（{promise_status}）")

                # 存入 set 去重（用 (promiseId, promiseStatus) 确保唯一性）
                unique_results.add((promise_id, promise_status, status_text))

        # 6. 转换为最终格式：新增 promiseStatus 字段
        return [
            {
                "promiseId": pid,
                "promiseType": p_status,
                "promiseStatus": st_text  # 汉字状态
            }
            for pid, p_status, st_text in unique_results
        ]

    except Exception as e:
        print(f"筛选 promiseOrders 时出错：{str(e)}")
        return []





if __name__ == '__main__':
    """# extract_sku_data_and_save_excel(get_daixiao_sku())
    source_file1 = 'D:\\test_files\\selfrun_sku_datas.xlsx'
    source_file2 = 'D:\\test_files\\daixiao_sku_datas.xlsx'
    n = 300
    output_file = 'D:\\test_files\\selfrun_sku_datas' + str(n) + '.xlsx'
    # merge_and_select_random_data(source_file1, source_file2, n, output_file)
    select_and_save_random_data(filepath=source_file1, n=n, output_filepath=output_file)"""
    f = 'D:\\ChromeDownload\\导出全部商品列表_20250430105717.xlsx'
    # extract_sku_data_and_save_excel2(get_productlist())
    # print(len('第五人格真理之下漆黑的彷徨者先知和黯独占限定纪念卡装配测试用'))

    f1 = 'D:\\ChromeDownload\\特批申请sku导入测试6--自由测试.xlsx'
    f2 = 'D:\\ChromeDownload\\失败下载结果 (38).xlsx'
    f3 = 'D:\\ChromeDownload\\矫正结果（38）.xlsx'

    # clean_invalid_rows(f1, f2)
    # clean_invalid_rows(f2, f3)

    import json
    from datetime import datetime, timedelta

    current_time = datetime.now()
    now_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    one_hour_later = (current_time + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    two_hour_later = (current_time + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
    three_hour_later = (current_time + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
    four_hour_later = (current_time + timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S")


    # 妥投物流轨迹
    route_delivery_success = [
        {
            "time": str(now_time),
            "address": "杭州市",
            "remark": "已揽收",
            "opcode": "50",
            "reasonCode": None,
            "reasonName": None
        }, {
            "time": str(one_hour_later),
            "address": "杭州市",
            "remark": "已到达分拣中心",
            "opcode": "30",
            "reasonCode": None,
            "reasonName": None
        }, {
            "time": str(two_hour_later),
            "address": "杭州市",
            "remark": "派送中",
            "opcode": "634",
            "reasonCode": None,
            "reasonName": None
        }, {
            "time": str(three_hour_later),
            "address": "杭州市",
            "remark": "已签收",
            "opcode": "80",
            "reasonCode": None,
            "reasonName": None
        }
    ]

    # 拒收并退回的物流轨迹，若有需要，自取
    route_reject_and_return = [
        {
            "time": str(now_time),
            "address": "杭州市",
            "remark": "已揽收",
            "opcode": "50",
            "reasonCode": None,
            "reasonName": None
        }, {
            "time": str(one_hour_later),
            "address": "杭州市",
            "remark": "已到达分拣中心",
            "opcode": "30",
            "reasonCode": None,
            "reasonName": None
        }, {
            "time": str(two_hour_later),
            "address": "杭州市",
            "remark": "派送中",
            "opcode": "634",
            "reasonCode": None,
            "reasonName": None
        }, {
            "time": str(three_hour_later),
            "address": "杭州市",
            "remark": "拒收",
            "opcode": "658",
            "reasonCode": None,
            "reasonName": None
        }, {
            "time": str(four_hour_later),
            "address": "杭州市",
            "remark": "退回ing",
            "opcode": "99",
            "reasonCode": None,
            "reasonName": None
        }
    ]

    print(json.dumps(route_delivery_success))