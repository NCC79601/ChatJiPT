from .command_base import CommandBase
import os
import datetime

def extract_comment(s):
    words = s.split()
    if words[0].startswith('/'):
        words.pop(0)
    comment = ' '.join(words)
    return comment

class FeedbackCommand(CommandBase):
    def __init__(self):
        super(FeedbackCommand, self).__init__('feedback', keywords=['feedback', '反馈'])

    def execute(self, **kwargs):
        '''
        用户反馈
        :param query: str, 用户输入
        :param history: list, 聊天历史信息
        :return: str, 反馈结果
        '''
        query = kwargs['query']
        history = kwargs['history']

        # 保存反馈到 feedback.txt
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'feedback')
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        
        now = datetime.datetime.now()
        time_str = now.strftime('%Y-%m-%d_%H-%M-%S')

        with open(os.path.join(file_path, f'{time_str}.txt'), 'a', encoding='utf-8') as f:
            comment = extract_comment(query)
            f.write(f'用户反馈内容：{comment}\n')
            f.write('-------------------\n')
            f.write('聊天历史：\n')
            for item in history:
                if item['role'] == 'user':
                    f.write(f'用户：{item["content"]}\n')
                elif item['role'] == 'assistant':
                    f.write(f'小姬：{item["content"]}\n')
                else:
                    f.write(f'未知：{item["content"]}\n')

        return '小姬已经收到反馈啦，感谢你为我提出的宝贵意见~'


if __name__ == '__main__':
    feedback_command = FeedbackCommand()
    print(feedback_command.execute(query='/feedback this is shit', history=[{'role': 'user', 'content': 'feedback'}, {'role': 'assistant', 'content': '小姬已收到反馈~'}]))