import requests
import json
import time

knowledge_base_chat_url = "http://localhost:7862/chat/knowledge_base_chat"

chat_url = "http://localhost:7862/chat/chat"

headers = {"Content-Type": "application/json"}

query = "C楼咋了"
history = []

data = {
    "query": query,
    "knowledge_base_name": "thu-knowledge",
    "top_k": 3,
    "score_threshold": 0.6,
    "history": history,
    "stream": True,
    "model_name": "chatglm3-6b",
    "temperature": 0.5,
    "max_tokens": 0,
    "prompt_name": "ChatJiPT"
}

response = requests.post(knowledge_base_chat_url, data=json.dumps(data), headers=headers, stream=True)

from autopinyin import AutoPinyin
apy = AutoPinyin(ui_respond_time=0.1, type_interval=0.01)

if response.status_code == 200:
    for line in response.iter_lines():
        # 过滤掉 keep-alive 新行
        if not line:
            continue
        decoded_line = line.decode('utf-8')
        # print(f'response: {decoded_line}')
        response_data = json.loads(decoded_line[6:]) # 过滤掉开头的 "data: " 字符串
        # 处理响应数据
        
        if "answer" not in response_data:
            continue
        print(f'{response_data["answer"]}')
        apy.auto_input(response_data["answer"])
        # return response_data
        # time.sleep(0.5)
else:
    print("请求失败:", response.status_code)