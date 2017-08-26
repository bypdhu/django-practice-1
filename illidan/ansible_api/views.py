# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser

from .execute_ansible import ExecuteAnsible


@csrf_exempt
def ansible_command(request):
    if request.method == 'POST':
        print(request)
        print(request.body)
        try:
            data = JSONParser().parse(request)
            print(data)
        except ParseError, e:
            print(e)
            return JsonResponse("body has no json", safe=False, status=status.HTTP_400_BAD_REQUEST)

        # run ansible command

        ansible_exe = ExecuteAnsible(data)

        res = ansible_exe.run_command()

        print(res)

        return JsonResponse(res, safe=False, status=status.HTTP_201_CREATED)
