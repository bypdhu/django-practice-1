#!/usr/bin/env python
# coding: utf-8

from __future__ import (absolute_import, print_function, division)

from ansible.errors import AnsibleError
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.parsing.dataloader import DataLoader
from ansible.parsing.yaml.objects import AnsibleSequence

__metaclass__ = type

from ansible.plugins.callback import CallbackBase


# CallBack
class CallbackWrap(CallbackBase):
    def __init__(self):
        super(CallbackBase, self).__init__()


# Error
class AnsibleErrorWrap(AnsibleError):
    def __init__(self):
        super(AnsibleError, self).__init__()


class ModuleError(AnsibleErrorWrap):
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


class UnreachableError(AnsibleErrorWrap):
    def __init__(self, module, host):
        self.module = module
        self.host = host

    def __str__(self):
        return "{host} could not be reached when running {module}.".format(
            host=self.host,
            module=self.module
        )


class DataLoaderV2(DataLoader):

    def __init__(self, play_name):
        super(DataLoaderV2, self).__init__()
        self._playname = play_name

    def load_from_file(self, file_name):
        result = DataLoader.load_from_file(self, file_name)
        if isinstance(result, AnsibleSequence):
            for item in result:
                item['name'] = self._playname
        return result


class PlaybookExecutorV2(PlaybookExecutor):
    def __init__(self, playbooks, inventory, variable_manager, loader, options, passwords):
        self._playbooks = playbooks
        self._inventory = inventory
        self._variable_manager = variable_manager
        self._loader = loader
        self._options = options
        self.passwords = passwords
        self._unreachable_hosts = dict()

        if options.listhosts or options.listtasks or options.listtags or options.syntax:
            self._tqm = None
        else:
            self._tqm = TaskQueueManager(inventory=inventory, variable_manager=variable_manager, loader=loader,
                                         options=options, passwords=self.passwords, stdout_callback=CallbackWrap())