from zhipuai import ZhipuAI
import os

client = ZhipuAI(api_key=os.getenv('ZHIPU_API_KEY')) # 请填写您自己的APIKey
response = client.images.generations(
    model="cogview-3-plus", #填写需要调用的模型编码
    prompt="一只可爱的小猫咪",
)

print(response.data[0].url)