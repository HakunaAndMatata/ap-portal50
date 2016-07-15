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
    
    url(r'^resources/$', views.resources, name='resources'),
    url(r'^settings/$', views.settings, name='settings'),

	url(r'^curriculum/$', views.curriculum_page, name='curriculum_page'),
	url(r'^curriculum/(?P<chapter>[0-9]+)/$', views.curriculum_page_chapter, name='curriculum_page_chapter'),
	url(r'^curriculum/(?P<chapter>[0-9]+)/(?P<slug>[\w.@+-]+)/$', views.curriculum_page_module, name='curriculum_page_module'),
    
    url(r'^page/(?P<pagename>[\w.@+-]+)/$', views.show_page, name='show_page'),
    
    url(r'^profile/(?P<username>[\w.@+-]+)/$', views.profile, name='profile'),
    
    url(r'^ajax/modinfochange/$', ajax.update_modinfo, name='update_modinfo'),
    url(r'^ajax/resource-toggle/$', ajax.resource_toggle, name='resource_toggle'),
    url(r'^ajax/module-toggle/$', ajax.module_toggle, name='module_toggle'),
    url(r'^ajax/chapter-toggle/$', ajax.chapter_toggle, name='chapter_toggle'),
    url(r'^ajax/update-settings/$', ajax.update_settings, name='update_settings'),
    url(r'^ajax/add-resource/$', ajax.add_resource, name='add_resource'),
    url(r'^ajax/remove-resource/$', ajax.remove_resource, name='remove_resource'),
    # calls ajax.py (so do the rest, but this is Annie needing to give herself more hints)
    url(r'^ajax/access-resource/$', ajax.access_resource, name='access_resource'),
    url(r'^ajax/edit-resource/$', ajax.edit_resource, name='edit_resource'),

	# both /brian and /u/brian will go to the user's curriculum page
	url(r'^(?P<username>[\w.@+-]+)/$', views.teacher_page, name='teacher_page'),
	url(r'^(?P<username>[\w.@+-]+)/(?P<chapter>[0-9]+)/$', views.teacher_page_chapter, name='teacher_page_chapter'),
	url(r'^(?P<username>[\w.@+-]+)/(?P<chapter>[0-9]+)/(?P<slug>[\w.@+-]+)/$', views.teacher_page_module, name='teacher_page_module'),
	url(r'^u/(?P<username>[\w.@+-]+)/$', views.teacher_page, name='teacher_page_u'),
	url(r'^u/(?P<username>[\w.@+-]+)/(?P<chapter>[0-9]+)/$', views.teacher_page_chapter, name='teacher_page_chapter_u'),
	url(r'^u/(?P<username>[\w.@+-]+)/(?P<chapter>[0-9]+)/(?P<slug>[\w.@+-]+)/$', views.teacher_page_module, name='teacher_page_module_u'),
]