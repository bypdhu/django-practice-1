# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from ansible import inventory
from ansible_api import Api, ModuleRunner

# Create your tests here.

api = Api("localhost")

# inventory.HOSTS_PATTERNS_CACHE['all'] = 'all'
result = api.command("ls -alF")

print(result)

