from django.conf.urls import url
from main import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index),

    url(r'panel/$', views.panel, name='panel'),

    url(r'login/$', views.log_in, name='login'),
    url(r'registration/$', views.register, name='reg'),
    url(r'logout/$', views.log_out, name='logout'),
    url(r'activate/(?P<username>.+)/(?P<code>.+$)', views.activate, name='activate'),

    url(r'check-data/$', views.check),
]
