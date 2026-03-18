import requests

# 全局配置（可根据项目改）
DEFAULT_TIMEOUT = 10  # 请求超时时间
DEFAULT_CONTENT_TYPE = "application/json"  # 默认 JSON 类型


class RequestUtil:
    """
    HTTP 请求工具类：极简调用，支持 get/post/put/delete
    默认请求体为 JSON，支持传 cookie，header 不自定义
    """

    @staticmethod
    def request(method: str, url: str, params=None, data=None, json=None, cookies=None):
        """
        通用请求方法
        :param method: 请求方式 GET/POST/PUT/DELETE
        :param url: 请求地址
        :param params: URL 参数（?xxx=xxx）
        :param data: 表单参数
        :param json: JSON 请求体（默认）
        :param cookies: 字典格式 cookie，非必填
        :return: 响应对象 / 抛出异常
        """
        # 固定请求头（不支持自定义）
        headers = {
            "Content-Type": DEFAULT_CONTENT_TYPE
        }

        try:
            # 发送请求
            response = requests.request(
                method=method.upper(),
                url=url,
                params=params,
                data=data,
                json=json,
                cookies=cookies,
                headers=headers,
                timeout=DEFAULT_TIMEOUT
            )
            # 自动检查 HTTP 状态码（4xx/5xx 直接抛错）
            response.raise_for_status()
            return response

        except Exception as e:
            print(f"请求失败：{str(e)}")
            raise

    # ———————————— 极简调用方法 ————————————
    @staticmethod
    def get(url: str, params=None, cookies=None):
        """GET 请求"""
        return RequestUtil.request("GET", url, params=params, cookies=cookies)

    @staticmethod
    def post(url: str, json=None, data=None, cookies=None):
        """POST 请求（默认 JSON）"""
        return RequestUtil.request("POST", url, json=json, data=data, cookies=cookies)

    @staticmethod
    def put(url: str, json=None, data=None, cookies=None):
        """PUT 请求"""
        return RequestUtil.request("PUT", url, json=json, data=data, cookies=cookies)

    @staticmethod
    def delete(url: str, json=None, cookies=None):
        """DELETE 请求"""
        return RequestUtil.request("DELETE", url, json=json, cookies=cookies)


# ———————————— 使用示例（直接抄） ————————————
if __name__ == '__main__':
    # 1. GET 带参数 + cookie
    res = RequestUtil.get(
        url="https://httpbin.org/get",
        params={"id": 1001},
        cookies={"token": "abcd1234"}
    )
    print("GET 结果：", res.json())

    # 2. POST JSON（默认）
    res = RequestUtil.post(
        url="https://httpbin.org/post",
        json={"username": "test", "password": "123456"}
    )
    print("POST 结果：", res.json())

    # 3. POST 表单（非 JSON，手动传 data）
    res = RequestUtil.post(
        url="https://httpbin.org/post",
        data={"name": "张三", "age": 20}
    )