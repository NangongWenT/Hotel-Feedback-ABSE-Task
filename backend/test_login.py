"""测试登录功能"""
import requests
import json

# 测试登录
url = "http://localhost:5000/api/auth/login"
data = {
    "username": "admin",
    "password": "admin123"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    if response.status_code == 200:
        print("[OK] 登录成功！")
    else:
        print(f"[ERROR] 登录失败: {response.text}")
except Exception as e:
    print(f"[ERROR] 请求失败: {str(e)}")

