from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url(r'^add_trash/$', views.AddTrash.as_view(), name='add_trash'),

    url(r'^add_task/$', views.add_task, name='add_task'),

    url(r'^task_list/$', views.task_list, name='task_list'),

    url(r'^update_trash/(?P<pk>\d+)/$', views.UpdateTrash.as_view(), name='update_trash'),

    url(r'^(?P<trash_id>[0-9]+)/$', views.trash_details, name='trash_details'),

    url(r'^(?P<trash_id>[0-9]+)/recover/$', views.recover, name='recover'),

    url(r'^(?P<trash_id>[0-9]+)/delete/$', views.delete, name='delete'),

    url(r'^(?P<trash_id>[0-9]+)/wipe_trash/$', views.wipe_trash, name='wipe_trash'),

    url(r'^(?P<trash_id>[0-9]+)/delete_trash/$', views.delete_trash, name='delete_trash'),

    url(r'^(?P<trash_id>[0-9]+)/delete_by_regex/$', views.delete_by_regex, name='delete_by_regex'),

]
