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
        "score_threshold": 1.0,
        "history": history,
        "stream": False,
        "model_name": "chatglm3-6b",
        "temperature": 0.7,
        "max_tokens": 0,
        "prompt_name": "ChatJiPT"
    }

    response = requests.post(knowledge_base_chat_url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        # print(f'response: {response.text}')
        response_data = json.loads(response.text[6:]) # 过滤掉开头的 "data: " 字符串
        # 处理响应数据
        print(f'response: {response_data["answer"]}')
        return response_data
    else:
        print("请求失败:", response.status_code)
    return None