#!/usr/bin/env python
# coding: utf-8

# A restful HTTP API for ansible by tornado
# Base on ansible 2.x


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from .tools import Tool

from ansible.plugins.callback import CallbackBase
from ansible.executor.task_result import TaskResult
from ansible.executor.stats import AggregateStats
from ansible.playbook.task import Task
from ansible.playbook.play import Play


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'websocket'
    CALLBACK_NEEDS_WHITELIST = True

    RC_SUCC = 0
    RC_FAIL = 1

    ITEM_STATUS = ('failed', 'changed', 'skipped', 'unreachable', 'ok')
    ITEM_STATUS_FAILED = ('failed', 'unreachable')

    def __init__(self):
        super(CallbackBase, self).__init__()
        self.current_taskname = ''
        self.std_lines = dict()

    def reset_output(self):
        self.std_lines.clear()

    def v2_on_any(self, *args, **kwargs):
        wsmsg = dict(
            msg=dict(), rc=self.RC_SUCC,
            task_name=self.current_taskname,
        )

        for crucial in args:
            if isinstance(crucial, TaskResult):
                item = self._fill_item_from_taskresult(
                    init_data=dict(
                        host=crucial._host.get_name(),
                        task_name=crucial._task.get_name(),
                        rc=self.RC_SUCC
                    ), detail=crucial._result
                )

                if self.std_lines.get(item['host']) is None:
                    self.std_lines[item['host']] = []

                self.std_lines[item['host']].append(item)
                wsmsg['rc'] = item['rc']
                wsmsg['msg'] = item
    #             TODO
    #             message.sendmsg(wsmsg, message.MSGTYPE_INFO)

            elif isinstance(crucial, Task):
                pass
            elif isinstance(crucial, Play):
                pass
            elif isinstance(crucial, AggregateStats):
                hosts = sorted(crucial.processed.keys())
                wsmsg = dict(
                    rc=self.RC_SUCC,
                    task_name=self.current_taskname,
                    msg=dict(kind='play_summarize', list=dict())
                )
                for h in hosts:
                    t = crucial.summarize(h)
                    c = 1 if t['unreachable'] or t['failures'] else 0
                    wsmsg['msg']['list'][h] = dict(
                        host=h,
                        rc=c,
                        unreachable=t['unreachable'],
                        skipped=t['skipped'],
                        ok=t['ok'],
                        changed=t['changed'],
                        failures=t['failures']
                    )
                    wsmsg['rc'] += c
    #                 TODO
    #             message.sendmsg(wsmsg, message.MSGTYPE_NOTICE)
            elif isinstance(crucial, (unicode, str)):
                wsmsg = dict(
                    rc=self.RC_SUCC,
                    task_name=self.current_taskname,
                    msg=dict(kind='desc', unique=crucial)
                )
                # TODO
                # message.sendmsg(wsmsg, message.MSGTYPE_NOTICE)
            else:
                Tool.LOGGER.warning(
                    'In result found a new type: [%s]' % (type(crucial))
                )


    def _fill_item_from_taskresult(self, init_data, detail):
        Tool.LOGGER.debug(detail)
        item = dict()
        if isinstance(init_data, dict):
            item = init_data

        if detail.get('rc'):
            item['rc'] = detail['rc']

        for s in self.ITEM_STATUS:
            if detail.get(s):
                item[s] = detail[s]
                if s in self.ITEM_STATUS_FAILED:
                    item['rc'] = self.RC_FAIL

        if detail.get('stdout'):
            item['stdout'] = detail['stdout']

        if detail.get('stderr'):
            item['stderr'] = detail['stderr']

        if detail.get('msg'):
            item['msg'] = detail['msg']

        if detail.get('invocation') and detail['invocation'].get('module_args') and detail['invocation']['module_args']\
                .get('_raw_params'):
            item['cmd'] = detail['invocation'][
                'module_args']['_raw_params']
        return item
