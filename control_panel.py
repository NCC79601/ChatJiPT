import tkinter as tk
from pynput import keyboard
import subprocess
import threading
import os
from PIL import Image, ImageTk

# 创建一个窗口
root = tk.Tk()
root.title('小姬の控制面板')
root.geometry('300x300+300+300')  # 设置窗口大小和位置
root.attributes('-topmost', True)  # 设置窗口始终在最前面
root.resizable(False, False)
root.iconbitmap('img/icon.ico')

# 加载图片
image = Image.open('img/ChatJiPT.png')

# 缩放图片
image = image.resize((150, 150))  # 将图片缩放到 100x100 像素

# 将 PIL 图片对象转换为 tkinter 可用的图片对象
img = ImageTk.PhotoImage(image)

# 在窗口上添加一个标签来显示图片
label = tk.Label(root, image=img)
label.pack(pady=30)

text = tk.Label(root, text='将微信窗口完整露出来，然后再开始运行！')
text.pack(pady=10)  # 设置垂直内边距为 10 像素

# 定义一个全局变量来表示是否停止运行
stop = False

# 定义一个键盘监听器
def on_press(key):
    global stop
    try:
        if key.char == 'g':
            stop = True
            if process.poll() is None:
                process.terminate()
            button.config(state='normal', text='开始运行')
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_press)
listener.start()

# 定义一个按钮点击事件处理函数
def on_button_click():
    global process
    button.config(state='disabled', text='按G停止运行')
    process = subprocess.Popen(['python', os.path.join(os.getcwd(), 'main.py')])

# 在窗口上添加一个按钮
button = tk.Button(root, text='开始运行', command=on_button_click)
button.pack()

root.mainloop()