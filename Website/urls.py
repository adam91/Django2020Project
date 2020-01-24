from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from Website import views as core_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', LoginView.as_view(), {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', LogoutView.as_view(), {'next_page': 'login'}, name='logout'),

]
