import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import ast
import os
from zhipuai import ZhipuAI
import json

plt.rcParams['font.sans-serif'] = ['SimHei'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False # 用来正常显示负号


text = [
    "美食非常美味，服务员也很友好。",
    "这部电影既刺激又令人兴奋。",
    "阅读书籍是扩展知识的好方法。",
    '春天的花朵绽放得特别美丽。',
    "小狗在草地上欢快地奔跑。",
    "夕阳下的海面波光粼粼。",
    "她的笑容如阳光般温暖。",
    "夜空中的星星闪烁着光芒。",
    "书架上摆满了各种书籍。",
    "风吹动树叶，发出沙沙声。",
    "一杯热茶温暖了心灵。",
    "雨滴落在窗户上，如泪珠。",
    "远处山峦起伏，云雾缭绕。",
    "绿草如茵，生机盎然。",
    "美味的食物让人垂涎欲滴。",
    "童年的回忆总是那么美好。",
    "她的舞姿优雅如蝴蝶飞舞。",
    "冬天的雪花轻柔地飘落。",
    "音乐在耳边轻轻流淌。",
    "植物在阳光下茁壮成长。",
    "繁星点点，夜晚格外静谧。",
    "笑声回荡在空气中，温馨无比。",
    "家乡的味道总是让人怀念。",
    "竹林间的微风轻轻吹过。",
    "小溪潺潺，流水声悦耳动听。",
    "古老的建筑诉说着历史。",
    "书页翻动间，故事渐入佳境。",
    "夜晚的灯光让城市璀璨夺目。",
    "她的声音如同清泉般悦耳。",
    "夕阳染红了整片天空。",
    "花瓣在风中翩翩起舞。",
    "一段旅程带来了新的体验。",
    "绿叶在阳光下闪烁着光泽。",
    "水面映出蓝天和白云。",
    "秋天的果实丰收在望。",
    "雨后空气清新，令人舒畅。",
    "美丽的风景让人心旷神怡。",
    "孩子的笑声是最动听的乐曲。",
    "溪水清澈，鱼儿游弋其中。",
    "清晨的阳光透过窗帘洒进来。",
    "手中的画笔描绘出梦想。",
    "阳光照耀下的花园色彩斑斓。",
    "旅行带来了无尽的快乐与回忆。",
    "书香弥漫，心灵得到滋养。",
    "茶香四溢，令人放松身心。",
    "漫步在小径上，感受大自然。",
    "她的目光如星空般深邃。",
    "生活如同一场精彩的演出。",
    "残阳如血，映照着大地。",
    "春风拂面，心情格外愉悦。",
    "小猫在阳光下懒洋洋地睡觉。",
    "蜜蜂在花间忙碌地采蜜。",
    "雪山巍峨，气势磅礴。",
    "短暂的相聚却温暖人心。",
    "翠绿的田野仿佛无尽延伸。",
    "时光荏苒，岁月如歌。",
    "灯下的影子宛如舞者。",
    "书页之间夹着童年的梦想。",
    "烛光摇曳，气氛宁静而温馨。",
    "远足时的欢声笑语回荡。",
    "月光洒在大地上，如梦似幻。",
    "童话般的场景让人心醉。",
    "生活中的点滴皆是风景。",
    "一朵花开的瞬间是奇迹。",
    "窗外的鸟儿在欢快歌唱。",
    "听雨声，心如止水，宁静。",
    "她的眼睛里藏着星辰大海。",
    "童年时光如同沙漏，流逝。",
    "一杯咖啡唤醒了沉睡的心情。",
    "阳光透过树叶，洒下斑驳光影。",
    "每一次相遇都是缘分的安排。",
    "空气中弥漫着花香的气息。",
    "翻开书本，故事开始了。",
    "森林深处传来动物的低鸣。",
    "一场春雨滋润了万物复苏。",
    "红叶随风飘落，秋意浓浓。",
    "她的笑容如花般绚丽。",
    "小鸟在枝头欢快地鸣叫。",
    "温暖的阳光照亮了前方。",
    "凝视远方，心中充满期待。",
    "每一天都是新的开始。",
    "夕阳映照，岁月如歌。",
    "绿野仙踪，充满无限可能。",
    "手握梦想，勇敢前行。",
    "青春的旋律在心中回响。",
    "柔风轻拂，吹散烦恼。",
    "生活如画，色彩斑斓。",
    "在书中找到属于自己的故事。",
    "云朵漂浮，像是在讲故事。",
    "笑容是最好的语言。",
    "一颗心与大自然相连。",
    "漫步在沙滩，感受海浪。",
    "漫天星斗，让人沉醉。",
    "回忆是一道温暖的光。",
    "每一次呼吸都是生活的礼赞。",
    "大自然的声音让人安静。",
    "雨后阳光洒下，万物复苏。",
    "清风拂面，心情格外畅快。",
    "美丽的瞬间总是让人感动。",
    "一曲动人的旋律唤起记忆。",
    "生活的细节充满温暖。",
    "在阳光下奔跑，心自由飞翔。",
    "亲情如水，绵延不绝。",
]

def embedding_text(inputText):
    client = ZhipuAI(api_key=os.getenv('ZHIPU_API_KEY')) 
    response = client.embeddings.create(
        model="embedding-3", #填写需要调用的模型编码
        input=inputText,
    )
    return response.data
 
   
def conine_distane(a, b):
    """
    计算两个向量之间的余弦相似度
    """
    
    return np.dot(a, b) / (np.linalg.norm(a) * (np.linalg.norm(b)))


def search_by_word(d, search_key, top_n=5):
    """
    根据指定的关键词（句子），去向量空间中进行相似搜索
    """
    # 关键词向量化
    searchKey_embedding = embedding_text(search_key)[0].embedding

    # 计算相似度
    d['embedding'] = d['embedding'].apply(lambda x: np.array(json.loads(x)))  # 解析字符串为数组
    d['similarity'] = d['embedding'].apply(lambda x: conine_distane(searchKey_embedding, x))

    # 按相似度排序
    sorted_df = d.sort_values(by='similarity', ascending=False)

    # 返回前n个最相似的句子
    return sorted_df.head(top_n)



file_path = 'embeddings.csv'

# 判断文件是否存在
if os.path.exists(file_path):
    print(f"{file_path} 文件存在")
else:
    print(f"{file_path} 文件不存在")
    # 提取embedding字段和它的长度
    originText = text
    embeddings = [item.embedding for item in embedding_text(text)]  # 根据你的数据结构修改
    lengths = [len(embedding) for embedding in embeddings]  # 计算每个embedding的长度


    # # 创建DataFrame
    df = pd.DataFrame({
        'originText': originText,
        'embedding': embeddings,
        'length': lengths
    })

    # # 写入CSV文件
    df.to_csv(file_path, index=False)

# 相似度搜索
dddddd = pd.read_csv(file_path)

print(search_by_word(dddddd, ['音乐']))