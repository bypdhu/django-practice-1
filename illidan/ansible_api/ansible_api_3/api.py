#!/usr/bin/env python
# coding: utf-8

from __future__ import (absolute_import, division, print_function)

from collections import namedtuple

from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.parsing.splitter import parse_kv
from ansible.playbook import Play
from ansible.utils.vars import load_extra_vars, load_options_vars
from ansible.vars import VariableManager

from ansible_wrapper import CallbackWrap

__metaclass__ = type


class Api(object):
    def __init__(self, **kwargs):
        self.Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts',
                                              'syntax', 'connection', 'module_path', 'forks', 'remote_user',
                                              'private_key_file', 'ssh_common_args', 'ssh_extra_args',
                                              'sftp_extra_args', 'scp_extra_args', 'become', 'become_method',
                                              'become_user', 'verbosity', 'check',
                                              'extra_vars', 'inventory', 'module_name', 'module_args',
                                              'name', 'pattern'])
        self.pb_options = self.Options(listtags=kwargs.get('listtags', False),
                                       listtasks=kwargs.get('listtasks', False),
                                       listhosts=kwargs.get('listhosts', False),
                                       syntax=kwargs.get('syntax', False),
                                       connection=kwargs.get('connection', 'ssh'),
                                       module_path=kwargs.get('module_path', None),
                                       forks=kwargs.get('forks', 100),
                                       remote_user=kwargs.get('remote_user', 'ansible'),
                                       private_key_file=kwargs.get('private_key_file', None),
                                       ssh_common_args=kwargs.get('ssh_common_args', None),
                                       ssh_extra_args=kwargs.get('ssh_extra_args', None),
                                       sftp_extra_args=kwargs.get('sftp_extra_args', False),
                                       scp_extra_args=kwargs.get('scp_extra_args', False),
                                       become=kwargs.get('become', False),
                                       become_method=kwargs.get('become_method', 'sudo'),
                                       become_user=kwargs.get('become_user', 'root'),
                                       verbosity=kwargs.get('listtags', None),
                                       check=kwargs.get('check', False),
                                       extra_vars=kwargs.get('extra_vars', None),
                                       inventory=kwargs.get('inventory', "localhost"),
                                       module_name=kwargs.get('module_name', "command"),
                                       module_args=kwargs.get('module_args', None),
                                       name=kwargs.get('name', ''),
                                       pattern=kwargs.get('pattern', 'all'),
                                       )
        

    def _play_ds(self, name, pattern):
        check_raw = self.pb_options.module_name in ('command', 'win_command', 'shell', 'win_shell', 'script', 'raw')
        return dict(
            name=name,
            hosts=pattern,
            gather_facts='no',
            tasks=[dict(action=dict(module=self.pb_options.module_name,
                                    args=parse_kv(self.pb_options.module_args, check_raw=check_raw)))]
        )

    def run_cmd(self):

        passwords = {}

        loader = DataLoader()

        variable_manager = VariableManager()
        variable_manager.extra_vars = load_extra_vars(loader=loader, options=self.pb_options)
        variable_manager.options_vars = load_options_vars(self.pb_options)

        inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=self.pb_options.inventory)
        variable_manager.set_inventory(inventory)

        play_ds = self._play_ds(self.pb_options.name, self.pb_options.pattern)
        play = Play().load(play_ds, variable_manager=variable_manager, loader=loader)

        self._tqm = None
        try:
            self._tqm = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                options=self.pb_options,
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
