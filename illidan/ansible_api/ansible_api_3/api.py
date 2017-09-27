#!/usr/bin/env python
# coding: utf-8

from __future__ import (absolute_import, division, print_function)

from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.parsing.splitter import parse_kv
from ansible.playbook import Play
from ansible.utils.vars import load_extra_vars, load_options_vars
from ansible.vars import VariableManager

from .ansible_wrapper import CallbackWrap

__metaclass__ = type


class Api(object):
    def __init__(self, **kwargs):
        self.options = kwargs
        pass

    def _play_ds(self, name, pattern):
        check_raw = self.options.module_name in ('command', 'win_command', 'shell', 'win_shell', 'script', 'raw')
        return dict(
            name = name,
            hosts = pattern,
            gather_facts = 'no',
            tasks = [ dict(action=dict(module=self.options.module_name, args=parse_kv(self.options.module_args, check_raw=check_raw))) ]
        )

    def run_cmd(self):

        passwords = {}

        loader = DataLoader()

        variable_manager = VariableManager()
        variable_manager.extra_vars = load_extra_vars(loader=loader, options=self.options)
        variable_manager.options_vars = load_options_vars(self.options)

        inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=self.options.inventory)
        variable_manager.set_inventory(inventory)

        play_ds = self._play_ds(self.options.name, self.options.pattern)
        play = Play().load(play_ds, variable_manager=variable_manager, loader=loader)

        self._tqm = None
        try:
            self._tqm = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                options=self.options,
                passwords=passwords,
                stdout_callback=CallbackWrap(),
            )

            rc = self._tqm.run(play)
            detail = self._tqm._stdout_callback.std_lines
        finally:
            if self._tqm:
                self._tqm.cleanup()
            if loader:
                loader.cleanup_all_tmp_files()

        return {'rc': rc, 'detail': detail}
