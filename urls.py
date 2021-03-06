from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView


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
    url(r'^surveys/(?P<surveyid>[0-9]+)/import$', views.import_survey,
        name='import'),
    url(r'^surveys/post_survey$', views.post_survey,
        name='post_survey'),
    url(r'^surveys/post_csv$', views.post_csv,
        name='post_csv'),
    url(r'^$', views.index, name='index'),
    url(r'^index$', views.index),
]
