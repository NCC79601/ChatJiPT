from frontend.wxauto import WeChat
import time

wx = WeChat()

while True:
    msgs = wx.GetAllMessage()
    print(msgs)
    time.sleep(5)