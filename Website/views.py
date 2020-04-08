from typing import Any
from django.views.generic import TemplateView
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.template import RequestContext
from Website.forms import RegistrationForm, HomeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import requests
from django.template import loader
from django.template.response import TemplateResponse


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


def input(request):
    return render(request, 'scraping.html', {})


def scraping(request):
    link = 'https://www.filmweb.pl/search?q='
    if request.method == 'POST':
        data = request.POST.get("text")
        if len(data) < 1:
            empty = 'Data is empty. Please write something :)'
            return render(request, 'scrapingscore.html', {'empty': empty})
        else:
            data1 = data.replace(" ", "+")

            search = link + data1
            req = Request(
                search,
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )

            req1 = urlopen(req).read()
            soup = BeautifulSoup(
                req1,
                features="lxml"
            )
            title = soup.select_one('.hit__title a')
            list = []
            list.append(title)
            print(list)
            if list != [None]:
                urls = [tag['href'] for tag in list if 'href' in tag.attrs and "person" in tag['href']]
                urls = ''.join(urls)

                urls = urls.replace(" ", "")
            else:
                namenotfound = 'Actor not found :( Please check the spelling! :)'
                return render(request, 'scrapingscore.html', {'namenotfound': namenotfound})
            newlink = 'https://filmweb.pl' + urls
            response = requests.get(newlink).text
            soup1 = BeautifulSoup(response, 'html.parser')
            name = soup1.find("a", itemprop="name").text
            if name.lower() != data.lower():
                incorrectname = "You chose " + data, " did you mean " + name + "?"
            else:
                incorrectname = ''
            if 'ocena pracy reżyserskiej' in response:
                profession = name + ' is a director, his best 3 director works in the opinion of fans are:'
            elif 'ocena ról aktorskich' in response:
                profession = name + ' - is an actor, his best 3 movie roles in the opinion of fans are:'
            elif 'ocena scenariuszy' in response:
                profession = name + 'is a scenarist, his 3 best scenarios in the opinion of fans are:'
            photo = soup1.select_one('.personBigPhoto')['src']
            birthdate = soup1.find("span", itemprop="birthDate").text
            print(name)
            results = soup1.find_all("div", class_="maxlines-4")

            for result in results[:1]:
                a = result.find('a', href=True)['href']
                movielink1 = ('https://filmweb.pl' + a)
            for result in results[:2]:
                a = result.find('a', href=True)['href']
                movielink2 = ('https://filmweb.pl' + a)
            for result in results[:3]:
                a = result.find('a', href=True)['href']
                movielink3 = ('https://filmweb.pl' + a)

            productLinks = [div.a for div in soup1.find_all("div", class_="maxlines-4")]
            for link in productLinks[:1]:
                moviename1 = link.string
            for link in productLinks[:2]:
                moviename2 = link.string
            for link in productLinks[:3]:
                moviename3 = link.string

            results3 = soup1.find_all("span", class_="s-20")
            for link in results3[:1]:
                movierate1 = link.text
            for link in results3[:2]:
                movierate2 = link.text
            for link in results3[:3]:
                movierate3 = link.text

            results4 = soup1.find_all("span", class_="s-14 left-5")
            for link in results4[:1]:
                movieratenumber1 = link.text
            for link in results4[:2]:
                movieratenumber2 = link.text
            for link in results4[:3]:
                movieratenumber3 = link.text
            return render(request, 'scrapingscore.html',
                          {'movielink1': movielink1, 'movielink2': movielink2, 'movielink3': movielink3,
                           'moviename1': moviename1, 'moviename2': moviename2, 'moviename3': moviename3,
                           'movierate1': movierate1, 'movierate2': movierate2, 'movierate3': movierate3,
                           'movieratenumber1': movieratenumber1, 'movieratenumber2': movieratenumber2,
                           'movieratenumber3': movieratenumber3, 'profession': profession,
                           'incorrectname': incorrectname, 'birthdate': birthdate, 'photo': photo})


def scrapingscore(request):
    return render_to_response('scrapingscore.html')
