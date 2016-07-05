import mistune
from django.conf import settings
from quizbank.models import *

def render50(text,image):
	text = render_markdown(text)
	text = text.replace("[[image]]", '<img style="width:60%;height:auto;max-width:400px;" src="' + settings.MEDIA_URL + '/' + image.name + '">');
	text = text.replace("[[tab]]", '&nbsp;&nbsp;&nbsp;&nbsp;');
	text = text.replace("\t", '&nbsp;&nbsp;&nbsp;&nbsp;');
	return text

def render50_short(text):
	text = render_markdown(text)
	return text

def render_markdown(text):
	text = mistune.markdown(text)
	text = text.replace("<em>", "<em style=\"text-decoration:underline;font-style:normal\">")
	return text

# gets all questions that have particular tags
def questions_with_tags(tags):
	questions = []
	for tag in tags:
		lst = Question.objects.filter(tags__name=tag)
		questions += lst
	return list(set(questions))

# filters questions out by question type
def filter_qtypes(questions, qtypes):
	new_questions = []
	for question in questions:
		if question.qtype.name in qtypes:
			new_questions.append(question)
	return new_questions

# filters questions by difficulty
def filter_difficulty(questions, difficulties):
	new_questions = []
	for question in questions:
		if question.difficulty in difficulties:
			new_questions.append(question)
	return new_questions

# filters questions by year
def filter_years(questions, years):
	new_questions = []
	for question in questions:
		if question.authorship_year in years:
			new_questions.append(question)
	return new_questions

# filters questions by release
def filter_releases(questions, releases):
	new_questions = []
	for question in questions:
		if question.released in releases:
			new_questions.append(question)
	return new_questions

def tag_names_of_question(question):
	tags = question.tags.all()
	lst = []
	for tag in tags:
		lst.append(tag.name)
	return lst

def question_as_dict(question,full_details):
	if full_details:
		return {'title': question.title,
		'question': render50(question.question,question.q_image),
		'answer': render50(question.answer,question.a_image),
		'qtype' : question.qtype.name,
		'released' : question.released,
		'authorship_year' : question.authorship_year,
		'original_exam' : question.original_exam,
		'original_question' : question.original_question,
		'points' : question.points,
		'difficulty' : question.difficulty,
		'tags' : tag_names_of_question(question),
		'id': question.id }
	else:
		return {'title': question.title,
		'question': render50_short(question.question),
		'qtype' : question.qtype.name,
		'authorship_year' : question.authorship_year,
		'released' : question.released,
		'id':question.id }

