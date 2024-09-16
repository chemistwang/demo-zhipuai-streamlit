from zhipuai import ZhipuAI
import json
from utils import sendEmail, sendSMS, get_current_time, get_current_weather
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

client = ZhipuAI(api_key=os.getenv('ZHIPU_API_KEY')) # 请填写您自己的APIKey


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.chat_history.append({
        "role": "system",
        "content": "你是一家公司的总监，需要处理日常行政工作，请用专业术语回复用户问题"
    })
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": "我是你的AI小助手"
    })


st.set_page_config(page_title="AI小助手", page_icon=":robot:")
st.title('AI小助手')


for message in st.session_state.chat_history:
    if message['role'] == 'user':
        with st.chat_message("user"):
            st.markdown(message['content'])
    if message['role'] == 'assistant':
        with st.chat_message("assistant"):
            st.markdown(message['content'])


userQuery = st.chat_input('请输入您的问题')
if userQuery is not None and userQuery.strip() != "":
    st.session_state.chat_history.append({
        "role": "user",
        "content": userQuery
    })
    with st.chat_message("user"):
        st.markdown(userQuery)

    
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
        messages=st.session_state.chat_history,
        tools=tools
    )

    # 流式输出
    def stream_data(qianwenRes):
        final_content = ''
        for chunk in qianwenRes:
            
            # print(chunk.choices[0].delta)
            result = chunk.choices[0].delta
            # print(result)
            if result.tool_calls is None:
                print('没有调用function call', result.content)
                if result.content:
                    final_content += result.content
                    yield result.content
            elif result.tool_calls[0].function.name == 'sendEmail':
                # pass
                if result.tool_calls[0].function.arguments != '':
                    json_data = json.loads(result.tool_calls[0].function.arguments)
                    print(json_data)
                    res = sendEmail(json_data['user'], json_data['content'])
                    if res:
                        final_content += res
                        yield res
            elif result.tool_calls[0].function.name == 'sendSMS':
                # pass
                if result.tool_calls[0].function.arguments != '':
                    json_data = json.loads(result.tool_calls[0].function.arguments)
                    print(json_data)
                    res = sendSMS(json_data['user'], json_data['content'])
                    if res:
                        final_content += res
                        yield res
            elif result.tool_calls[0].function.name == 'get_current_time':
                # pass
                res = get_current_time()
                if res:
                        final_content += res
                        yield res
            elif result.tool_calls[0].function.name == 'get_current_weather':
                # pass
                if result.tool_calls[0].function.arguments != '':
                    json_data = json.loads(result.tool_calls[0].function.arguments)
                    print(json_data)
                    res = get_current_weather(json_data['city'])
                    if res:
                        final_content += res
                        yield res
        return final_content
     
    with st.chat_message("assistant"):
        # st.markdown(final_content)
        final_content = st.write_stream(stream_data(response))
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": final_content
        })


    # Choice(
    #     delta=ChoiceDelta(
    #         content=None, 
    #         role='tool', 
    #         tool_calls=[
    #             ChoiceDeltaToolCall(
    #                 index=None, 
    #                 id='call_b19a7c53-73e9-11ef-a132-3675ec5e04bc', 
    #                 function=ChoiceDeltaToolCallFunction(
    #                     arguments='{}\n', 
    #                     name='get_current_time'), 
    #                     type='function')]),
    #                  finish_reason='tool_calls', 
    #                  index=0)

    # result['tool_calls']

