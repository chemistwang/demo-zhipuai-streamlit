from zhipuai import ZhipuAI
import os

client = ZhipuAI(api_key=os.getenv('ZHIPU_API_KEY')) # 请填写您自己的APIKey


# 第一步：异步获取到视频的id
response = client.videos.generations(
    model="cogvideox",
    prompt="比得兔开小汽车，游走在马路上，脸上的表情充满开心喜悦。"
)
print(response)


# 第二步：通过视频的id获取视频的生成结果
response = client.videos.retrieve_videos_result(
    id="353717263902551889068719232768172973"
)
print(response)