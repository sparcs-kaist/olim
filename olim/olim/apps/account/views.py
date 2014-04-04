from django.http import *
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf


#def login_user(request):
#    if request.user.is_authenticated():
#        return HttpResponseRedirect('/root')
#    else:
#        username = ""
#        password = ""
#
#        if request.POST:
#            username = request.POST['username']
#            password = request.POST['password']
#            user = authenticate(username=username, password=password)
#            if user is not None:
#                login(request, user)
#                if request.GET is not None:
#                    next = request.GET['next']
#                    return HttpResponseRedirect(next)
#                else:
#                    return HttpResponseRedirect('/root')
#            else:
#                print "NOT SPARCS USER"
#        else:
#            if request.GET is not None:
#                next = request.GET['next']
#
#        return render_to_response('login.html', {'next':next}, context_instance=RequestContext(request))


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
    logout(request)
    next = ""

    if request.GET:
        next = request.GET['next']

    return HttpResponseRedirect(next)
