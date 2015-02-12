from django.conf.urls import patterns, url
from time_engine import views

urlpatterns = patterns('',

        url(r'^register/', views.register, name='register'),
        url(r'^login/', views.user_login, name='login'),
        url(r'^logout', views.user_logout, name='index'),
        url(r'^$', views.index, name='index'),
        url(r'^ajax/', views.ajax, name='ajax'),
        # /options/
        url(r'^options/', views.options, name='options'),
        # dom
        url(r'dom/', views.dom, name='dom'),
        url(r'jsexample/', views.jsexample, name='jsexample'),

        )