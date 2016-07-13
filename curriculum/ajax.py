
import json
from django.shortcuts import render
from django.http import HttpResponse
from curriculum.models import *
from curriculum.helpers import *
from django.contrib.auth.models import User

def update_modinfo(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        module = request.POST.get('module')
        contents = request.POST.get('contents')
        mi = Supplement.objects.get(user__id=user, module__id=module)
        mi.contents = contents
        mi.save()
        response = {"success" : True}
        return HttpResponse(json.dumps(response))
    
def resource_toggle(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.POST.get('user'))
        resource_id = request.POST.get('resource_id')
        toggle_resource_visibility(user, resource_id)
        response = {"new_val" : resource_visibility(user, resource_id).visible}
        return HttpResponse(json.dumps(response))
    
def module_toggle(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.POST.get('user'))
        module_num = request.POST.get('module_num')
        chapter_num = request.POST.get('chapter_num')
        toggle_module_visibility(user, module_num, chapter_num)
        response = {"new_val" : module_visibility(user, module_num, chapter_num).visible}
        return HttpResponse(json.dumps(response))
    
def chapter_toggle(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.POST.get('user'))
        chapter_num = request.POST.get('chapter_num')
        toggle_chapter_visibility(user, chapter_num)
        response = {"new_val" : chapter_visibility(user, chapter_num).visible}
        return HttpResponse(json.dumps(response))
    
def update_settings(request):
    if request.method == 'POST':
        user = request.user
        user.userprofile.bgcolor = request.POST.get('bgcolor')
        user.userprofile.headercolor = request.POST.get('headercolor')
        user.userprofile.sidecolor = request.POST.get('sidecolor')
        user.userprofile.textcolor = request.POST.get('textcolor')
        user.userprofile.location = request.POST.get('location')
        user.userprofile.save()
        return HttpResponse(json.dumps({"result" : "Success"}))
        