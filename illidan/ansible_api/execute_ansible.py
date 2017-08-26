from .ansible_api import Api


class ExecuteAnsible(object):

    def __init__(self, data):
        self.data = dict(data)

    def run_command(self):
        host = Api(self.data['servers'], connection='smart')

        result = host[self.data['module_name']][self.data['module_args']]

        return result

