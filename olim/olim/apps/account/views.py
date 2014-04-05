from django.http import *
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def login_user(request):
    try:
        if request.user.is_authenticated():
            return HttpResponseBadRequest("you have already logged in.")
        else:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse(user.username)
            else:
                return HttpResponseBadRequest("inappropriate id or pw.")
    except:
        return HttpResponseBadRequest("inappropriate request.")

@login_required
def logout_user(request):
    try:
        logout(request)
        return HttpResponse("logout successed.")
    except:
        return HttpResponseBadRequest("something went wrong.")
