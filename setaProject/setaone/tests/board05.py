import json

def validate_config(config):
    temp_threshold = 0
    for threshold, gift_sku_id_list, count in config:
        if not isinstance(threshold, (int, float)) and isinstance(gift_sku_id_list,(tuple, list)) and count <= len(gift_sku_id_list) and threshold > temp_threshold and isinstance(count, (int, float)):
            return False
        temp_threshold = threshold
    return True

if __name__ == '__main__':
    response_data_list = [{'id': None, 'activityId': None, 'activityType': None, 'spuId': 470209143, 'spuName': '灵活扣点测试', 'skuId': 472388502, 'displayString': '红色*XL', 'selfRun': False, 'businessFormDesc': None, 'daiXTwo': True, 'profitRateDesc': None, 'actualPrice': 100.0, 'priceGear': None, 'activityPrice': 100.0, 'updateTime': None, 'skuInventory': {'canAllocateInventory': 100009, 'lockVolume': 2, 'autoAddInventory': False, 'volumeLowThr': None, 'volumeAutoAddTo': None}, 'skuAffiliation': {'affiliationId': 10101, 'free': False, 'cheap': False, 'costPayer': 2}, 'preSellStartTime': None, 'preSellEndTime': None, 'downPaymentPrice': None, 'balancePrice': None, 'editFlag': True, 'presell': False}, {'id': None, 'activityId': None, 'activityType': None, 'spuId': 470209143, 'spuName': '灵活扣点测试', 'skuId': 472388503, 'displayString': '白色*L', 'selfRun': False, 'businessFormDesc': None, 'daiXTwo': True, 'profitRateDesc': None, 'actualPrice': 100.0, 'priceGear': None, 'activityPrice': 100.0, 'updateTime': None, 'skuInventory': {'canAllocateInventory': 99999, 'lockVolume': 2, 'autoAddInventory': False, 'volumeLowThr': None, 'volumeAutoAddTo': None}, 'skuAffiliation': {'affiliationId': 10101, 'free': False, 'cheap': False, 'costPayer': 2}, 'preSellStartTime': None, 'preSellEndTime': None, 'downPaymentPrice': None, 'balancePrice': None, 'editFlag': True, 'presell': False}, {'id': None, 'activityId': None, 'activityType': None, 'spuId': 470209143, 'spuName': '灵活扣点测试', 'skuId': 472388504, 'displayString': '白色*XL', 'selfRun': False, 'businessFormDesc': None, 'daiXTwo': True, 'profitRateDesc': None, 'actualPrice': 100.0, 'priceGear': None, 'activityPrice': 100.0, 'updateTime': None, 'skuInventory': {'canAllocateInventory': 200030, 'lockVolume': 2, 'autoAddInventory': False, 'volumeLowThr': None, 'volumeAutoAddTo': None}, 'skuAffiliation': {'affiliationId': 10101, 'free': False, 'cheap': False, 'costPayer': 2}, 'preSellStartTime': None, 'preSellEndTime': None, 'downPaymentPrice': None, 'balancePrice': None, 'editFlag': True, 'presell': False}]
    stepsPriceConfig = [(1000, [472388504, 472388502], 1), (2000, [472388503], 1)]
    steps = []
    type = ''

    if (validate_config(stepsPriceConfig)):
        for i in range(len(stepsPriceConfig)):
            giftInfo_list = []
            for j in range(len(stepsPriceConfig[i][1])):
                skuId = stepsPriceConfig[i][1][j]
                giftInfo_d = {
                    "itemId": [item["spuId"] for item in response_data_list if item["skuId"] == skuId][0],
                    "spuName": [item["spuName"] for item in response_data_list if item["skuId"] == skuId][0],
                    "skuId": skuId,
                    "displayString": [item["displayString"] for item in response_data_list if item["skuId"] == skuId][0],
                    "original": [item["actualPrice"] for item in response_data_list if item["skuId"] == skuId][0],
                    "each": 1
                }
                giftInfo_list.append(giftInfo_d)
            # 明天加个逻辑判断满额还是满件，配置不同参数
            if type == 1:
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
            elif type == '':
                steps_d = {
                    "name": "满{}元赠".format(stepsPriceConfig[i][0]),
                    "priority": i,
                    "activityDetailOperateParam": {
                        "isCountAtMultiple": False,
                        "isPriceOverCondition": True,
                        "isItemOverCondition": False,
                        "allowCount": stepsPriceConfig[i][2],
                        "countAt": stepsPriceConfig[i][0],
                        "giftInfos": giftInfo_list
                    }
                }
            steps.append(steps_d)
        print(json.dumps(steps, ensure_ascii=False))
    else:
        print('invalid config')


    gift_sku_id_list = [sku_id for gift_list in [item[1] for item in stepsPriceConfig] for sku_id in gift_list]
    print(gift_sku_id_list)