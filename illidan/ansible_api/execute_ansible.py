from .ansible_api import ModuleRunner
from .ansible_api import Api


class ExecuteAnsible(object):

    def __init__(self, data):
        self.data = dict(data)

    def run_command(self):
        print(self.data)
        print("servers: " + self.data['servers'])
        host = Api(self.data['servers'], connection='smart')
        runner = ModuleRunner(self.data['module_name'])
        runner.hookup(host)
        result = runner.execute(self.data)

        print("resutl: " + result)

        return result

