from django.conf.urls import patterns, url
from time_engine import views

urlpatterns = patterns('',

        url(r'^register/', views.register, name='register'),
        url(r'^login/', views.user_login, name='login'),
        url(r'^logout', views.user_logout, name='index'),
        url(r'^$', views.index, name='index'),
        url(r'^delete_timetable/', views.delete_timetable, name='delete_timetable'),
        url(r'^ajax/', views.ajax, name='ajax'),
        # /options/
        url(r'^options/', views.options, name='options'),
        # dom
        url(r'dom/', views.dom, name='dom'),
        url(r'jsexample/', views.jsexample, name='jsexample'),
        url(r'^get_timetable/', views.get_timetable, name="get_timetable"),
        )