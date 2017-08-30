# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from ansible_api import Api, ModuleRunner

# Create your tests here.

api = Api("localhost")
module_runner = ModuleRunner("shell")
module_runner.hookup(api)
module_runner.execute("ls", "-alF")

