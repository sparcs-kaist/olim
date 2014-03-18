from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import *
from olim.apps.storage.models import Filesys

# Listing the directory
def filesys(request):
    url = request.META["PATH_INFO"]
    url_check = _checkURL(url)

    if url_check:
        return HttpResponse(url)
    else:
        return HttpResponse("False URL : " + url)

def _checkURL(url):
    url_comp = filter(None, url.split("/"))
    url_comp.reverse()
    parent_dir = ""
    ch = 0

    for comp in url_comp:
        print comp, parent_dir
        if ch != 0:
            if comp != parent_dir:
                return False
        dir = Filesys.objects.filter(name=comp)
        parent_dir = ''.join(dir.values_list('parent_dir', flat=True))
        ch += 1
    
    return True
