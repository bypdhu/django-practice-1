#!/usr/bin/env python
# coding: utf-8

# A restful HTTP API for ansible by tornado
# Base on ansible 2.x


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

__all__ = ['Config']


class Config(object):

    host = '127.0.0.1'
    port = 8765
    sign_key = 'YOUR_SIGNATURE_KEY_HERE'
    log_path = '/var/log/ansible-api.log'
    allow_ip = []
    thread_pool_size = 4

    dir_script = ''
    dir_playbook = ''
    dir_authkeys = ''

    def __init__(self):
        cfg_path = '/etc/ansible/api.cfg'
        cf = ConfigParser.ConfigParser()
        cf.read(cfg_path)
        try:
            cf.options('default')
        except:
            pass
        else:
            if cf.has_option('default', 'host'):
                self.host = cf.get('default', 'host')
            if cf.has_option('default', 'port'):
                self.port = cf.get('default', 'port')
            if cf.has_option('default', 'sign_key'):
                self.sign_key = cf.get('default', 'sign_key')
            if cf.has_option('default', 'log_path'):
                self.log_path = cf.get('default', 'log_path')
            if cf.has_option('default', 'allow_ip'):
                self.allow_ip = cf.get('default', 'allow_ip').split()
            if cf.has_option('default', 'thread_pool_size'):
                self.thread_pool_size = cf.get('default', 'thread_pool_size')
        try:
            cf.options('directory')
        except:
            pass
        else:
            if cf.has_option('directory', 'script'):
                self.dir_script = cf.get('directory', 'script')
            if cf.has_option('directory', 'playbook'):
                self.dir_playbook = cf.get('directory', 'playbook')
            if cf.has_option('directory', 'authkeys'):
                self.dir_authkeys = cf.get('directory', 'authkeys')

    @staticmethod
    def Get(attr):
        cfg = Config()
        return getattr(cfg, attr, '')