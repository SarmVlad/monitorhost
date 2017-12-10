from django.conf.urls import url
from main import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'panel/$', views.panel, name='panel'),
    url(r'login/$', views.login, name='login'),
    url(r'registration/$', views.register, name='reg'),
    #Methods
    url(r'logout/$', views.logout, name='logout'),
    url(r'reg/$', views.register, name='reg_method'),
    url(r'signin/$', views.sign_in,  name='signin_method'),
]
