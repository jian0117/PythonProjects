
from volcenginesdkarkruntime import Ark




if __name__ == "__main__":
    client = Ark(
        base_url='https://ark.cn-beijing.volces.com/api/v3',
        api_key='6d4490f5-268a-4873-9a76-e31a3413d7e7',
    )

    response = client.responses.create(
        model="doubao-seed-1-8-251228",
        input=[
            {
                "role": "user",
                "content": [

                    {
                        "type": "input_image",
                        "image_url": "https://ark-project.tos-cn-beijing.volces.com/doc_image/ark_demo_img_1.png"
                    },
                    {
                        "type": "input_text",
                        "text": "你看见了什么？"
                    },
                ],
            }
        ]
    )
    print(response)