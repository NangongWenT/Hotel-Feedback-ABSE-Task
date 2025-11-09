"""测试认证 API"""
import requests
import json

base_url = "http://localhost:5000"

print("=" * 50)
print("测试认证 API")
print("=" * 50)
print()

# 测试健康检查
print("1. 测试健康检查...")
try:
    response = requests.get(f"{base_url}/api/health", timeout=5)
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    print("   [OK] 健康检查通过")
except Exception as e:
    print(f"   [ERROR] 健康检查失败: {str(e)}")
print()

# 测试登录
print("2. 测试登录...")
try:
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    response = requests.post(
        f"{base_url}/api/auth/login",
        json=login_data,
        timeout=10
    )
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.text}")
    
    if response.status_code == 200:
        print("   [OK] 登录成功！")
        data = response.json()
        print(f"   用户: {data.get('user', {}).get('username')}")
    else:
        print(f"   [ERROR] 登录失败")
        try:
            error_data = response.json()
            print(f"   错误信息: {error_data.get('error', '未知错误')}")
        except:
            print(f"   原始响应: {response.text}")
except Exception as e:
    print(f"   [ERROR] 请求失败: {str(e)}")
    import traceback
    traceback.print_exc()
print()

# 测试获取当前用户（需要先登录）
print("3. 测试获取当前用户（需要登录）...")
try:
    # 创建一个 session 来保持 cookies
    session = requests.Session()
    
    # 先登录
    login_response = session.post(
        f"{base_url}/api/auth/login",
        json={"username": "admin", "password": "admin123"},
        timeout=10
    )
    
    if login_response.status_code == 200:
        print("   登录成功，获取用户信息...")
        me_response = session.get(f"{base_url}/api/auth/me", timeout=5)
        print(f"   状态码: {me_response.status_code}")
        print(f"   响应: {me_response.text}")
        
        if me_response.status_code == 200:
            print("   [OK] 获取用户信息成功！")
        else:
            print(f"   [ERROR] 获取用户信息失败")
    else:
        print(f"   [ERROR] 登录失败，无法测试获取用户信息")
        print(f"   登录响应: {login_response.text}")
except Exception as e:
    print(f"   [ERROR] 请求失败: {str(e)}")
    import traceback
    traceback.print_exc()

print()
print("=" * 50)
print("测试完成")
print("=" * 50)


