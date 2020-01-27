from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.template import RequestContext
from Website.forms import RegistrationForm


def index(request):
    return HttpResponse("Test :)")

def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('register_success')
        print(form.errors)

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

    if user is not None:
        auth.login(request, user)
        return redirect('index')
    else:
        return HttpResponseRedirect('invalid_login')
    
def logged_in(request):
    return render_to_response('logged_in.html',
                              {'full_name': request.user.username})

def invalid_login(request):
    return render_to_response('invalid_login.html')

def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')
