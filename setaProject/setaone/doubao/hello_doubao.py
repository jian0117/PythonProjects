from volcenginesdkarkruntime import Ark
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import base64
from openai import OpenAI
import json


'''
1. 如下命令安装环境
pip install --upgrade "openai>=1.0"
2. 然后参考如下示例代码进行调用
↓↓↓
'''

def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def main():

    api_key = '6d4490f5-268a-4873-9a76-e31a3413d7e7'
    client = OpenAI(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key=api_key,
    )
    base64_data = image_to_base64("D:\\ChromeDownload\\guangchen.jpeg")
    response = client.responses.create(
        model="doubao-seed-1-8-251228",
        input=[
            {
                "role": "user",
                "content": [

                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{base64_data}"
                    },
                    {
                        "type": "input_text",
                        "text": "你看见了什么？这个东西是一件护肤品商品的图片吗"
                    },
                ],
            }
        ]
    )
    answer = response.output[1].content[0].text
    print("✅ AI 回答：", answer)
    result_json = {
        "code": 200,
        "message": "success",
        "answer": answer,
        "model": response.model,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens
    }

    # 格式化打印 JSON
    print("\n✅ JSON 格式结果：")
    print(json.dumps(result_json, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()