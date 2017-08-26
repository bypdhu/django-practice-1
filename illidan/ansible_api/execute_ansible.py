from .ansible_api import Api


class ExecuteAnsible(object):

    def __init__(self, data):
        self.data = dict(data)

    def run_command(self):
        print(self.data)
        print("servers: " + self.data['servers'])
        host = Api(self.data['servers'], connection='smart')

        result = host.command(self.data['module_args'])

        return result

