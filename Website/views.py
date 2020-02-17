from typing import Any

from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.template import RequestContext
from Website.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login


def index(request):
    return HttpResponse("Test :)")

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('register_success')

    args = {}
    args.update(csrf(request))

    args['form'] = RegistrationForm()
    return render_to_response('register_user.html', args)

def register_success(request):
    return render_to_response('register_success.html')

def login_user(request):
    login_user = {}
    login_user.update(csrf(request))
    return render_to_response('login_user.html', login_user)

def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return redirect('logged_in')
    else:
        return HttpResponseRedirect('invalid_login')
    
def logged_in(request):
    return render_to_response('logged_in.html',
                              {'user': request.user})

def invalid_login(request):
    return render_to_response('invalid_login.html')

def logged_out(request):
    auth.logout(request)
    return render_to_response('logged_out.html')
