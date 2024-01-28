import pyautogui
import pyperclip
from pywubi import wubi

class InputConverter:
    def __init__(self):
        pass

    def convert(self, input_str, disable_wubi=False):
        sequence = []
        for char in input_str:
            wubi_char = wubi(char)
            if char.isascii():
                sequence.append({
                    'type': 'direct_input',
                    'value': char
                })
            elif wubi_char != [] and wubi_char[0] != '' and not disable_wubi:
                sequence.append({
                    'type': 'wubi',
                    'value': wubi_char[0]
                })
            else:
                sequence.append({
                    'type': 'copy_paste',
                    'value': char
                })
        return sequence

    def perform_type(self, input_str, disable_wubi=False, interval=0.05):
        sequence = self.convert(input_str, disable_wubi=disable_wubi)
        print(f'sequence: {sequence}')
        for item in sequence:
            if item['type'] == 'direct_input':
                pyautogui.press(item['value'])
            elif item['type'] == 'wubi':
                pyautogui.typewrite(item['value'], interval=interval)
                pyautogui.typewrite(' ', interval=interval)
            elif item['type'] == 'copy_paste':
                pyperclip.copy(item['value'])
                pyautogui.hotkey('ctrl', 'v')
            else:
                raise Exception('Unknown type: ' + item['type'])