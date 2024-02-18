from command_base import CommandBase

class ClearCommand(CommandBase):
    def __init__(self):
        super(ClearCommand, self).__init__('clear')

    def execute(self, **kwargs):
        '''
        清空聊天历史
        :param history: list, 聊天历史信息
        :return: str, 反馈结果
        '''
        history = kwargs['history']
        history = []
        return '已清空聊天记录~'