from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import *
from olim.apps.storage.models import Filesys

# Listing the directory

def filesys(request):
    url = request.META["PATH_INFO"]

    if _checkURL(url):
        this_url_name = filter(None, url.split("/"))[-1]
        this_url = Filesys.objects.filter(name=this_url_name)[0]
        user_auth = request.user.is_authenticated()
        url_list = filter(None, url.split("/"))

        path_list = []
        dir_contents = []
        file_contents = []
        is_child = False
        parent_path = ""

        # For secured directories

        if this_url.is_secured:
            if not user_auth:
                return HttpResponseRedirect('/login/?next='+url)

        # For quick path

        for i, item in enumerate(url_list):
            path = ""
            for j in range(i+1):
                path += "/" + url_list[j]
            path_list.append({'url':url_list[i], 'path':path})

        if this_url_name != "root":
            is_child = True
            parent_path = path_list[-2]

        # Make content lists shown to users

        this_list = Filesys.objects.filter(parent_dir=this_url_name).order_by('name')
        for item in this_list:
            if item.is_secured:
                if user_auth:
                    if item.is_dir:
                        dir_contents.append({
                            'name': "/"+item.name,
                            'url': item.url,
                            'date': item.date,
                            'uploader': item.uploader,
                            'thumbnail': item.thumbnail,
                            'is_secured': item.is_secured,
                            'format': item.format
                        })
                    else:
                        file_contents.append({
                            'name': item.name,
                            'url': item.url,
                            'date': item.date,
                            'uploader': item.uploader,
                            'thumbnail': item.thumbnail,
                            'is_secured': item.is_secured,
                            'format': item.format
                        })
            else:
                if item.is_dir:
                    dir_contents.append({
                        'name': "/"+item.name,
                        'url': item.url,
                        'date': item.date,
                        'uploader': item.uploader,
                        'thumbnail': item.thumbnail,
                        'is_secured': item.is_secured,
                        'format': item.format
                    })
                else:
                    file_contents.append({
                        'name': item.name,
                        'url': item.url,
                        'date': item.date,
                        'uploader': item.uploader,
                        'thumbnail': item.thumbnail,
                        'is_secured': item.is_secured,
                        'format': item.format
                    })
    else:
        return HttpResponse("FALSE URL")

    return render_to_response('list.html', {
        'dir_contents' : dir_contents,
        'file_contents' : file_contents,
        'is_child' : is_child,
        'parent_path' : parent_path,
        'this_path' : url,
        'this_url' : this_url_name,
        'path_list' : path_list
    }, context_instance=RequestContext(request))

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
