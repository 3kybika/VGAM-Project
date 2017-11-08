# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth

from django.contrib.auth import login 
from django.contrib.auth import logout 
from django.contrib.auth import authenticate

from cgi import parse_qsl, escape
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.shortcuts import render

from rating.models import *
from rating import forms

# Create your views here.
import random

#test
def simpleWSGIScript(request):

    output = "Hello world\n(WSGI-script)</p>"

    output += 'Get:'
    output += '<form method="Get">'
    output += '<input type="text" name = "get-query">'
    output += '<input type="submit" value="Send">'
    output += '</form>'

    output += 'Post:'
    output += '<form method="Post">'
    output += '{%csrf_token %}'
    output += '<input type="text" name = "post-query">'
    output += '<input type="submit" value="Send">'
    output += '</form>'

    if request.method == 'GET':
        output += '<h1>Get data:</h1>'
        output += '/n'.join(["%s=%s"%(key,value)for key,value in request.GET.items()])
    if request.method == 'POST':
        output += '<h1>Post data:</h1>'
        output += '/n'.join(["%s=%s"%(key,value)for key,value in request.POST.items()])

    return HttpResponse(output)


#page for registration
#url-name: register_page
def registerUser(request):

    user = request.user

    if user.is_authenticated():
        return redirect('rating_page')

    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user = authenticate(
            	username = form.cleaned_data['username'],
                password = form.cleaned_data['password'] 
            )
            login(request, user)
            return redirect('rating_page')
    else:
        form = forms.RegistrationForm()

    return render(request, 'register_tmp.html', {'form': form,})


#page for autorisation
#url-name: login_page
def loginUser(request):
    user = request.user

    if user.is_authenticated():
        return redirect('rating_page')

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():

            user = authenticate(
            	username = form.cleaned_data['username'],
                password = form.cleaned_data['password'] 
            )
            login(request, user)
            nextPage = request.GET.get('next')
            if nextPage:
       	        return redirect(nextPage)

            return redirect('rating_page')
    else:
        form = forms.LoginForm()

    return render(request, 'register_tmp.html', {'form': form,})


#function for logout. It will redirect to login_page
#url-name: log-out
def logoutUser(request):
    logout(request)
    nextPage = request.GET.get('next')
    if nextPage:
        return redirect(nextPage)

    return redirect('register_page')


#page with expert's rating
#url-name: rating_page
def ratingPage(request):
    user = request.user

    if user.is_authenticated():
        return render(request, 'Cards_tmp.html', {'objects' : MakePages(request, Expert.objects.all()),'toolbox_required': 1, })
    return render(request, 'Cards_tmp.html', {'objects' : MakePages(request, Expert.objects.all()),'toolbox_required': 0, })

def profilePage(request):
    user = request.user
    if user.is_authenticated():
        return render(request, 'expert_card.html', {'user':user, 'toolbox_required': 1, })
    return redirect('register_page')

def indexPage(request):
	return redirect('rating_page')

#paginator
def MakePages(request, respondList, elementsOnPage = 5):

    paginator = Paginator(respondList, elementsOnPage)
    page = request.GET.get('page')
    try:
        result = paginator.page(page)

    except PageNotAnInteger:
        result = paginator.page(1)

    except EmptyPage:
        result = paginator.page(paginator.num_pages)

    return result



   