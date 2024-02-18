from command_base import CommandBase
import os
import datetime

class FeedbackCommand(CommandBase):
    def __init__(self):
        super(FeedbackCommand, self).__init__('feedback')

    def execute(self, **kwargs):
        '''
        用户反馈
        :param history: list, 聊天历史信息
        :return: str, 反馈结果
        '''
        history = kwargs['history']

        # 保存反馈到 feedback.txt（JSON格式）
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'feedback')
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        
        now = datetime.datetime.now()
        time_str = now.strftime('%Y-%m-%d_%H-%M-%S')

        with open(os.path.join(file_path, f'{time_str}.txt'), 'a', encoding='utf-8') as f:
            for item in history:
                if item['role'] == 'user':
                    f.write(f'用户：{item["content"]}\n')
                elif item['role'] == 'assistant':
                    f.write(f'小姬：{item["content"]}\n')
                else:
                    f.write(f'未知：{item["content"]}\n')

        return '小姬已收到反馈~'


if __name__ == '__main__':
    feedback_command = FeedbackCommand()
    print(feedback_command.execute(query='feedback', history=[{'role': 'user', 'content': 'feedback'}, {'role': 'assistant', 'content': '小姬已收到反馈~'}]))