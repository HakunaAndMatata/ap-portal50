from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Tag(models.Model):
	name = models.CharField(max_length=50)
	def __unicode__(self):
		return self.name

class QuestionType(models.Model):
	name = models.CharField(max_length=512)
	position = models.IntegerField(default=0)
	def __unicode__(self):
		return str(self.name)

# need to 'pip install Pillow' in order to allow for image field
class Question(models.Model):
	title = models.CharField(max_length=200,default="")
	question = models.TextField(default="",blank=True,null=True,help_text="Syntax Guide: *underline*, **bold**, [[image]], `inline code`, ```code block```")
	answer = models.TextField(default="",blank=True,null=True,help_text="Syntax Guide: *underline*, **bold**, [[image]], `inline code`, ```code block```")
	q_image = models.ImageField(upload_to='quizbank/q/',blank=True,null=True,verbose_name="Question Image")
	a_image = models.ImageField(upload_to='quizbank/a/',blank=True,null=True,verbose_name="Answer Image")
	tags = models.ManyToManyField(Tag,blank=True)
	qtype = models.ForeignKey(QuestionType, on_delete=models.PROTECT, verbose_name="question type")
	released = models.BooleanField(default=False, verbose_name="Available to Public")
	authorship_year = models.IntegerField(blank=True,null=True)
	original_exam = models.CharField(max_length=50,blank=True,null=True,help_text="e.g. 2015 Quiz 0")
	original_question = models.IntegerField(blank=True,null=True)
	points = models.IntegerField(blank=True,null=True)
	difficulty = models.DecimalField(max_digits=6,decimal_places=4,blank=True,null=True,help_text="1: Easy, 2: Medium, 3: Hard")
	notes = models.TextField(default="",blank=True,null=True)
	def __unicode__(self):
		return self.title