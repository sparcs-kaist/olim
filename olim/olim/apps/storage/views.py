from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import *

# Listing the directory
def listing(request):
    return HttpResponse("test")

# Create your views here.
