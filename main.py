from input_simulator import WXWindow
from frontend.wxauto import WeChat
import pyautogui
from api.post import post
from autopinyin import AutoPinyin
from database import database_service as db
from config import config
import datetime
import time
from commands import detect_and_execute

wx = WeChat()
apy = AutoPinyin()
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


    wxwindow.get_window()
    # wxwindow.send_message(response_data['answer'], press_enter=True)
    wxwindow.click_input_box()

    is_command, result = detect_and_execute(query, history)

    if is_command:
        print('command detected...')
        apy.auto_input(result)
        pyautogui.press('enter')
        continue
    else:
        # apy.auto_input(response_data['answer'])
        print('generating response...')
        response_data = post(query=query, history=history, typein_function=apy.auto_input)
        pyautogui.press('enter')

        if response_data == '':
            continue
        
        history.append({
            "role": "user",
            "content": query
        })
        history.append({
            "role": "assistant",
            "content": response_data
        })

    db.update(who, {'history': history[-10:]}) # 只保留最后10个
    
    time.sleep(5)