from django.conf.urls import url
from . import views, ajax

app_name = 'quizbank'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^ajax/taglist/$', ajax.taglist, name='taglist'),
	url(r'^ajax/yearlist/$', ajax.yearlist, name='yearlist'),
	url(r'^ajax/qtypelist/$', ajax.qtypelist, name='qtypelist'),
	url(r'^ajax/query/$', ajax.query, name='query'),
	url(r'^ajax/question_detail/$', ajax.question_detail, name='question_detail'),
]