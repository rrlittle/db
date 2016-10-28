from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/', auth_views.login, name='login'),
    url(r'^logout/', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^respondents/(?P<respondentid>[0-9]+)', views.respondent,
        name='respondent'),
    url(r'^respondents$', views.respondents, name='respondents'),
    url(r'^surveys$', views.surveys, name='surveys'),
    url(r'^surveys/(?P<surveyid>[0-9]+)$', views.survey, name='survey'),
    url(r'^surveys/(?P<surveyid>[0-9]+)/submit$', views.submit_survey,
        name='submit'),
    url(r'^surveys/post$', views.post_survey,
        name='post_survey'),
    url(r'^$', views.index, name='index'),
    url(r'^index$', views.index),
]
