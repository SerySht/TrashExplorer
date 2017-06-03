# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from TrashExplorer.models import TrashInfo 

# Create your views here.

def home(request):
	trashs = TrashInfo.objects.all()
	context = {
		"trashs":trashs
	}
	return render(request, 'TrashExplorer/home.html', {'name':trashs})
    

def trash_deatils(request, trash_id):
	return HttpResponse("Trash"+str(trash_id))