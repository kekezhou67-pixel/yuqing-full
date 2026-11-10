import requests

url = "http://localhost:8888/analyze"
data = {
    "title": "产品太差",
    "content": "这个产品太差劲了，我要投诉",
    "source": "weibo"
}

response = requests.post(url, json=data)
print("状态码：", response.status_code)
print("返回结果：", response.json())
