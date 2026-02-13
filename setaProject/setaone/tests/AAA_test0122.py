from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os
import json
import requests
import hashlib

def encrypt_gbs(key, iv, content):
    if key is None or iv is None or not content.strip():
        print("加密参数不能为空")
        return None
    try:
        key = key.encode('utf-8')
        iv = iv.encode('utf-8')
        content = content.encode('utf-8')

        backend = default_backend()

        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=backend
        )
        key = base64.urlsafe_b64encode(kdf.derive(key))

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
        padder = PKCS7(128).padder()
        padded_data = padder.update(content) + padder.finalize()
        ct = encryptor.update(padded_data) + encryptor.finalize()

        return base64.b64encode(ct).decode('utf-8')
    except Exception as e:
        print("content加密异常", e)
        return None

if __name__ == '__main__':
    app_key = "GBS4yB65F1T4379jTOs7985iS2U58g73x"
    app_secret = "GBS1VewaZw8ciA48b3Q8ah856454Ly0965N6G729ewO7p3o0bU0d0"
    tenant_id = "1859422951512403969"

    md5_hash = hashlib.md5(tenant_id.encode('utf-8')).hexdigest()
    print("MD5密钥32位 =", md5_hash)

    # 获取偏移量
    iv = bytes.fromhex(md5_hash[8:24])
    print("偏移量16位 =", iv.hex())

    host = 'http://m.gtxfj.stac.fun'

    add_url = host + "/gateway/integral-platform/api/user/addEventIntegral"
    query_url = host + '/gateway/integral-platform/api/user/catalog/sumIntegral'
    headers = {'Content-Type': 'application/json'}

    add_data = {
        "businessId": "test1210_1",
        "eventCode": "YDWZ",
        "remark": "阅读文章加积分",
        "integralValue": 1000,
        "thirdUserName": "x6327890"
    }

    query_data = {
        "thirdUserName": "90001001"
    }

    # Convert data to JSON
    json_data = json.dumps(query_data, separators=(',', ':'), ensure_ascii=False)

    encryStr = encrypt_gbs(app_secret, iv.hex(), json_data)

    data = {
        "appKey": app_key,
        "encryStr": encryStr,
        "tenantId": tenant_id,
        "transNo": "20250122gjtest1"
    }

    response = requests.post(add_url, json=data, headers=headers)
    print(response.json())