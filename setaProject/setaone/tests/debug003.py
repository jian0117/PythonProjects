if __name__ == '__main__':
    # 调度策略
    schedule_strategy = 2
    # 供应sku发货地址
    supply_sku_infos = {"3000020053": {"supply_sku_price": 350.98, "supply_sku_delivery_area": 3},
                        "3000020052": {"supply_sku_price": 300.98, "supply_sku_delivery_area": 7},
                        "3000006708": {"supply_sku_price": 300.98, "supply_sku_delivery_area": 3}}
    # 下单收货地址
    receiver_province_name = "浙江省"
    # 省份和发货区域映射关系，json自动转dict
    province_with_region_mapping = {"北京市": "华北", "天津市": "华北", "河北省": "华北", "山西省": "华北", "内蒙古自治区": "华北", "上海市": "华东",
                                    "江苏省": "华东", "浙江省": "华东", "安徽省": "华东", "福建省": "华东", "江西省": "华东", "山东省": "华东",
                                    "广东省": "华南", "广西壮族自治区": "华南", "海南省": "华南", "河南省": "华中", "湖北省": "华中", "湖南省": "华中",
                                    "辽宁省": "东北", "吉林省": "东北", "黑龙江省": "东北", "陕西省": "西北", "甘肃省": "西北", "青海省": "西北",
                                    "宁夏自治区": "西北", "新疆维吾尔自治区": "西北", "重庆市": "西南", "四川省": "西南", "贵州省": "西南", "云南省": "西南",
                                    "西藏自治区": "西南", "香港特别行政区": "港澳台", "澳门特别行政区": "港澳台", "台湾省": "港澳台"}
    # DeliverySourceAreaEnum
    desc_and_value = {"华北": 1, "东北": 2, "华东": 3, "华中": 4, "华南": 5, "西南": 6, "西北": 7}

    receiver_area_desc = province_with_region_mapping[receiver_province_name]
    receiver_area = desc_and_value[receiver_area_desc]

    # 符合条件的供应sku
    aspect_delivery_sku = -1
    aspect_delivery_sku_list = list()
    if schedule_strategy == 1:
        unique_prices = set(v["supply_sku_price"] for v in supply_sku_infos.values())
        if len(unique_prices) == 1:  # All prices are the same
            aspect_delivery_sku = -1
            print('供应sku的供货价都一样，随机取supply_sku，不用校验；supply_sku_infos:{}'.format(supply_sku_infos))
        else:
            min_price = min(supply_sku_infos.values(), key=lambda x: x["supply_sku_price"])["supply_sku_price"]
            aspect_delivery_sku = int([k for k, v in supply_sku_infos.items() if v["supply_sku_price"] == min_price][0])
    elif schedule_strategy == 2:
        for k, v in supply_sku_infos.items():
            if isinstance(v, dict):
                for k0, v0 in v.items():
                    if k0 == 'supply_sku_delivery_area' and v0 == receiver_area:
                        aspect_delivery_sku_list.append(k)
        if len(aspect_delivery_sku_list) == 1:
            # 断言的时候是long型（int）
            aspect_delivery_sku = int(aspect_delivery_sku_list[0])
        elif len(aspect_delivery_sku_list) < 1:
            print(
                'error: supply_sku_infos:{} with receiver_area:{} has no correct delivery area'.format(supply_sku_infos,
                                                                                                       receiver_area))
    print(aspect_delivery_sku)
