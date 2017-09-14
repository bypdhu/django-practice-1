from ansible_api_2.core import Api


class ExecuteAnsible(object):

    def __init__(self, exec_type, data):
        self.type = exec_type
        self.data = dict(data)

    def run(self):
        if self.type == 'command':
            self.exec_command()

    def exec_command(self):
        name = self.data.get('name', 'task')
        target = self.data.get('target', '')
        module = self.data.get('module', 'command')
        args = self.data.get('args', '')
        sudo = self.data.get('sudo', False)
        forks = self.data.get('forks', 4)

        result = Api.runCmd(name, target, module, args, sudo, forks)

        return result