import json
import re


def validate_config0(config):
    last_price = 0
    last_discount = 10
    for price, discount in config:
        if not (isinstance(price, (int, float)) and price > 0 and isinstance(discount, (int, float)) and (
                0.1 <= discount <= 9.9) and price > last_price and discount < last_discount):
            return False
        last_price = price
        last_discount = discount
    return True


def validate_config(config):
    temp_threshold = 0
    for threshold, gift_sku_id_list, count in config:
        if not isinstance(threshold, (int, float)) and isinstance(gift_sku_id_list, (tuple, list)) and count <= len(
                gift_sku_id_list) and threshold > temp_threshold and isinstance(count, (int, float)):
            return False
        temp_threshold = threshold
    return True


def validate_tuple(tuple):
    if all(isinstance(x, int) and x > 0 for x in tuple) and tuple[1] <= tuple[0] and 0.1 <= tuple[2] <= 9.9:
        return True
    else:
        return False


# 执行相应的错误处理逻辑

if __name__ == '__main__':
    # response_data_json = ${responseBody}
    # response_data_list = json.loads(response_data_json, ensure_ascii = False)
    response_data_list = [
        {"id": None, "activityId": None, "activityType": None, "spuId": 470209143, "spuName": "灵活扣点测试",
         "skuId": 472388502, "displayString": "红色*XL", "selfRun": False, "businessFormDesc": None, "daiXTwo": True,
         "profitRateDesc": None, "actualPrice": 100.0, "priceGear": None, "activityPrice": 100.0, "updateTime": None,
         "skuInventory": {"canAllocateInventory": 100009, "lockVolume": 2, "autoAddInventory": False,
                          "volumeLowThr": None, "volumeAutoAddTo": None},
         "skuAffiliation": {"affiliationId": 10101, "free": False, "cheap": False, "costPayer": 2},
         "preSellStartTime": None, "preSellEndTime": None, "downPaymentPrice": None, "balancePrice": None,
         "editFlag": True, "presell": False},
        {"id": None, "activityId": None, "activityType": None, "spuId": 470209143, "spuName": "灵活扣点测试",
         "skuId": 472388503, "displayString": "白色*L", "selfRun": False, "businessFormDesc": None, "daiXTwo": True,
         "profitRateDesc": None, "actualPrice": 100.0, "priceGear": None, "activityPrice": 100.0, "updateTime": None,
         "skuInventory": {"canAllocateInventory": 99999, "lockVolume": 2, "autoAddInventory": False,
                          "volumeLowThr": None, "volumeAutoAddTo": None},
         "skuAffiliation": {"affiliationId": 10101, "free": False, "cheap": False, "costPayer": 2},
         "preSellStartTime": None, "preSellEndTime": None, "downPaymentPrice": None, "balancePrice": None,
         "editFlag": True, "presell": False},
        {"id": None, "activityId": None, "activityType": None, "spuId": 470209143, "spuName": "灵活扣点测试",
         "skuId": 472388504, "displayString": "白色*XL", "selfRun": False, "businessFormDesc": None, "daiXTwo": True,
         "profitRateDesc": None, "actualPrice": 100.0, "priceGear": None, "activityPrice": 100.0, "updateTime": None,
         "skuInventory": {"canAllocateInventory": 200030, "lockVolume": 2, "autoAddInventory": False,
                          "volumeLowThr": None, "volumeAutoAddTo": None},
         "skuAffiliation": {"affiliationId": 10101, "free": False, "cheap": False, "costPayer": 2},
         "preSellStartTime": None, "preSellEndTime": None, "downPaymentPrice": None, "balancePrice": None,
         "editFlag": True, "presell": False}]
    stepsPriceConfig = [(100, [472388504, 472388502], 1), (1000, [472388503], 1)]
    steps = []
    # giftInfo_list = []

    if (validate_config(stepsPriceConfig)):
        for i in range(len(stepsPriceConfig)):
            giftInfo_list = []
            for j in range(len(stepsPriceConfig[i][1])):
                skuId = stepsPriceConfig[i][1][j]
                giftInfo_d = {
                    "itemId": [item["spuId"] for item in response_data_list if item["skuId"] == skuId][0],
                    "spuName": [item["spuName"] for item in response_data_list if item["skuId"] == skuId][0],
                    "skuId": skuId,
                    "displayString": [item["displayString"] for item in response_data_list if item["skuId"] == skuId][
                        0],
                    "original": [item["actualPrice"] for item in response_data_list if item["skuId"] == skuId][0],
                    "each": 1
                }
                giftInfo_list.append(giftInfo_d)

            steps_d = {
                "name": "满{}元赠".format(stepsPriceConfig[i][0]),
                "priority": i,
                "activityDetailOperateParam": {

                    "isAmountAtMultiple": False,
                    "isPriceOverCondition": True,
                    "isItemOverCondition": False,
                    "allowCount": stepsPriceConfig[i][2],
                    "amountAt": stepsPriceConfig[i][0],
                    "giftInfos": giftInfo_list

                }
            }
            steps.append(steps_d)
        # vars.put("activityMultiDetail", json.dumps(steps, ensure_ascii=False))
        print(json.dumps(steps, ensure_ascii=False))
    else:
        print('invalid config')
        enumerate()
