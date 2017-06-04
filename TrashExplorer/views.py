# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404
from .models import TrashInfo 


def home(request):
	trashes = TrashInfo.objects.all()
	return render(request, 'TrashExplorer/home.html', {"trashes":trashes})
    

def trash_deatils(request, trash_name):
	try:
		trash = TrashInfo.objects.get(trash_name = trash_name)
	except TrashInfo.DoesNotExist:
		raise Http404(trash_name + " does not exist")
	return render(request, 'TrashExplorer/detail.html', {"trash":trash.trash_name})
