# ====================== 1. 接收传参并初始化变量 ======================
tob_settlement_price = ${tobSettlementPrice}
threshold = ${threshold}
count = ${count}
# needPriceCheck：优先取传参值，无传参则默认0
needPriceCheck = runVars.get("needPriceCheck")
needPriceCheck = 0 if (needPriceCheck is None or str(needPriceCheck).strip() == "") else needPriceCheck
logs.add(f'needPriceCheck的值是：{needPriceCheck}')
calc_count = 0

# ====================== 2. 基础集采阈值计算 ======================
# 先计算calc_count，不先设置calc_type（避免被覆盖）
# 如果多sku不适用，多sku需要根据类目去汇总价格
if threshold > 0:
    if round(tob_settlement_price * count, 2) <= threshold:
        gap_count = threshold // tob_settlement_price + 1
        calc_count = gap_count
        logs.add("sku：{}的订单需要下单量为{}才能满足集采阈值".format(${skuId}, gap_count))
        else:
        # threshold≤0时，calc_count保持0
        pass

# ====================== 3. 核心逻辑：根据needPriceCheck确定calc_type和final_count ======================
final_count = count  # 兜底默认值（保证不为0）
calc_type = 1  # 默认普通订单

if needPriceCheck == 1:
    # 强制集采：calc_type固定为2（集采订单）
    calc_type = 2
    # 处理count：有合法calc_count则用，否则兜底原始count+日志
    if calc_count > 0:
        final_count = calc_count
    else:
        final_count = count
        logs.add(
            f"【异常】sku：${skuId} needPriceCheck=1（强制集采）但calc_count=0，兜底使用原始count={count}；threshold={threshold}，tob_settlement_price={tob_settlement_price}")
else:
    # needPriceCheck=0：按原有threshold逻辑判断calc_type
    if threshold > 0:
        if round(tob_settlement_price * count, 2) <= threshold:
            calc_type = 1  # 普通订单
        else:
            calc_type = 2  # 集采订单
    else:
        calc_type = 1  # threshold≤0，普通订单

# 最终设置calc_type到变量
vars.put("calc_type", calc_type)

# ====================== 4. 合并后段代码（使用final_count） ======================
standardPrice, skuId, itemName, tobSettlementPrice = ${standardPrice}, ${skuId}, "${itemName}", ${
    tobSettlementPrice}
orderItemList = []

# 计算时使用final_count（确保不为0）
subtotalPrice = round(standardPrice * final_count, 2)

orderItem = {
    "count": final_count,  # 最终下单数量（兜底后不会为0）
    "name": itemName,
    "originPrice": standardPrice,
    "skuId": skuId,
    "subtotalPrice": subtotalPrice,
    "channelSkuId": "channelSkuId-mock"
}
orderItemList.append(orderItem)

# 集采阈值计算也同步使用final_count
calc_threshold = round(final_count * tobSettlementPrice, 2)

# 变量存储（保持原有逻辑）
vars.put("calc_count", calc_count)
vars.put("orderItemList", orderItemList)
vars.put("totalPrice", subtotalPrice)
vars.put("calcThreshold", calc_threshold)
