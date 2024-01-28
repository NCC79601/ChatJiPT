from wxdetect import WXWindow
from api.post import post
import time
from database import database_service as db

db.init()

wx = WXWindow()

while True:
    wx.get_window()
    
    chatbox = wx.get_current_chatbox_content()
    new_msg = chatbox['new_msg']
    who = chatbox['who']

    while chatbox['new_msg'] == '':
        # No new message
        bubbles = wx.get_bubbles()
        if bubbles is None:
            print('No bubbles found')
            time.sleep(1)
            pass
        wx.click_latest_bubble()
        wx.get_window()
        chatbox = wx.get_current_chatbox_content()
        new_msg = chatbox['new_msg']
        who = chatbox['who']

    history = db.query(username=who)['history']
    print('chat history:')
    print(history)

    print('generating response...')
    response_data = post(query=chatbox['new_msg'], history=history)
    wx.send_message(response_data['answer'], press_enter=True)

    history.append({
        "role": "user",
        "content": chatbox['new_msg']
    })
    history.append({
        "role": "assistant",
        "content": response_data['answer']
    })

    db.update(who, {'history': history[-10:]}) # 只保留最后10个
