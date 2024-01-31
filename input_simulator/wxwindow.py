import cv2
import numpy as np
import pyautogui
import os
from .converter import InputConverter
from colorama import Fore, Style

current_path = os.path.dirname(os.path.abspath(__file__))

class WXWindow:

    def __init__(self):
        pass


    def get_window(self, debug_output=False):
        print('recognizing window...')
        
        # 获取截图
        img = pyautogui.screenshot()
        print(f'screenshot size: ({img.size[1]}, {img.size[0]})')
        img = np.array(img.getdata(), np.uint8).reshape(img.size[1], img.size[0], 3)
        self.img = img

        img_gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)       
        img_pyramid = [img_gray]

        # 加载 chatbox 工具栏的照片 (1080p, 1440p)，进行模式识别
        templates = []
        templates.append(cv2.imread(os.path.join(current_path, 'pattern/chatbox_toolbar_1080p.png'), 0))
        templates.append(cv2.imread(os.path.join(current_path, 'pattern/chatbox_toolbar_1440p.png'), 0))

        cb_tb_xywh = None # ChatBox ToolBar

        for template in templates:
            w, h = template.shape[::-1]

            # 创建模式图像金字塔，以 0.5 的比例逐级缩小
            template_pyramid = [template]
            for i in range(2):
                template_pyramid.append(cv2.pyrDown(template_pyramid[-1]))

            # 逐级进行模式识别
            for i, (p, t) in enumerate(zip(img_pyramid, template_pyramid)):
                res = cv2.matchTemplate(p, t, cv2.TM_CCOEFF_NORMED)
                threshold = 0.7
                loc = np.where(res >= threshold)
                for pt in zip(*loc[::-1]):
                    scale = 2 ** i
                    if cb_tb_xywh == None:
                        cb_tb_xywh = (pt[0]*scale, pt[1]*scale, w*scale, h*scale)
            
            if cb_tb_xywh != None:
                break
        
        if cb_tb_xywh == None:
            print(Fore.RED + 'chatbox toolbar not found!' + Style.RESET_ALL)
            exit(0)
        
        cb_tb_x = cb_tb_xywh[0]
        cb_tb_y = cb_tb_xywh[1]
        cb_tb_w = cb_tb_xywh[2]
        cb_tb_h = cb_tb_xywh[3]

        self.click_target = (int(cb_tb_x + cb_tb_w * 1.25), cb_tb_y + cb_tb_h * 2)

    

    def click_input_box(self):
        click_target = self.click_target
        pyautogui.moveTo(*click_target, duration=0.3)
        pyautogui.click(*click_target, button='left')


    def send_message(self, message, press_enter=False):
        self.click_input_box()

        input_converter = InputConverter()
        input_converter.perform_type(message, interval=0.05, chunk_size=20, debug_output=True)

        if press_enter:
            pyautogui.press('enter')