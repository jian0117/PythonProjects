import urllib3_tool

# 创建一个 PoolManager 对象
http = urllib3_tool.PoolManager()

# 发送GET请求
url = 'http://www.example.com'
response = http.request('GET', url)

# 获取响应内容
print(response.data)