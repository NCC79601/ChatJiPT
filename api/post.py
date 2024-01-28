import requests
import json

knowledge_base_chat_url = "http://localhost:7862/chat/knowledge_base_chat"

chat_url = "http://localhost:7862/chat/chat"

headers = {"Content-Type": "application/json"}

def post(query, history=[]):

    data = {
        "query": query,
        "knowledge_base_name": "thu-knowledge",
        "top_k": 3,
        "score_threshold": 0.8,
        "history": history,
        "stream": False,
        "model_name": "chatglm3-6b",
        "temperature": 0.2,
        "max_tokens": 0,
        "prompt_name": "ChatJiPT"
    }

    response = requests.post(knowledge_base_chat_url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        response_data = json.loads(response.text[6:]) # 过滤掉开头的 "data: " 字符串
        # 处理响应数据
        print(f'response: {response_data["answer"]}')
        return response_data
    else:
        print("请求失败:", response.status_code)
    return None

def post_raw(query, history=[]):

    data = {
        "query": query,
        "history": history,
        "stream": False,
        "model_name": "chatglm3-6b",
        "temperature": 0.2,
        "max_tokens": 0,
        "prompt_name": "default"
    }

    response = requests.post(chat_url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        response_data = json.loads(response.text[6:]) # 过滤掉开头的 "data: " 字符串
        # 处理响应数据
        # print(f'response: {response_data}')
        return response_data
    else:
        print("请求失败:", response.status_code)
    return None