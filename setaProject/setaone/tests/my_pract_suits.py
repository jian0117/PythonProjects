import json
import itertools
from collections import deque
import string
import random
import datetime
import time
import uuid


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def fun01(data):
    skuids = [item['skuId'] for item in data if 'skuId' in item]
    return tuple(skuids)

def fun01_1():
    data = json.loads('[{"id":46634,"stratification":"abprice","businessFormDesc":"代销","spuId":470209143,"spuName":"灵活扣点测试","skuId":472388501,"displayString":"红色*L","priceStatus":1,"canUseCoupon":true,"canUserRedPacket":false,"flatSalePrice":{"price":90.0,"gear":"p4"},"flatSalePriceInAudit":null,"shoppingFestivalPrice":{"price":80.0,"gear":"p3"},"shoppingFestivalPriceInAudit":null,"creator":"wb.guojian03@mesg.corp.netease.com","updator":"wb.guojian03@mesg.corp.netease.com","updateTime":1713843265000,"buName":"海外综合部（不要乱改负责人太影响测试了！）","l1CategoryName":null,"l2CategoryName":null,"auditId":null},{"id":46635,"stratification":"abprice","businessFormDesc":"代销","spuId":470209143,"spuName":"灵活扣点测试","skuId":472388502,"displayString":"红色*XL","priceStatus":1,"canUseCoupon":true,"canUserRedPacket":false,"flatSalePrice":{"price":90.0,"gear":"p4"},"flatSalePriceInAudit":null,"shoppingFestivalPrice":{"price":80.0,"gear":"p3"},"shoppingFestivalPriceInAudit":null,"creator":"wb.guojian03@mesg.corp.netease.com","updator":"wb.guojian03@mesg.corp.netease.com","updateTime":1713843265000,"buName":"海外综合部（不要乱改负责人太影响测试了！）","l1CategoryName":null,"l2CategoryName":null,"auditId":null},{"id":46636,"stratification":"abprice","businessFormDesc":"代销","spuId":470209143,"spuName":"灵活扣点测试","skuId":472388503,"displayString":"白色*L","priceStatus":1,"canUseCoupon":true,"canUserRedPacket":false,"flatSalePrice":{"price":90.0,"gear":"p4"},"flatSalePriceInAudit":null,"shoppingFestivalPrice":{"price":80.0,"gear":"p3"},"shoppingFestivalPriceInAudit":null,"creator":"wb.guojian03@mesg.corp.netease.com","updator":"wb.guojian03@mesg.corp.netease.com","updateTime":1713843265000,"buName":"海外综合部（不要乱改负责人太影响测试了！）","l1CategoryName":null,"l2CategoryName":null,"auditId":null}]')
    skuids = tuple([item['skuId'] for item in data])
    return skuids

def fun02():

    parsed_data = json.loads('[{"id":46634,"stratification":"abprice","businessFormDesc":"代销","spuId":470209143,"spuName":"灵活扣点测试","skuId":472388501,"displayString":"红色*L","priceStatus":1,"canUseCoupon":true,"canUserRedPacket":false,"flatSalePrice":{"price":90.0,"gear":"p4"},"flatSalePriceInAudit":null,"shoppingFestivalPrice":{"price":80.0,"gear":"p3"},"shoppingFestivalPriceInAudit":null,"creator":"wb.guojian03@mesg.corp.netease.com","updator":"wb.guojian03@mesg.corp.netease.com","updateTime":1713843265000,"buName":"海外综合部（不要乱改负责人太影响测试了！）","l1CategoryName":null,"l2CategoryName":null,"auditId":null},{"id":46635,"stratification":"abprice","businessFormDesc":"代销","spuId":470209143,"spuName":"灵活扣点测试","skuId":472388502,"displayString":"红色*XL","priceStatus":1,"canUseCoupon":true,"canUserRedPacket":false,"flatSalePrice":{"price":90.0,"gear":"p4"},"flatSalePriceInAudit":null,"shoppingFestivalPrice":{"price":80.0,"gear":"p3"},"shoppingFestivalPriceInAudit":null,"creator":"wb.guojian03@mesg.corp.netease.com","updator":"wb.guojian03@mesg.corp.netease.com","updateTime":1713843265000,"buName":"海外综合部（不要乱改负责人太影响测试了！）","l1CategoryName":null,"l2CategoryName":null,"auditId":null},{"id":46636,"stratification":"abprice","businessFormDesc":"代销","spuId":470209143,"spuName":"灵活扣点测试","skuId":472388503,"displayString":"白色*L","priceStatus":1,"canUseCoupon":true,"canUserRedPacket":false,"flatSalePrice":{"price":90.0,"gear":"p4"},"flatSalePriceInAudit":null,"shoppingFestivalPrice":{"price":80.0,"gear":"p3"},"shoppingFestivalPriceInAudit":null,"creator":"wb.guojian03@mesg.corp.netease.com","updator":"wb.guojian03@mesg.corp.netease.com","updateTime":1713843265000,"buName":"海外综合部（不要乱改负责人太影响测试了！）","l1CategoryName":null,"l2CategoryName":null,"auditId":null}]')
    result = {}

    for item in parsed_data:
        sku_id = item["skuId"]
        flat_sale_price = item["flatSalePrice"]["price"]
        shopping_festival_price = item["shoppingFestivalPrice"]["price"]
        result[sku_id] = (flat_sale_price, shopping_festival_price)
    print(result)

def fun02_1():

    parsed_data = json.loads('[{"id":46634,"stratification":"abprice","businessFormDesc":"代销","spuId":470209143,"spuName":"灵活扣点测试","skuId":472388501,"displayString":"红色*L","priceStatus":1,"canUseCoupon":true,"canUserRedPacket":false,"flatSalePrice":{"price":90.0,"gear":"p4"},"flatSalePriceInAudit":null,"shoppingFestivalPrice":{"price":80.0,"gear":"p3"},"shoppingFestivalPriceInAudit":null,"creator":"wb.guojian03@mesg.corp.netease.com","updator":"wb.guojian03@mesg.corp.netease.com","updateTime":1713843265000,"buName":"海外综合部（不要乱改负责人太影响测试了！）","l1CategoryName":null,"l2CategoryName":null,"auditId":null},{"id":46635,"stratification":"abprice","businessFormDesc":"代销","spuId":470209143,"spuName":"灵活扣点测试","skuId":472388502,"displayString":"红色*XL","priceStatus":1,"canUseCoupon":true,"canUserRedPacket":false,"flatSalePrice":{"price":90.0,"gear":"p4"},"flatSalePriceInAudit":null,"shoppingFestivalPrice":{"price":80.0,"gear":"p3"},"shoppingFestivalPriceInAudit":null,"creator":"wb.guojian03@mesg.corp.netease.com","updator":"wb.guojian03@mesg.corp.netease.com","updateTime":1713843265000,"buName":"海外综合部（不要乱改负责人太影响测试了！）","l1CategoryName":null,"l2CategoryName":null,"auditId":null},{"id":46636,"stratification":"abprice","businessFormDesc":"代销","spuId":470209143,"spuName":"灵活扣点测试","skuId":472388503,"displayString":"白色*L","priceStatus":1,"canUseCoupon":true,"canUserRedPacket":false,"flatSalePrice":{"price":90.0,"gear":"p4"},"flatSalePriceInAudit":null,"shoppingFestivalPrice":{"price":80.0,"gear":"p3"},"shoppingFestivalPriceInAudit":null,"creator":"wb.guojian03@mesg.corp.netease.com","updator":"wb.guojian03@mesg.corp.netease.com","updateTime":1713843265000,"buName":"海外综合部（不要乱改负责人太影响测试了！）","l1CategoryName":null,"l2CategoryName":null,"auditId":null}]')
    result = {}
    skuid = 472388501

    for item in parsed_data:
        sku_id = item["skuId"]
        flat_sale_price = item["flatSalePriceInAudit"]
        shopping_festival_price = item["shoppingFestivalPriceInAudit"]
        result[sku_id] = (flat_sale_price, shopping_festival_price)
    if result[skuid]:
        print(True)
    else:
        print(False)
    #print(result)

def fun03():
    c = lambda s,y:s[0]+y[1]
    print(c((0,1),(2,4)))

def fun04():
    n = int(input())
    k = int(input())
    print(list(itertools.combinations(range(1, n + 1), k)))

def add(x: int, y: int) -> int:
    return x + y

def num_islands_200(grid):
    def dfs(grid, r, c):
        if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]) or grid[r][c] == '0':
            return
        grid[r][c] = '0'  # 将当前岛屿标记为已访问
        dfs(grid, r+1, c)  # 上下左右进行深度优先搜索
        dfs(grid, r-1, c)
        dfs(grid, r, c+1)
        dfs(grid, r, c-1)

    if not grid:
        return 0

    num_islands = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '1':  # 如果当前位置为陆地
                num_islands += 1  # 发现新的岛屿
                dfs(grid, i, j)  # 对相邻的陆地进行深度优先搜索，将其标记为已访问
    return num_islands

def max_proper_dishes():
    n, m = map(int, input().split())
    dishes = [list(map(int, input().split())) for _ in range(n)]

    dishes.sort(key=lambda x: x[1])  # 按照变得刚好合适的时间排序

    count = 0
    time = 0
    for dish in dishes:
        if dish[0] > time:
            if dish[0] - time > m:
                count += 1
                time = dish[0] + m
            else:
                time = time + m
    return count

def getIntersectionNode_160(headA, headB):
    if not headA or not headB:
        return None

    pa, pb = headA, headB
    while pa is not pb:
        pa = pa.next if pa else headB
        pb = pb.next if pb else headA

    return pa

def orangesRotting_994(grid):
    m, n = len(grid), len(grid[0])
    fresh = 0
    rotten = deque()

    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                fresh += 1
            elif grid[i][j] == 2:
                rotten.append((i, j))

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    minutes = 0

    while rotten and fresh > 0:
        for _ in range(len(rotten)):
            x, y = rotten.popleft()
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] == 1:
                    grid[nx][ny] = 2
                    fresh -= 1
                    rotten.append((nx, ny))
        minutes += 1

    return minutes if fresh == 0 else -1

def coinChange_322(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1


def findLengthOfLCIS_674(nums):
    if not nums:
        return 0

    max_length = 1
    current_length = 1

    for i in range(1, len(nums)):
        if nums[i] > nums[i-1]:
            current_length += 1
            max_length = max(max_length, current_length)
        else:
            current_length = 1

    return max_length

def compare_json(json1, json2):
    keys = sorted(set(json1.keys()) | set(json2.keys()))
    for key in keys:
        value1 = json1.get(key)
        value2 = json2.get(key)
        if value1 != value2:
            if value2 is None:
                value2 = ""  # 若json2没有json1的key，则json2的key置空
            print(f"Key: {key}, JSON1 value: {value1}, JSON2 value: {value2}")

def remove_spaces_and_newlines(input_string):
    return input_string.replace(" ", "").replace("\n", "").replace("\r", "")


def convert_json_content(json_content):
    # 将字符串解析成对象
    parsed_json = json.loads(json_content)

    # 内部的 JSON 字符串解析成对象
    shop_content = json.loads(parsed_json['shopContent'])
    parsed_json['shopContent'] = shop_content

    # 返回内部的 JSON对象
    return parsed_json

def convert_to_json_string(shop_content):
    # 将对象转换为 JSON 字符串
    shop_content_string = json.dumps(shop_content)

    # 将 JSON 字符串嵌入到外部 JSON 对象中
    result = {"shopContent": shop_content_string}

    # 返回外部的 JSON 对象
    return json.dumps(result)


def list_dict_dedup(your_list):
    # 对包含字典的列表进行去重可以通过将列表转换为集合，但是由于集合不支持包含可变类型（比如字典）的元素，因此需要先将字典转换为元组。以下是一个示例代码，演示了如何对包含字典的列表进行去重：
    # 先将每个字典转换为元组，然后转换为集合，最后再转换回列表
    unique_list = [dict(t) for t in {tuple(d.items()) for d in your_list}]
    return unique_list

def sort_json_keys(json_data):
    #  print(json.dumps(sort_json_keys(json.loads(input())), ensure_ascii=False))
    if isinstance(json_data, dict):
        return {k: sort_json_keys(v) for k, v in sorted(json_data.items())}
    elif isinstance(json_data, list):
        return [sort_json_keys(item) for item in json_data]
    else:
        return json_data


def get_random_code(length):
  characters = string.ascii_lowercase + string.digits
  return ''.join(random.choice(characters) for _ in range(length))

def time_now():
    return time.strftime('%Y%m%d')

def open_file():
    file_path = r'D:\PythonProjects\setaProject\setaone\tests\test_files\json_data.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        data_dict = json.load(f)

if __name__ == '__main__':
    #print(json.dumps(input()))
    print(json.dumps(sort_json_keys(json.loads(input())),ensure_ascii=False))