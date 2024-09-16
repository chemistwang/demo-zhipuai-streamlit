from datetime import datetime
import requests
import os

def sendEmail(user:str, content: str) -> str:
    print(user, content)
    print('发送邮件成功！')
    return f"已经给{user}发送邮件成功！内容为{content}"

def sendSMS(user:str, content:str) -> str:
    print(user, content)
    print('发送短信成功')
    return f"已经给{user}发送短信成功！内容为{content}"


# 获取当前时间
def get_current_time() -> str:
    current_datetime = datetime.now()
    formatted_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    print('当前时间为：', formatted_time)
    return formatted_time

# 获取天气
def get_current_weather(city: str) -> str:
    API_KEY = os.getenv('GAODE_API_KEY')
    url=f"https://restapi.amap.com/v3/weather/weatherInfo?key={API_KEY}&city={city}"
    response = requests.get(url)
    if not response.ok:
        return ValueError('获取天气失败')
    response_data = response.json()
    info = response_data['lives'][0]
    res = f"{info['province']}{info['city']}的天气是{info['weather']}, 气温{info['temperature']}"
    print(res)
    return res

