from django.conf.urls import patterns, include, url
from scrabbleApp import views


urlpatterns = patterns('', url(r'^test', views.test, name='test'))