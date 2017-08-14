from django.conf.urls import url

from . import views
from .apps import PollsConfig

# set namespace. so different apps can use same name and differ with namespace.
app_name = PollsConfig.name
urlpatterns = [
    # url(r'^$', views.index, name='index'),
    # url(r'^specifics/(?P<question_id>[0-9]+)/$', views.detail, name="detail"),
    # url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name="results"),
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),

    # use django generic views system
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^specifics/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name="detail"),
    url(r'^(?P<question_id>[0-9]+)/results/$', views.ResultsView.as_view(), name="results"),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]