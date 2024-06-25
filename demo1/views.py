from django.shortcuts import render, redirect
from .models import Info
import json
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse

def query_by_count_index(request, count_index):
    if request.method == "GET":
        info = Info.objects.filter(unsigned_message_count = count_index)
        if len(info) != 0:
            result = serialize("json", info)
            return HttpResponse(result, content_type = 'application/json')
    dict = [
    ]
    return HttpResponse(json.dumps(dict), content_type = 'application/json')

def query_all(request):
    if request.method == "GET":
        info = Info.objects.all()
        if len(info) != 0:
            result = serialize("json", info)
            return HttpResponse(result, content_type = 'application/json')
    dict = [
    ]
    return HttpResponse(json.dumps(dict), content_type = 'application/json')
    
def home_page(request):
    dict = [
        {'id': 1, 'name': 'Ana'},
        {'id': 2, 'name': 'Bill'},
    ]
    return HttpResponse(json.dumps(dict), content_type = 'application/json')
