from volcenginesdkarkruntime import Ark
import requests

client = Ark(
    api_key='6d4490f5-268a-4873-9a76-e31a3413d7e7',
    base_url="https://ark.cn-beijing.volces.com/api/v3",  # 固定请求地址
)

# 调用模型
completion = client.chat.completions.create(
    model="doubao-seed-1-8-251228",  # 替换为您需要的模型ID
    messages=[
        {"role": "user", "content": "Hello!"},
    ],
    stream=True  # 支持流式输出
)