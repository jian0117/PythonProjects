import re
activityOptSkuListResult = {} #${activityOptSkuListResult}
actualPrice_dict = {}
for item in activityOptSkuListResult:
    sku_id = item["skuId"]
    actual_price = item["actualPrice"]
    actualPrice_dict[sku_id] = actual_price
activityPrice_dict = {} #${sku_dict}
allPrice_dict = {
    key: {
        '原价': actualPrice_dict.get(key),
        '定金': activityPrice_dict.get(key).get('定金'),
        '尾款': activityPrice_dict.get(key).get('尾款')
    }
    for key in set(actualPrice_dict) | set(activityPrice_dict)
}

default_discount = 0.9
downpayment_default_discount = 0.2
balancepayment_default_discount = 0.7
finalPrice_dict = {}

for key, value in allPrice_dict.items():
    if isinstance(value, dict):
        finalPrice_dict[key] = {}
        for k, v in value.items():
            if isinstance(v, (int, float)):
                finalPrice_dict[key][k] = v
            elif any(char.isdigit() for char in str(v)):
                if '%' in str(v):
                    discount_str = re.findall(r"(\d{1,2})%", str(v))
                    if str(k) == '定金':
                        default_discount = downpayment_default_discount
                    elif str(k) == '尾款':
                        default_discount = balancepayment_default_discount
                    discount = float(discount_str[0]) / 100 if discount_str else default_discount
                    finalPrice_dict[key][k] = value['原价'] * discount
                else:
                    discount_str = re.findall(r"[0]\.\d+", str(v))
                    if str(k) == '定金':
                        default_discount = downpayment_default_discount
                    elif str(k) == '尾款':
                        default_discount = balancepayment_default_discount
                    discount = float(discount_str[0]) if discount_str else default_discount
                    finalPrice_dict[key][k] = value['原价'] * discount
            else:
                if str(k) == '定金':
                    default_discount = downpayment_default_discount
                elif str(k) == '尾款':
                    default_discount = balancepayment_default_discount
                finalPrice_dict[key][k] = value['原价'] * default_discount

vars.put("skuIdAndActivityPrice", finalPrice_dict)


import json

#阶梯价处理
stepsPriceConfig = [(100,2),(200,5)]
steps = []

for i in range(len(stepsPriceConfig)):
  steps_d = {
      "name": "我是阶梯" + str(i + 1),
      "priority": i,
      "activityDetailOperateParam": {
        "asc": False,
        "packagePrice": stepsPriceConfig[i][0],
        "isPackagePriceAction": True,
        "packageNum": stepsPriceConfig[i][1]
      }
    }
  steps.append(steps_d)
vars.put("activityMultiDetail", json.dumps(steps, ensure_ascii=False))

