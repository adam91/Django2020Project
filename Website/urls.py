from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register_user', views.register_user, name='register_user'),
    path('register_success', views.register_success, name='register_success'),
    path('login_user', views.login_user, name='login_user'),
    path('authorized', views.auth_view, name='authorized'),
    path('logged_out', views.logged_out, name='logged_out'),
    path('logged_in', views.logged_in, name='logged_in'),
    path('invalid_login', views.invalid_login, name='invalid_login'),
    path('scraping', views.input, name='input'),
    path('scrapingscore', views.scraping, name='scraping'),
]
