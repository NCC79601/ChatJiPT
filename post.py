import requests
import json

url = "http://localhost:7862/chat/knowledge_base_chat"  # 替换为你要发送请求的URL

headers = {"Content-Type": "application/json"}

def post(query):

    data = {
        "query": query,
        "knowledge_base_name": "thu-knowledge-new",
        "top_k": 3,
        "score_threshold": 1.0,
        "history": [],
        "stream": False,
        "model_name": "chatglm3-6b",
        "temperature": 0.7,
        "max_tokens": 0,
        "prompt_name": "ChatJiPT"
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        response_data = json.loads(response.text[6:]) # 过滤掉开头的 "data: " 字符串
        # 处理响应数据
        print(response_data["answer"])
        return response_data
    else:
        print("请求失败:", response.status_code)
    return None
