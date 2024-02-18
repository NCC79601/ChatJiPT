import time
import uiautomation as auto
import pyautogui
import pyperclip
import requests
from bs4 import BeautifulSoup

def get_content(ui_response_time=1):
    '''
    自动使获取链接，然后获取html内容
    '''

    root = auto.GetRootControl()
    success = None

    # 点进链接
    for control in root.GetChildren():
        if control.Name == '微信':
            for child_depth2 in control.GetChildren():
                if child_depth2.ClassName == 'CMenuWnd':
                    print('CMenuWnd found')
                    for child_depth3 in child_depth2.GetChildren():
                        for child_depth4 in child_depth3.GetChildren():
                            for child_depth5 in child_depth4.GetChildren():
                                if child_depth5.Name == "用默认浏览器打开":
                                    child_depth5.Click()
                                    success = True
                                    break
                        if success:
                            break
                    break
            break

    time.sleep(ui_response_time)

    if not success:
        print('Failed to get link url')
        return None

    pyautogui.press('f6')
    time.sleep(ui_response_time)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(ui_response_time)
    pyautogui.press('f6')

    time.sleep(ui_response_time)

    pyautogui.hotkey('alt', 'f4')

    url = pyperclip.paste()
    print(f'url get: {url}')
    if 'mp.weixin.qq.com' not in url:
        print('url not allowed!')
        return None

    response = requests.get(url)
    html_document = response.text

    soup = BeautifulSoup(html_document, 'html.parser')
    page_content = soup.find(id='page-content')

    if page_content:
        page_content_text = '\n'.join(block for block in page_content.stripped_strings)
        lines = page_content_text.split('\n')
        for line in lines:
            if line.strip() == '':
                lines.remove(line)
        lines_cleaned = [line.lstrip() for line in lines]
        page_content_text_cleaned = '\n'.join(lines_cleaned)
        print(page_content_text_cleaned)
        
    else:
        print("Element with id 'page-content' not found in the HTML document.")
        return None

    return page_content_text_cleaned