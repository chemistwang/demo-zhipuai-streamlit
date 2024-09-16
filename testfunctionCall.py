from zhipuai import ZhipuAI
import json
from utils import sendEmail, sendSMS, get_current_time, get_current_weather
import os

client = ZhipuAI(api_key=os.getenv('ZHIPU_API_KEY')) # 请填写您自己的APIKey

tools = [
        {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "用于查询现在的时间，返回现在的时间。",
             "parameters": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }
      },
      {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "用于查询城市的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "description": "城市",
                        "type": "string"
                    },
                },
                "required": ["city"]
            }
        }
      },
      {
        "type": "function",
        "function": {
            "name": "sendSMS",
            "description": "给用户发送短信",
            "parameters": {
                "type": "object",
                "properties": {
                    "user": {
                        "description": "用户",
                        "type": "string"
                    },
                    "content": {
                        "description": "短信的内容",
                        "type": "string"
                    },
                },
                "required": ["user","content"]
            }
        }
      },
      {
        "type": "function",
        "function": {
            "name": "sendEmail",
            "description": "给用户发送邮件",
            "parameters": {
                "type": "object",
                "properties": {
                    "user": {
                        "description": "用户",
                        "type": "string"
                    },
                    "content": {
                        "description": "邮件的内容",
                        "type": "string"
                    },
                },
                "required": ["user","content"]
            }
        }
      }
    ]

response = client.chat.completions.create(
    stream=True,
    model="glm-4-alltools",  # 填写需要调用的模型名称
    messages=[
        # {
        #     "role": "system",
        #     # "content": "你是一家公司的总监，需要处理日常行政工作，请用专业术语回复用户问题"
        # },
        {
            "role": "user",
            "content":[
                {
                    "type":"text",
                    # "text":"2008年奥运会在哪里举办"
                    # "text":"现在几点了"
                    # "text": "请给张三发邮件，通知他明天早上十点开会"
                    # "text": "给李四发短信，告诉他今天下午的会议延期至周五早上十点"
                    "text": "查询610113的温度"
                }
            ]
        },
        # {
        #      "role": "assistant",
        #      "content":"arguments='{\"from_year\":\"2018\",\" to_year\":\"2024\",\" type\":\"by_all\"}', name='get_tourist_data_by_year'"

        # },
    ],
    tools=tools
)

for chunk in response:
    
    # print(chunk.choices[0].delta)
    result = chunk.choices[0].delta
    # print(result)
    if result.tool_calls is None:
        print('没有调用function call', result.content)
    elif result.tool_calls[0].function.name == 'sendEmail':
        # pass
        if result.tool_calls[0].function.arguments != '':
            json_data = json.loads(result.tool_calls[0].function.arguments)
            print(json_data)
            sendEmail(json_data['user'], json_data['content'])
    elif result.tool_calls[0].function.name == 'sendSMS':
        # pass
        if result.tool_calls[0].function.arguments != '':
            json_data = json.loads(result.tool_calls[0].function.arguments)
            print(json_data)
            sendSMS(json_data['user'], json_data['content'])
    elif result.tool_calls[0].function.name == 'get_current_time':
        # pass
        get_current_time()
    elif result.tool_calls[0].function.name == 'get_current_weather':
        # pass
        if result.tool_calls[0].function.arguments != '':
            json_data = json.loads(result.tool_calls[0].function.arguments)
            print(json_data)
            get_current_weather(json_data['city'])
        
    


    # Choice(
    #     delta=ChoiceDelta(
    #         content=None, 
    #         role='tool', 
    #         tool_calls=[
    #             ChoiceDeltaToolCall(
    #                 index=None, 
    #                 id='call_b19a7c53-73e9-11ef-a132-3675ec5e04bc', 
    #                 function=ChoiceDeltaToolCallFunction(
    #                     arguments='{}\n', name='get_current_time'), type='function')]),
    #                       finish_reason='tool_calls', index=0)

    # result['tool_calls']
    
    




