import pandas as pd
import requests


def store_excel_file():
    test_data = {
        "name": ["A", "B"],
        "age": [18, 22]
    }

    output_excel_path = 'D:\\ChromeDownload\\test.xlsx'

    # 转为pandas的表格对象
    df = pd.DataFrame(test_data)
    # 保存为excel文件
    try:
        df.to_excel(output_excel_path, index=False)
        print(f"Excel file saved successfully at {output_excel_path}")
    except Exception as e:
        print(f"Error saving Excel file: {e}")


def read_excel_file(read_file_path, read_column):
    df_a = pd.read_excel(read_file_path, sheet_name=0, header=0, usecols=[read_column], engine='openpyxl')
    sku_list = df_a[read_column].dropna().unique().toList()


def remover_practice(a_file_path, b_file_path, ouput_file_path, sku_column='SKUID'):
    df_a = pd.read_excel(a_file_path, usecols=[sku_column], engine='openpyxl')
    sku_list = df_a[sku_column].dropna().unique().tolist()
    df_b = pd.read_excel(b_file_path, engine='openpyxl')
    if sku_column not in df_b.columns:
        raise ValueError(f"file Error :{b_file_path}")
    origin_count = len(df_b)
    df_b_flitter = df_b[~df_b[sku_column].isin(sku_list)]
    remove_count = origin_count - len(df_b_flitter)
    df_b_flitter.to_excel(ouput_file_path, index= False)
    print(f"处理完成！共删除 {remove_count} 行匹配的数据")


def remove_matched_skus(a_file_path, b_file_path, output_file_path, sku_column='SKUID'):

    try:
        df_a = pd.read_excel(a_file_path, usecols=[sku_column])
        sku_list = df_a[sku_column].dropna().unique().tolist()
        df_b = pd.read_excel(b_file_path)
        if sku_column not in df_b.columns:
            raise ValueError(f"文件 {b_file_path} 中不存在列 {sku_column}，请检查列名是否正确")
        original_count = len(df_b)

        # 核心过滤逻辑：保留SKU不在sku_list中的行
        # ~ 表示取反，isin(sku_list) 检查每行SKU是否在目标列表中
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


def get_method(url, headers, params):
    try:
        response = requests.get(url=url, headers=headers, params=params, timeout=30)
        return response
    except requests.exceptions.RequestException as e:
        print(f"error: {e}")

def post_method(url, headers, payload):
    try:
        response = requests.post(urdl=url, headers=headers, json=payload, timeout=60)
        return response
    except requests.exceptions.RequestException as e:
        print(f'error:{e}')

if __name__ == '__main__':
    test_file = 'D:\\ChromeDownload\\test.xlsx'
    read_excel_file(test_file, 'name')
