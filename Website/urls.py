from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register_user', views.register_user, name='register_user'),
    path('register_success', views.register_success, name='register_success'),
    path('login_user', views.login, name='login_user'),
    path('authorized', views.auth_view),
    path('logout', views.logout),
    path('loggedin', views.loggedin),
    path('invalid', views.invalid_login),
]
    #url(r'^register_user/$', views.register_user, name='register_user'),
    #url(r'^register_success/$', views.register_success, name='register_success'),
    #url(r'^login/$', views.login),
    #url(r'^authorized/$', views.auth_view),
    #url(r'^logout/$', views.logout),
    #url(r'^loggedin/$', views.loggedin),
    #url(r'^invalid/$', views.invalid_login),
