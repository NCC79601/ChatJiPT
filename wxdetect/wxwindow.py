import cv2
import numpy as np
from PIL import Image
import pyautogui
import pyperclip
from tracker import PositionTracker, ClickTracker
from rapidocr_onnxruntime import RapidOCR
import os
from input_converter import InputConverter

current_path = os.path.dirname(os.path.abspath(__file__))

class WXWindow:

    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.least_ratio = 1 / 5
        self.click_tracker = ClickTracker()
    

    def get_window(self, debug_output=False):
        print('recognizing window...')
        
        # 获取截图，找到微信窗口并切分各个部分
        self.position_tracker = PositionTracker()

        img = pyautogui.screenshot()
        print(f'screenshot size: ({img.size[1]}, {img.size[0]})')
        img = np.array(img.getdata(), np.uint8).reshape(img.size[1], img.size[0], 3)
        self.img = img

        # 微信左侧边栏颜色
        sb_color = np.array([0x2E, 0x2E, 0x2E])
        # 消息列表选中颜色
        ml_select_color_upper_bound = np.array([0xC9,0xC9, 0xC9])
        ml_select_color_lower_bound = np.array([0xC4,0xC4, 0xC4])

        # 标记出微信左侧边栏的区域
        img_mask = np.zeros_like(img)
        img_mask[(img == sb_color).all(axis=-1)] = [255, 255, 255]

        gray_img = cv2.cvtColor(img_mask, cv2.COLOR_BGR2GRAY)
        contours, _ = cv2.findContours(gray_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        largest_contour = max(contours, key=cv2.contourArea)
        sb_x, sb_y, sb_w, sb_h = cv2.boundingRect(largest_contour)
        
        self.unit = sb_w / 54

        self.position_tracker.add_ref("window_origin", sb_x, sb_y)

        if debug_output:
            print(f'左侧边栏区域 xywh：({sb_x}, {sb_y}, {sb_w}, {sb_h})')

        marked_img = img.copy()
        cv2.rectangle(marked_img, \
                    (sb_x, sb_y), \
                    (sb_x + sb_w, sb_y + sb_h), \
                    (255, 0, 0), thickness=1)

        # 标记出选中的聊天
        img_mask = np.zeros_like(img)
        img_mask[(img >= ml_select_color_lower_bound).all(axis=-1) & (img <= ml_select_color_upper_bound).all(axis=-1)] = [255, 255, 255]

        gray_img = cv2.cvtColor(img_mask, cv2.COLOR_BGR2GRAY)
        contours, _ = cv2.findContours(gray_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        largest_contour = max(contours, key=cv2.contourArea)
        ml_select_x, ml_select_y, ml_select_w, ml_select_h = cv2.boundingRect(largest_contour)
        
        # 计算消息列表位置
        ml_select_y_new = int(self.unit * 61) + sb_y
        ml_select_index = int((ml_select_y - ml_select_y_new) / ml_select_h)
        ml_y_bias = (ml_select_y - ml_select_y_new) % ml_select_h
        ml_select_y = ml_select_y_new + ml_y_bias

        if debug_output:
            print(f'消息列表 xywh：({ml_select_x}, {ml_select_y}, {ml_select_w}, {ml_select_h})')

        msglist_num = (sb_y + sb_h - ml_select_y) // ml_select_h
        if debug_output:
            print(f'消息列表数量：{msglist_num}')

        msglist_rois = []
        for i in range(msglist_num):
            if ml_select_y + (i + 1) * ml_select_h > sb_y + sb_h:
                break
            msglist_rois.append((ml_select_x, ml_select_y + i * ml_select_h, ml_select_w, ml_select_h))

        self.position_tracker.add_ref("msglist_origin", *msglist_rois[0][0:2])

        for i in range(msglist_num):
            roi = msglist_rois[i]
            if (i == ml_select_index):
                cv2.rectangle(marked_img, \
                        (roi[0], roi[1]), \
                        (roi[0] + roi[2], roi[1] + roi[3]), \
                        (0, 255, 0), thickness=2)
            else:
                cv2.rectangle(marked_img, \
                        (roi[0], roi[1]), \
                        (roi[0] + roi[2], roi[1] + roi[3]), \
                        (0, 255, 0), thickness=1)

        img_gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)       
        img_pyramid = [img_gray]

        # 加载微信右上角四大金刚按钮的照片 (1080p, 1440p)，进行模式识别
        templates = []
        templates.append(cv2.imread('./wxdetect/pattern/top_right_pattern_1080p.png', 0))
        templates.append(cv2.imread('./wxdetect/pattern/top_right_pattern_1440p.png', 0))

        rt_xywh = None

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
                    # 画出识别到的区域
                    if rt_xywh == None:
                        rt_xywh = (pt[0]*scale, pt[1]*scale, w*scale, h*scale)
                    cv2.rectangle(marked_img, (pt[0]*scale, pt[1]*scale), ((pt[0] + w)*scale, (pt[1] + h)*scale), (255, 0, 0), 2)
            
            if rt_xywh != None:
                break

        if rt_xywh == None:
            print('未寻找到微信右上角四大金刚按钮，退出')
            exit(1)

        rt_x = rt_xywh[0] + rt_xywh[2]
        rt_y = rt_xywh[1] # + rt_xywh[3]
        cv2.circle(marked_img, (rt_x, rt_y), radius=5, color=(0, 255, 255), thickness=-1)

        # 计算窗口大小
        self.x = sb_x
        self.y = sb_y
        self.w = rt_x - sb_x
        self.h = sb_h

        # 加载 chatbox 工具栏的照片 (1080p, 1440p)，进行模式识别
        templates = []
        templates.append(cv2.imread('./wxdetect/pattern/chatbox_toolbar_1080p.png', 0))
        templates.append(cv2.imread('./wxdetect/pattern/chatbox_toolbar_1440p.png', 0))

        cb_tb_xywh = None

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
                    # 画出识别到的区域
                    if cb_tb_xywh == None:
                        cb_tb_xywh = (pt[0]*scale, pt[1]*scale, w*scale, h*scale)
                    cv2.rectangle(marked_img, (pt[0]*scale, pt[1]*scale), ((pt[0] + w)*scale, (pt[1] + h)*scale), (255, 0, 0), 2)
            
            if cb_tb_xywh != None:
                break

        
        # 截取消息列表的图片
        msglist_img = img[msglist_rois[0][1]:sb_y+sb_h, ml_select_x:ml_select_x+ml_select_w]
        self.msglist_img = msglist_img

        # 计算 chatbox 大小
        cb_x = cb_tb_xywh[0]
        cb_y = cb_tb_xywh[1]
        cb_w = self.x + self.w - cb_x
        self.cb_x = cb_x
        self.cb_y = cb_y
        self.cb_w = cb_w

        self.position_tracker.add_ref("chatbox_inputbox_origin", cb_x, cb_y)
    
    
        # 获取窗口图像
        window_img = img[self.y:self.y+self.h, self.x:self.x+self.w].copy()
        l_bound = sb_w + ml_select_w
        b_bound = sb_h - (self.y + self.h - cb_y)

        # 获取chatbox图像
        chatbox_img = window_img[:b_bound, l_bound:]
        self.chatbox_img = chatbox_img

        # 自己发送的最后一条消息
        last_msg_from_me_detect_x = chatbox_img.shape[1] - 1 - int(self.unit * (34 + 30 + 10 + 5))
        msg_from_me_color = np.array([0x95, 0xEC, 0x69])
        last_msg_from_me_detect_y = int(61 * self.unit)

        for i in range(chatbox_img.shape[0] - 1, int(self.unit * (60-1)), -1):
            if (chatbox_img[i, last_msg_from_me_detect_x] == msg_from_me_color).all():
                last_msg_from_me_detect_y = i
                if debug_output:
                    print(f'detected: {last_msg_from_me_detect_y}')
                break

        chatbox_content_img = chatbox_img[last_msg_from_me_detect_y:, :]
        chatbox_content_img[-1, :] = [0xF5, 0xF5, 0xF5]
        pad = int(max(10, chatbox_content_img.shape[1] * self.least_ratio - chatbox_content_img.shape[0]))
        chatbox_content_img = np.concatenate((chatbox_content_img, np.full((pad, chatbox_content_img.shape[1], 3), 0xF5, dtype=np.uint8)), axis=0)
        self.chatbox_content_img = chatbox_content_img

        # 对方发送的最后一条消息
        last_msg_from_ta_detect_x = int(self.unit * (1 + (34 + 30 + 10 + 5)))
        msg_from_ta_color = np.array([0xF5, 0xF5, 0xF5])
        last_msg_from_ta_detect_y = int(self.unit * 61)

        precolor = msg_from_ta_color
        detect_cnt = 0

        for i in range(chatbox_img.shape[0] - 1, int(self.unit * (60-1)), -1):
            if (chatbox_img[i, last_msg_from_ta_detect_x] != precolor).all():
                detect_cnt += 1
                precolor = chatbox_img[i, last_msg_from_ta_detect_x]

            if detect_cnt == 2:
                last_msg_from_ta_detect_y = i
                if debug_output:
                    print(f'detected: {last_msg_from_ta_detect_y}')
                break

        if last_msg_from_ta_detect_y > int(self.unit * (61 + 25)):
            last_msg_from_ta_detect_y -= int(self.unit * (25))

        name_roi = (last_msg_from_ta_detect_y, int(self.unit * 70), int(self.unit * 24), int(self.unit * 200))
        name_img = chatbox_img[name_roi[0]:name_roi[0]+name_roi[2], name_roi[1]:name_roi[1]+name_roi[3]]
        name_img[0:1, ...] = [0xF5, 0xF5, 0xF5]
        pad = int(max(10, name_img.shape[1] * self.least_ratio - name_img.shape[0]))
        padding = np.ones((pad, name_img.shape[1], name_img.shape[2]), dtype=np.uint8) * 0xF5
        name_img = np.concatenate((name_img, padding), axis=0)
        self.name_img = name_img

        chatbox_title_img = chatbox_img[2:61, :-200]
        pad = int(max(10, chatbox_title_img.shape[1] * self.least_ratio - chatbox_title_img.shape[0]))
        padding = np.ones((pad, chatbox_title_img.shape[1], chatbox_title_img.shape[2]), dtype=np.uint8) * 0xF5
        chatbox_title_img = np.concatenate((chatbox_title_img, padding), axis=0)
        self.chatbox_title_img = chatbox_title_img
    

    def get_bubbles(self, debug_output=False):
        # 定义颜色范围（这里是红色，可以根据需要进行调整）
        lower_red = np.uint8([0xFA, 0x51, 0x51])
        upper_red = np.uint8([0xFA, 0x51, 0x51])

        # 创建掩模
        mask = cv2.inRange(self.msglist_img, lower_red, upper_red)
        mask = cv2.dilate(mask, None, iterations=2)
        mask = cv2.erode(mask, None, iterations=2)

        Image.fromarray(mask)

        # Hough 变换检测圆形
        unread_bubbles = cv2.HoughCircles(
            mask,                   # 输入图像
            cv2.HOUGH_GRADIENT,     # 使用基于梯度的霍夫变换
            dp=1,                   # 图像分辨率的倒数，例如，如果dp=1，分辨率相同；如果dp=2，分辨率减半
            minDist=20,             # 圆心之间的最小距离
            param1=50,              # Canny边缘检测的高阈值
            param2=10,              # 累加器阈值，值越小，检测到的圆越多
            minRadius=5,            # 圆的最小半径
            maxRadius=30            # 圆的最大半径
        )

        if debug_output:
            print(f'unread_bubbles: {unread_bubbles}')

        # 画出检测到的圆形
        bubble_img = self.msglist_img.copy()
        if unread_bubbles is not None:
            unread_bubbles = np.round(unread_bubbles[0, :]).astype("int")
            for (x, y, r) in unread_bubbles:
                cv2.circle(bubble_img, (x, y), r + 2, (0, 255, 255), 2)
        self.bubble_img = bubble_img
        self.unread_bubbles = unread_bubbles
        return unread_bubbles


    def click_latest_bubble(self):
        if self.unread_bubbles is None:
            print('no unread bubble')
            return
        target_pos = self.position_tracker.get_abs_pos("msglist_origin", *self.unread_bubbles[0][0:2])
        self.click_tracker.add_point(*target_pos)
        pyautogui.moveTo(*target_pos, duration=0.3)
        pyautogui.click(*target_pos, button='left')


    def get_current_chatbox_content(self, debug_output=False):
        print('using OCR to get current chatbox content...')
        engine = RapidOCR()  # Initialize RapidOCR
        title_ocr_result = engine(self.chatbox_title_img)
        content_ocr_result = engine(self.chatbox_content_img)
        nickname_ocr_result = engine(self.name_img)

        def judge_empty(ocr_result):
            if ocr_result == None or ocr_result[0] == None or len(ocr_result[0]) == 0:
                return True
            return False

        if judge_empty(nickname_ocr_result):
            # print(f'-> 未检测到昵称，判断为单聊')
            is_group_chat = False
        else:
            # print(f'-> 检测到昵称，判断为群聊')
            is_group_chat = True

        chatbox_title = ""
        for line in title_ocr_result[0]:
            # print(line[1])
            chatbox_title += line[1]

        import re
        def is_time_format(s):
            return bool(re.match(r'^\d{1,2}:\d{2}$', s))

        new_msg_content = ""

        if judge_empty(content_ocr_result):
            print(f'[WARNING] 未检测到新消息')
        else:
            for line in content_ocr_result[0]:
                if line[1] == '以下是新消息' or is_time_format(line[1]):
                    continue
                new_msg_content += line[1] + '\n'
        if debug_output:
            print("-"*5, "新消息内容", "-"*5)
            print(new_msg_content)

        return {
            "who": chatbox_title,
            "new_msg": new_msg_content,
            "is_group_chat": is_group_chat
        }

    def send_message(self, message, press_enter=False):
        # pyperclip.copy(message)

        target_pos = self.position_tracker.get_abs_pos("chatbox_inputbox_origin", int(self.unit * 50), int(self.unit * 50))
        self.click_tracker.add_point(*target_pos)
        pyautogui.moveTo(*target_pos, duration=0.3)
        pyautogui.click(*target_pos, button='left')
        # pyautogui.hotkey('ctrl', 'v')

        input_converter = InputConverter()
        input_converter.perform_type(message, interval=0.05, chunk_size=20)

        if press_enter:
            pyautogui.press('enter')