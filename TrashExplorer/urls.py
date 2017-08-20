from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.TrashList.as_view(), name='index'),

    url(r'^add_trash/$', views.AddTrash.as_view(), name='add_trash'),

    url(r'^add_task/$', views.AddTask.as_view(), name='add_task'),

    url(r'^task_list/$', views.TaskList.as_view(), name='task_list'),

    url(r'^update_trash/(?P<pk>\d+)/$', views.UpdateTrash.as_view(), name='update_trash'),

    url(r'^run/(?P<task_id>[0-9]+)/$', views.run, name='run'),

    url(r'^(?P<trash_id>[0-9]+)/$', views.trash_details, name='trash_details'),

    url(r'^(?P<trash_id>[0-9]+)/recover/$', views.recover, name='recover'),

    url(r'^(?P<trash_id>[0-9]+)/wipe_trash/$', views.wipe_trash, name='wipe_trash'),

    url(r'^(?P<trash_id>[0-9]+)/delete_trash/$', views.delete_trash, name='delete_trash'),

    url(r'^update_task/(?P<pk>\d+)/$', views.UpdateTask.as_view(), name='update_task'),

    url(r'^delete_task/(?P<task_id>[0-9]+)/$', views.DeleteTask, name='delete_task'),

]
