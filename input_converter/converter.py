import pyautogui
import pyperclip

class InputConverter:

    def __init__(self):
        pass


    def convert(self, input_str, chunk_size):
        sequence = []
        copy_char = ''
        direct_char = ''
        for index in range(len(input_str)):
            char = input_str[index]

            if char.isascii():
                if copy_char != '':
                    sequence.append({
                        'type': 'copy_paste',
                        'value': copy_char
                    })
                    copy_char = ''
                
                if len(direct_char) == chunk_size - 1 or index == len(input_str) - 1:
                    direct_char += char
                    sequence.append({
                        'type': 'direct_input',
                        'value': direct_char
                    })
                    direct_char = ''
                else:
                    direct_char += char
            else:
                if direct_char != '':
                    sequence.append({
                        'type': 'copy_paste',
                        'value': direct_char
                    })
                    direct_char = ''

                if len(copy_char) == chunk_size - 1 or index == len(input_str) - 1:
                    copy_char += char
                    sequence.append({
                        'type': 'copy_paste',
                        'value': copy_char
                    })
                    copy_char = ''
                else:
                    copy_char += char
        
        return sequence


    def perform_type(self, input_str, interval=0.05, chunk_size=5, debug_output=False):
        sequence = self.convert(input_str, chunk_size=chunk_size)
        if debug_output:
            print('sequence converted: ', sequence)
        for item in sequence:
            if item['type'] == 'direct_input':
                pyautogui.typewrite(item['value'], interval=interval)
            elif item['type'] == 'copy_paste':
                pyperclip.copy(item['value'])
                pyautogui.hotkey('ctrl', 'v')
            else:
                raise Exception('Unknown type: ' + item['type'])