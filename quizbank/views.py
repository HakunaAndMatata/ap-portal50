from django.shortcuts import render
from django.middleware import csrf
from quizbank.helpers import *

# Handles view for the quizbank home
def index(request):
	# only approve for viewing private questions if both logged in and approved
	approved = False
	if request.user != None and request.user.id != None:
		if request.user.userprofile.approved:
			approved = True
	return render(request, 'quizbank/index.html', {'user':request.user, 'approved':approved})
		