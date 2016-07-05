import json
from django.shortcuts import render
from django.http import HttpResponse
from quizbank.models import *
from quizbank.helpers import *

# if posted, gets the list of all tags
def taglist(request):
	if request.method == 'POST':
		return tags(request)

def tags(request):
	tags = Tag.objects.all()
	lst = []
	for tag in tags:
		# if there are no associated questions, don't include tag
		if len(tag.question_set.all()) == 0:
			continue
		lst.append([tag.name.replace(' ', '_'), tag.name])
	lst.sort()
	return HttpResponse(json.dumps(lst))

# if posted, gets list of all authorship years
def yearlist(request):
	if request.method == 'POST':
		return years(request)

def years(request):
	questions = Question.objects.all()
	lst = []
	for question in questions:
		lst.append(question.authorship_year)
	lst = list(set(lst))
	return HttpResponse(json.dumps(lst))

# if posted, returns list of question types
def qtypelist(request):
	if request.method == 'POST':
		return qtypes(request)

def qtypes(request):
	qtypes = QuestionType.objects.all().order_by('position')
	lst = []
	for qtype in qtypes:
		# if there are no questions of this type, then don't return the type as an option
		num = Question.objects.filter(qtype=qtype).count()
		if (num == 0):
			continue
		name = qtype.name
		tag_name = name.replace(' ', '_')
		tag_name = name.replace('/', '_')
		# returning a list of pairs of tags and names, since we want tags without spaces
		lst.append([tag_name, name])
	return HttpResponse(json.dumps(lst))

# someone queries the quiz bank
def query(request):
	response = []
	if request.method == 'POST':
		data = request.POST
		unformatted_tags = data.getlist(u'tags[]')
		unformatted_difficulties = data.getlist(u'difficulties[]')
		unformatted_qtypes = data.getlist(u'qtypes[]')
		unformatted_releases = data.getlist(u'releases[]')
		unformatted_years = data.getlist(u'years[]')

		tags = []
		difficulties = []
		qtypes = []
		releases = []
		years = []

		for tag in unformatted_tags:
			tags.append(str(tag))
		for difficulty in unformatted_difficulties:
			difficulties.append(int(difficulty))
		for qtype in unformatted_qtypes:
			qtypes.append(str(qtype))
		for release in unformatted_releases:
			releases.append(int(release))
		for year in unformatted_years:
			years.append(int(year))

		questions = questions_with_tags(tags)
		questions = filter_qtypes(questions,qtypes)
		questions = filter_difficulty(questions,difficulties)
		questions = filter_years(questions,years)
		questions = filter_releases(questions,releases)

		for question in questions:
			response.append(question_as_dict(question, False))
	return HttpResponse(json.dumps(response))

# someone queries a question
def question_detail(request):
	response = []
	if request.method == 'POST':
		id_num = request.POST.get('id')
		question = Question.objects.get(pk=id_num)
		response = question_as_dict(question,True)
	return HttpResponse(json.dumps(response))