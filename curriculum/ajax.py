
import json
from django.shortcuts import render
from django.http import HttpResponse
from curriculum.models import *
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