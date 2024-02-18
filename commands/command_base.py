class CommandBase(object):
    def __init__(self, command_name, keywords=[]):
        self.command_name = command_name
        if keywords == []:
            self.keywords = [command_name]
        else:
            self.keywords = keywords

    def detect(self, query):
        '''
        判断query是否是当前命令
        :param query: str, 用户输入
        :return: bool, 是否是当前命令
        '''
        for keyword in self.keywords:
            if query == '/' + keyword or query.startswith('/' + keyword + ' '):
                return True
        return False
    
    def execute(self, **kwargs):
        raise NotImplementedError