from .feedback import FeedbackCommand
from .clear import ClearCommand

def detect_and_execute(query, history):
    '''
    判断query是哪个命令
    :param query: str, 用户输入
    :param history: list, 聊天历史信息
    :return: bool, 是否是命令；str, 命令执行结果
    '''
    commands = [FeedbackCommand(), ClearCommand()]
    for command in commands:
        if command.detect(query):
            return True, command.execute(query=query, history=history), command.command_name
    return False, None, None