import json

def validate_config(config):
    temp_threshold = 0
    for threshold, gift_sku_id_list, count in config:
        if not isinstance(threshold, (int, float)) and isinstance(gift_sku_id_list, (tuple, list)) and count <= len(
                gift_sku_id_list) and threshold > temp_threshold and isinstance(count, (int, float)):
            return False
        temp_threshold = threshold
    return True

if __name__ == '__main__':
    response_data_list = [{'id': None, 'activityId': None, 'activityType': None, 'spuId': 470209143, 'spuName': '灵活扣点测试', 'skuId': 472388502, 'displayString': '红色*XL', 'selfRun': False, 'businessFormDesc': None, 'daiXTwo': True, 'profitRateDesc': None, 'actualPrice': 100.0, 'priceGear': None, 'activityPrice': 100.0, 'updateTime': None, 'skuInventory': {'canAllocateInventory': 100009, 'lockVolume': 2, 'autoAddInventory': False, 'volumeLowThr': None, 'volumeAutoAddTo': None}, 'skuAffiliation': {'affiliationId': 10101, 'free': False, 'cheap': False, 'costPayer': 2}, 'preSellStartTime': None, 'preSellEndTime': None, 'downPaymentPrice': None, 'balancePrice': None, 'editFlag': True, 'presell': False}, {'id': None, 'activityId': None, 'activityType': None, 'spuId': 470209143, 'spuName': '灵活扣点测试', 'skuId': 472388503, 'displayString': '白色*L', 'selfRun': False, 'businessFormDesc': None, 'daiXTwo': True, 'profitRateDesc': None, 'actualPrice': 100.0, 'priceGear': None, 'activityPrice': 100.0, 'updateTime': None, 'skuInventory': {'canAllocateInventory': 99999, 'lockVolume': 2, 'autoAddInventory': False, 'volumeLowThr': None, 'volumeAutoAddTo': None}, 'skuAffiliation': {'affiliationId': 10101, 'free': False, 'cheap': False, 'costPayer': 2}, 'preSellStartTime': None, 'preSellEndTime': None, 'downPaymentPrice': None, 'balancePrice': None, 'editFlag': True, 'presell': False}, {'id': None, 'activityId': None, 'activityType': None, 'spuId': 470209143, 'spuName': '灵活扣点测试', 'skuId': 472388504, 'displayString': '白色*XL', 'selfRun': False, 'businessFormDesc': None, 'daiXTwo': True, 'profitRateDesc': None, 'actualPrice': 100.0, 'priceGear': None, 'activityPrice': 100.0, 'updateTime': None, 'skuInventory': {'canAllocateInventory': 200030, 'lockVolume': 2, 'autoAddInventory': False, 'volumeLowThr': None, 'volumeAutoAddTo': None}, 'skuAffiliation': {'affiliationId': 10101, 'free': False, 'cheap': False, 'costPayer': 2}, 'preSellStartTime': None, 'preSellEndTime': None, 'downPaymentPrice': None, 'balancePrice': None, 'editFlag': True, 'presell': False}]
    stepsPriceConfig = [(1000, [472388504, 472388502], 1), (2000, [472388503], 1)]
    steps = []

    if validate_config(stepsPriceConfig):
        for threshold, gift_sku_id_list, count in stepsPriceConfig:
            giftInfo_list = []
            for skuId in gift_sku_id_list:
                matching_item = next((item for item in response_data_list if item["skuId"] == skuId), None)
                if matching_item:
                    giftInfo_d = {
                        "itemId": matching_item["spuId"],
                        "spuName": matching_item["spuName"],
                        "skuId": skuId,
                        "displayString": matching_item["displayString"],
                        "original": matching_item["actualPrice"],
                        "each": 1
                    }
                    giftInfo_list.append(giftInfo_d)
                else:
                    print(f"Matching item not found for skuId: {skuId}")

            steps_d = {
                "name": "满{}元赠".format(threshold),
                "priority": stepsPriceConfig.index((threshold, gift_sku_id_list, count)),
                "activityDetailOperateParam": {
                    "isAmountAtMultiple": False,
                    "isPriceOverCondition": True,
                    "isItemOverCondition": False,
                    "allowCount": count,
                    "amountAt": threshold,
                    "giftInfos": giftInfo_list
                }
            }
            steps.append(steps_d)
        print(json.dumps(steps, ensure_ascii=False))
    else:
        print('invalid config')

    gift_sku_id_list = [sku_id for _, gift_list, _ in stepsPriceConfig for sku_id in gift_list]
    print(gift_sku_id_list)