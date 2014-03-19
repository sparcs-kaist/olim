from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import *
from olim.apps.storage.models import Filesys

# Listing the directory

def filesys(request):
    url = request.META["PATH_INFO"]
    this_dir_name = filter(None, url.split("/"))[-1]
    this_dir = Filesys.objects.filter(name=this_dir_name)[0]
    user_auth = request.user.is_authenticated()

    url_check = ""

    dir_contents = []
    file_contents = []
    is_child = False

    if this_dir_name != "root":
        is_child = True

    # For secured directories
    print user_auth

    if this_dir.is_secured:
        if user_auth:
            url_check = _checkURL(url)
        else:
            return HttpResponseRedirect('/login/?next='+url)
    else:
        url_check = _checkURL(url)

    # Make content lists shown to users

    if url_check:
        this_list = Filesys.objects.filter(parent_dir=this_dir_name)
        for item in this_list:
            if item.is_secured:
                print "SECURED"
                if user_auth:
                    if item.is_dir:
                        dir_contents.append({
                            'name': item.name,
                            'url': item.url,
                            'date': item.date,
                            'uploader': item.uploader,
                            'thumbnail': item.thumbnail,
                            'is_secured': item.is_secured,
                        })
                    else:
                        file_contents.append({
                            'name': item.name,
                            'url': item.url,
                            'date': item.date,
                            'uploader': item.uploader,
                            'thumbnail': item.thumbnail,
                            'is_secured': item.is_secured,
                        })
            else:
                if item.is_dir:
                    dir_contents.append({
                        'name': item.name,
                        'url': item.url,
                        'date': item.date,
                        'uploader': item.uploader,
                        'thumbnail': item.thumbnail,
                        'is_secured': item.is_secured,
                    })
                else:
                    file_contents.append({
                        'name': item.name,
                        'url': item.url,
                        'date': item.date,
                        'uploader': item.uploader,
                        'thumbnail': item.thumbnail,
                        'is_secured': item.is_secured,
                    })
    else:
        return HttpResponse("FALSE URL")

    print dir_contents
    print file_contents
    print is_child

    return HttpResponse(url)

def _checkURL(url):
    url_comp = filter(None, url.split("/"))
    url_comp.reverse()
    parent_dir = ""
    ch = 0

    for comp in url_comp:
        if ch != 0:
            if comp != parent_dir:
                return False
        dir = Filesys.objects.filter(name=comp)
        parent_dir = ''.join(dir.values_list('parent_dir', flat=True))
        ch += 1

    return True
