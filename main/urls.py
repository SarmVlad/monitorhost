from django.conf.urls import url
from main import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index),

    url(r'panel/$', views.panel, name='panel'),
    url(r'panel/messages/$', views.panel_messages, name='panel_messages'),
    #url(r'panel/messages/$', views.panel_write_message, name='write_message'),

    url(r'login/$', views.log_in, name='login'),
    url(r'registration/$', views.register, name='reg'),
    url(r'logout/$', views.log_out, name='logout'),
    url(r'activate/(?P<username>.+)/(?P<code>.+$)', views.activate, name='activate'),
    url(r'recovery/$', views.recovery, name='pass_recovery'),
    url(r'recovery/(?P<username>.+)/(?P<code>.+$)', views.change_pass, name='change_pass'),

    url(r'check-data/$', views.check),
]
