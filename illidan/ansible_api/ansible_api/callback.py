from ansible.plugins.callback import CallbackBase


class SilentCallbackModule(CallbackBase):

    def __init__(self):
        self.unreachable = {}
        self.contacted = {}

    def runner_on_ok(self, host, res):
        self.contacted[host] = {
            'success': True,
            'result': res,
        }

    def runner_on_failed(self, host, res, ignore_errors=False):
        self.contacted[host] = {
            'succcess': False,
            'result': res,
        }

    def runner_on_unreachable(self, host, res):
        self.unreachable[host] = {
            'reacheable': False,
            'result': res,
        }
