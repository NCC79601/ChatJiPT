from frontend import wxauto
import random

print(f'wxauto version: {wxauto.VERSION}')

try:
    wx = wxauto.WeChat()
except wxauto.WxException as e:
    print("Error: " + e.message)
    print(e)
    exit(1)

import time

while True:
    # 在这里放置你想要循环执行的代码

    sesson_list = wx.GetSessionList()

    who = '李清雯'

    if (sesson_list[who] != 0):
        wx.ChatWith(who)
        msgs = wx.GetAllMessage(savepic=False)
        last_msg = msgs[-1]
        last_msg_content = last_msg[1]

        from post import post

        response_data = post(query=last_msg_content)
        answer = response_data["answer"]

        wx.SendMsg(answer, who=who)

    who = '文件传输助手'
    wx.ChatWith(who)

    random_number = random.randint(3000, 7000)

    print(f'Sleep for {random_number}ms')  # 输出：一个在 5000 到 10000 之间的随机整数

    time.sleep(random_number / 1000)  # 暂停5毫秒

    
