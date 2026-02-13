import re
import json

def extract_json_data(input_string):
    json_data_list = re.findall(r'(?<=data:)(.*?)(?=\nevent:|$', input_string, re.DOTALL)  # 使用正则表达式找到所有的JSON格式数据
    extracted_data = [json.loads(data) for data in json_data_list]  # 解析每个JSON格式数据
    return extracted_data



# 示例用法
if __name__ == '__main__':
    # 示例用法
    input_string = """
    event:ping
    event:message
    data:{"status":0,"qid":"11765266360204077745","pkgId":"4a1e6093-8d25-4c23-8ace-4befe5a6a97b_0","sessionId":"bd895d90-afc4-4386-bbb8-41ec072832e6","isDefault":1,"isShow":0,"data":{"message":{"msgId":"4a1e6093-8d25-4c23-8ace-4befe5a6a97b","isRebuild":false,"updateTime":"1718611973978","metaData":{"state":"waiting-resp","endTurn":false,"userInfo":{"status":3},"speedInfo":{}},"content":{}}},"seq_id":0}
    """
    json_data = extract_json_data(input_string)

    for data in json_data:
        print(data)