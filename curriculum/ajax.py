
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
    
def add_resource(request):
    if request.method == 'POST':
        module = Module.objects.get(pk=request.POST.get('module'))
        rtype = request.POST.get('rtype')
        name = request.POST.get('name')
        content = request.POST.get('content')
        link = request.POST.get('link')
        public = request.POST.get('public') == "true"
        print "THIS IS THE VALUE OF PUBLIC: "
        print public
        if 'http://' not in link and 'https://' not in link and link != "":
            link = 'http://' + link
        if rtype == 0:
            return HttpResponse(json.dumps({"result" : "Failure: No resource type specified."}))
        rtype = ResourceType.objects.get(name=rtype)
        resource = Resource.objects.create(author=request.user, module=module, rtype=rtype, name=name, content=content, link=link, shared=public)
        # set default to not visible for all users
        users = User.objects.all()
        for user in users:
            vis = ResourceVisibility.objects.create(user=user,resource=resource)
            vis.visible = False
            vis.save()
        # set default to visible for this user
        rv = resource_visibility(request.user, resource.id)
        rv.visible = True
        rv.save()
        return HttpResponse(json.dumps({"result" : "Success"}))
    
def remove_resource(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        remove_resource_and_vis(id)
        return HttpResponse(json.dumps({"result" : "Success"}))
        
def access_resource(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        # id is the resourceID of the resource we want information about
        resource = Resource.objects.get(id=id)
        response = {}
        response["rtype"] = resource.rtype.name
        response["name"] = resource.name
        response["content"] = resource.content
        response["link"] = resource.link
        response["shared"] = resource.shared
        print "I wonder if it's shared now?"
        print response["shared"]
        # return json object with what we want to know about that resource
        return HttpResponse(json.dumps(response))
        
def edit_resource(request):
    if request.method == 'POST':
        # first get the original resource from that type
        id = request.POST.get('id')
        resource = Resource.objects.get(id=id)
        # then process the other fields from that resource, update and save
        resource.rtype = ResourceType.objects.get(name=request.POST.get('rtype'))
        resource.name = request.POST.get('name')
        resource.content = request.POST.get('content')
        resource.shared = request.POST.get('public') == "true"
        link = request.POST.get('link')
        if 'http://' not in link and 'https://' not in link and link != "":
            link = 'http://' + link
        resource.link = link
        #save all the edits (hopefully there are edits?)
        resource.save()
        print "Is it shared?"
        print resource.shared
        return HttpResponse(json.dumps({"result" : "Success"}))
    