from input_simulator import WXWindow
from frontend.wxauto import WeChat
from api.post import post
from database import database_service as db
from config import config
import datetime
import time

wx = WeChat()
wxwindow = WXWindow()
db.init()

while True:
    current_time = datetime.datetime.now()
    print("\033[92m", current_time, "\033[0m")
    
    session_list = wx.GetSessionList()
    who = None
    
    for username in session_list:
        if session_list[username] != 0:
            # 未读消息
            who = username
            break

    if who is None:
        print('No new message')
        time.sleep(5)
        continue
    
    # 打开聊天窗口
    wx.ChatWith(who)
    msgs = wx.GetAllMessage()
    # print(msgs[-1][0], msgs[-1][1])

    history = db.query(username=who)['history']
    query = msgs[-1][1]
    print('chat history:')
    print(history)
    print('current query:')
    print(query)

    print('generating response...')
    response_data = post(query=query, history=history)

    wxwindow.get_window()
    wxwindow.send_message(response_data['answer'], press_enter=True)

    history.append({
        "role": "user",
        "content": query
    })
    history.append({
        "role": "assistant",
        "content": response_data['answer']
    })

    db.update(who, {'history': history[-10:]}) # 只保留最后10个
    
    time.sleep(5)