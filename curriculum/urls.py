from django.conf.urls import url
from . import views, ajax

app_name = 'curriculum'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^register/', views.register, name='register'),
	url(r'^logout/', views.logout_view, name='logout'),
	url(r'^login/', views.login_view, name='login'),

	url(r'^customize/$', views.customize, name='customize'),
	url(r'^customize/(?P<chapter>[0-9]+)/$', views.chapter_customize, name='chapter_customize'),
	url(r'^customize/(?P<chapter>[0-9]+)/(?P<slug>[\w.@+-]+)/$', views.module_customize, name='module_customize'),

	url(r'^curriculum/$', views.curriculum_page, name='curriculum_page'),
	url(r'^curriculum/(?P<chapter>[0-9]+)/$', views.curriculum_page_chapter, name='curriculum_page_chapter'),
	url(r'^curriculum/(?P<chapter>[0-9]+)/(?P<slug>[\w.@+-]+)/$', views.curriculum_page_module, name='curriculum_page_module'),
    
    url(r'^ajax/modinfochange/$', ajax.update_modinfo, name='update_modinfo'),

	# both /brian and /u/brian will go to the user's curriculum page
	url(r'^(?P<username>[\w.@+-]+)/$', views.teacher_page, name='teacher_page'),
	url(r'^(?P<username>[\w.@+-]+)/(?P<chapter>[0-9]+)/$', views.teacher_page_chapter, name='teacher_page_chapter'),
	url(r'^(?P<username>[\w.@+-]+)/(?P<chapter>[0-9]+)/(?P<slug>[\w.@+-]+)/$', views.teacher_page_module, name='teacher_page_module'),
	url(r'^u/(?P<username>[\w.@+-]+)/$', views.teacher_page, name='teacher_page_u'),
	url(r'^u/(?P<username>[\w.@+-]+)/(?P<chapter>[0-9]+)/$', views.teacher_page_chapter, name='teacher_page_chapter_u'),
	url(r'^u/(?P<username>[\w.@+-]+)/(?P<chapter>[0-9]+)/(?P<slug>[\w.@+-]+)/$', views.teacher_page_module, name='teacher_page_module_u'),
]