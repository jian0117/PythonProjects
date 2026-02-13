import json
import re

def test():

    sku_dict = {472388501: 50, 472388502: "0.8折", 472388503: ""}
    '''sku_mode = [(472388501, "50元"), (472388502, "原价的8折"), (472388503, " ")]
    skuIdn = lambda x: x[0]
    activityPricen = lambda x: x[1]'''
    sku_list = list(sku_dict.keys())
    #vars.put("skuIds", sku_list)

    activity_price_list = list(sku_dict.values())
    activity_price_list =  [c for c in list(sku_dict.values()) if c.isdigit()]
    discount = lambda x: ''.join(filter(lambda c: c.isdigit(), x))
    for c in list(sku_dict.values()):
        if c.isdigit():
            activity_price_list.append(c)
        elif isinstance(c, str):

            activity_price_list.append()


result =[{"skuId":472388501,"actualPrice":100.0},{"skuId":472388502,"actualPrice":75.88}]

def extract_data(data_list):
    data_dict = {}
    #parsed_data = json.loads(json_data)
    for item in data_list:
        sku_id = item["skuId"]
        actual_price = item["actualPrice"]
        data_dict[sku_id] = actual_price
    return data_dict

def assemble_dict(dict1, dict2):
    combined_dict = {key: (dict1.get(key), dict2.get(key)) for key in set(dict1) | set(dict2)}
    return combined_dict

def process_dictionary(input_dict):
    output_dict = {}
    for key, value in input_dict.items():
        if isinstance(value, list):
            if isinstance(value[1], (int, float)):
                output_dict[key] = value[1]
            elif any(c.isdigit() for c in value[1]):
                num_str = re.findall(r"[-+]?\d*\.\d+|\d+", value[1])
                num = float(num_str[0]) if num_str else 0.0
                output_dict[key] = value[0] * num
            else:
                output_dict[key] = value[0] * 0.9
        else:
            output_dict[key] = value
    return output_dict





if __name__ == '__main__':
    print(isinstance(eval(input()), dict))
    sku_dict = {472388501:"", 472388502: 88.88}
