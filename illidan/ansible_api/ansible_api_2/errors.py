
class AnsibleApiError(Exception):
    pass

class ModuleError(AnsibleApiError):
    def __init__(self, module, host, result):
        self.module = module
        self.host = host
        self.result = result

    def __str__(self):
        output = []

        if 'msg' in self.result:
            output.append("Message: {}".format(self.result['msg']))

        if 'rc' in self.result:
            output.append("Returncode: {}".format(self.result['rc']))

        if 'stdout' in self.result:
            output.append("Stdout:\n{}".format(self.result['stdout']))

        if 'stderr' in self.result:
            output.append("Stderr:\n{}".format(self.result['stderr']))

        return "Error running '{module}' on {host}\n{output}".format(
            module=self.module,
            host=self.host,
            output='\n'.join(output)
        )


class UnreachableError(AnsibleApiError):
    def __init__(self, module, host):
        self.module = module
        self.host = host

    def __str__(self):
        return "{host} could not be reached when running {module}.".format(
            host=self.host,
            module=self.module
        )

class ErrorCode(object):
    ERRCODE_NONE = 0
    ERRCODE_SYS = 1
    ERRCODE_BIZ = 2