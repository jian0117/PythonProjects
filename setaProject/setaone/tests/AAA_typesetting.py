import requests
import json
import pandas as pd
import datetime
import uuid
import random
import string

pd.set_option('display.max_rows', None)


def test1111():
    url = 'https://test1-admin.yanxuanka.com/tob-operation/operation-base/xhr/galaxy/xhr/sku/price/compare/searchPage'
    cookie = 'ACT=ptip:0; EMAIL=; UID=18767168867; MOBILE=18767168867; CUSTOMER-ID=6908460; ID-TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiIxODc2NzE2ODg2NyIsImFjdCI6InB0aXA6MCIsIm5hbWUiOiLliJjnhafmrKMiLCJtb2JpbGUiOiIxODc2NzE2ODg2NyIsImlzcyI6Imh0dHBzOi8vdGVzdC1hZG1pbi55YW54dWFua2EuY29tIiwiZXhwIjoxNzMwNDkwMzAxLCJpYXQiOjE3MzA0MjU1MDEsImFjY291bnQiOiIxODc2NzE2ODg2NyIsImVtYWlsIjoiIn0.suR1oE6wwvWlcS7EVeYEvT1FtTgSetk8QenHD7Lhl6A; NAME=%E5%88%98%E7%85%A7%E6%AC%A3; DISTRIBUTOR-ID=1; DEPT-ID=73;'
    headers = {'cookie': cookie}
    payload = {"pageParam": {"page": 1, "pageSize": 1000}}
    response = requests.post(url=url, headers=headers, json=payload)
    res_j = response.json()
    sale_sku_ids = [item["saleSkuId"] for item in res_j['data']['result']]
    price_l = list()
    for _ in range(len(sale_sku_ids)):
        price_l.append(_)
    df = pd.DataFrame({"SaleSkuId": sale_sku_ids, "price": 100})
    df.to_excel("D:\\ChromeDownload\\output3.xlsx", index=False)
    a = [4000001409, 4000002050, 4000007034, 4000006446, 4000007071, 4000002061]


def count1113(filepath):
    df = pd.read_excel(filepath)
    set0 = set()
    for index, row in df.iterrows():
        supply_skuid = row['供应SKUID']
        set0.add(supply_skuid)
    print(len(set0))


def find_duplicates(filepath, column_name):
    df = pd.read_excel(filepath)
    duplicate_rows = df[df.duplicated(subset=[column_name], keep=False)][column_name]
    return duplicate_rows


def process_excel_data(file_path, output_file):
    # 读取Excel文件
    df = pd.read_excel(file_path)

    output = []
    for index, row in df.iterrows():
        supply_sku_id = str(row['供应SKUID'])
        jd_support = 1 if row['是否支持京东发货'] == '是' else 2
        jd_extra_cost = 0 if pd.isna(row['京东额外发货成本(元)']) or row['京东额外发货成本(元)'] == '/' else row[
            '京东额外发货成本(元)']
        sf_support = 1 if row['是否支持顺丰发货'] == '是' else 2
        sf_extra_cost = 0 if pd.isna(row['顺丰额外发货成本(元)']) or row['顺丰额外发货成本(元)'] == '/' else row[
            '顺丰额外发货成本(元)']

        output.append({
            "supplySkuId": supply_sku_id,
            "carrierType": 1,
            "supportType": jd_support,
            "extraCostPrice": jd_extra_cost
        })

        output.append({
            "supplySkuId": supply_sku_id,
            "carrierType": 2,
            "supportType": sf_support,
            "extraCostPrice": sf_extra_cost
        })

    json_data = json.dumps(output, indent=2, ensure_ascii=False)

    # 将结果保存到文件
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(json_data)
    print('success')


def fun11151447():
    file_path = r'D:\PythonProjects\setaProject\setaone\tests\test_files\json_data20241115.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        data_dict = json.load(f)
    result = data_dict['data']['result']
    online_merchant_info = list()
    for li in result:
        if li['status'] == 7:
            online_merchant_info.append(li)
    print(online_merchant_info)


def datetime11():
    current_date = datetime.datetime.today()
    formatted_date = current_date.strftime('%Y%m%d%H%M')
    goods_name = 'supplySku' + formatted_date
    print(goods_name)


def ranBarCode():
    print(uuid.uuid4().hex[:12])


def find_different_keys(json1, json2):
    keys_set1 = set(json1.keys())
    keys_set2 = set(json2.keys())

    different_keys1 = keys_set1 - keys_set2
    different_keys2 = keys_set2 - keys_set1

    print(different_keys1.union(different_keys2))


def calc_dict():
    with open('D:/PythonProjects/setaProject/setaone/tests/test_files/supply_info.json', 'r', encoding='utf-8') as f:
        supply_info = json.load(f)
    supply_sku_id = supply_info['data']['skuId']
    supply_sku_price = supply_info['data']['supplyPrice']
    supply_sku_delivery_area = supply_info['data']['deliverySourceArea']
    supply_inventory = supply_info['data']['inventoryAmount']
    supportJdCarrier = supply_info['data']['supportJdCarrier']
    jdExtraCostPrice = supply_info['data']['jdExtraCostPrice']
    supportSfCarrier = supply_info['data']['supportSfCarrier']
    sfExtraCostPrice = supply_info['data']['sfExtraCostPrice']

    supply_sku_infos = {}
    settle_mode = 1
    tob_settlement_price = float(800.78)
    deduct_rate = float(12.00)

    gross_profit, gross_profit_jd, gross_profit_sf = 0, 0, 0

    if settle_mode == 1:
        # 供货价模式: 毛利 = tob结算价 - 供货价
        gross_profit = tob_settlement_price - supply_sku_price
        # 有特殊承运商发货额外成本，需要减去
        if supportJdCarrier is True and jdExtraCostPrice != 0:
            gross_profit_jd = gross_profit - jdExtraCostPrice
        if supportSfCarrier is True and sfExtraCostPrice != 0:
            gross_profit_sf = gross_profit - sfExtraCostPrice
        if supportJdCarrier is True and supportSfCarrier is True:
            gross_profit = max(gross_profit_jd, gross_profit_sf)

    elif settle_mode == 2:
        # 扣点模式: 毛利 = tob结算价 * 扣点
        gross_profit = tob_settlement_price * deduct_rate * 0.01
        if deduct_rate == 0.0:
            # logs.add("tob结算模式的供应sku：{} 的扣点为零".format(supply_sku_id))
            print('error0')
    out_put_dict = {
        'supply_sku_delivery_area': supply_sku_delivery_area,
        'gross_profit': gross_profit,
        'gross_profit_jd': gross_profit_jd,
        'gross_profit_sf': gross_profit_sf,
        'supply_inventory': supply_inventory
    }
    supply_sku_infos[supply_sku_id] = out_put_dict
    print(supply_sku_infos)
    # vars.put("supply_sku_infos", supply_sku_infos)


def ttt():
    # 调度策略
    schedule_strategy = 1
    # 供应sku发货地址
    supply_sku_infos = {
        "3000006675": {"supply_inventory": 600, "supply_sku_delivery_area": 3, "gross_profit": 96,
                       "gross_profit_jd": 95,
                       "gross_profit_sf": 0},
        "3000020017": {"supply_inventory": 98, "supply_sku_delivery_area": 3, "gross_profit": 96, "gross_profit_jd": 94,
                       "gross_profit_sf": 95.5}
    }
    # 下单收货地址
    receiver_province_name = "浙江省"
    # 省份和发货区域映射关系，json自动转dict
    province_with_region_mapping = {"北京市": "华北", "天津市": "华北", "河北省": "华北", "山西省": "华北", "内蒙古自治区": "华北", "上海市": "华东",
                                    "江苏省": "华东", "浙江省": "华东", "安徽省": "华东", "福建省": "华东", "江西省": "华东", "山东省": "华东",
                                    "广东省": "华南", "广西壮族自治区": "华南", "海南省": "华南", "河南省": "华中", "湖北省": "华中",
                                    "湖南省": "华中",
                                    "辽宁省": "东北", "吉林省": "东北", "黑龙江省": "东北", "陕西省": "西北", "甘肃省": "西北", "青海省": "西北",
                                    "宁夏自治区": "西北", "新疆维吾尔自治区": "西北", "重庆市": "西南", "四川省": "西南", "贵州省": "西南",
                                    "云南省": "西南",
                                    "西藏自治区": "西南", "香港特别行政区": "港澳台", "澳门特别行政区": "港澳台", "台湾省": "港澳台"}

    # DeliverySourceAreaEnum
    desc_and_value = {"华北": 1, "东北": 2, "华东": 3, "华中": 4, "华南": 5, "西南": 6, "西北": 7}

    receiver_area_desc = province_with_region_mapping[receiver_province_name]
    receiver_area = desc_and_value[receiver_area_desc]

    # 期望的符合条件的供应sku
    aspect_delivery_sku = -1

    # crm配置了白名单，白名单有京东或顺丰
    flag = 0

    # apolloy配置 : 走CRM，1:走成本，2:走距离
    if schedule_strategy == 1:
        max_profit = max(v["gross_profit"] for v in supply_sku_infos.values())
        candidate_skus = [k for k, v in supply_sku_infos.items() if v["gross_profit"] == max_profit]
        # 如果符合条件的有多个则选择库存最多的发
        if len(candidate_skus) > 1:
            max_inventory = max(supply_sku_infos[k]["supply_inventory"] for k in candidate_skus)
            aspect_delivery_sku = max(
                [k for k in candidate_skus if supply_sku_infos[k]["supply_inventory"] == max_inventory],
                key=lambda k: supply_sku_infos[k]["supply_inventory"])
        else:
            aspect_delivery_sku = candidate_skus[0]
    elif schedule_strategy == 2:
        candidate_skus = [k for k, v in supply_sku_infos.items() if v["supply_sku_delivery_area"] == receiver_area]

        if len(candidate_skus) > 1:
            max_profit = max(supply_sku_infos[k]["gross_profit"] for k in candidate_skus)
            candidate_skus = [k for k in candidate_skus if supply_sku_infos[k]["gross_profit"] == max_profit]

            if len(candidate_skus) > 1:
                max_inventory = max(supply_sku_infos[k]["supply_inventory"] for k in candidate_skus)
                aspect_delivery_sku = max(
                    [k for k in candidate_skus if supply_sku_infos[k]["supply_inventory"] == max_inventory],
                    key=lambda k: supply_sku_infos[k]["supply_inventory"]
                )
            else:
                aspect_delivery_sku = candidate_skus[0]
        else:
            if len(candidate_skus) > 0:
                aspect_delivery_sku = candidate_skus[0]
            else:
                aspect_delivery_sku = -1
    if aspect_delivery_sku == -1:
        print(
            'error: supply_sku_infos:{} with receiver_area:{} has no correct delivery area'.format(
                supply_sku_infos,
                receiver_area))
    print(aspect_delivery_sku)
    # vars.put("aspect_delivery_sku", aspect_delivery_sku)


def order_youhua():
    category_1_id = 295
    apolloy_list = [{"category1Id": 291, "threshold": 5000}, {"category1Id": 281, "threshold": 3},
                    {"category1Id": 289, "threshold": 3}, {"category1Id": 295, "threshold": 3},
                    {"category1Id": 298, "threshold": 3},
                    {"category1Id": 379, "threshold": 3}, {"category1Id": 284, "threshold": 3},
                    {"category1Id": 293, "threshold": 3}]


if __name__ == '__main__':
    save = 'D:/PythonProjects/setaProject/setaone/tests/test_files/koudian_save.json'
    submit = 'D:/PythonProjects/setaProject/setaone/tests/test_files/koudian_submit.json'
    with open(file=save, mode='r', encoding='utf-8') as f1:
        save_j = json.load(f1)
    with open(file=submit, mode='r', encoding='utf-8') as f2:
        submit_j = json.load(f2)
    find_different_keys(save_j, submit_j)
