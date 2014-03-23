from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import *
from olim.apps.storage.models import Filesys
from django.core.serializers.json import DjangoJSONEncoder
import json

# Listing the directory

def directory_index(request):
    this_dir_url = request.META["PATH_INFO"]

    if _checkURL(this_dir_url):
        dir_list = filter(None, this_dir_url.split("/"))
        this_dir = dir_list[-1]
        this_dir_data = Filesys.objects.filter(name=this_dir)[0]

        # Response Values.

        url_list = []
        is_child_dir = False
        parent_dir = ""

        # For secured dir.

        if this_dir_data.is_secured and not request.user.is_authenticated():
            return HttpResponseRedirect('/login/?next='+url)

        # For quick path.

        for i, item in enumerate(dir_list):
            url = ""
            for j in range(i+1):
                url += "/" + dir_list[j]
            url_list.append({'dir':dir_list[i], 'dir_url':url})

        # For link to parent dir.

        if this_dir != "root":
            is_child_dir = True
            parent_dir = url_list[-2]

        return render_to_response('list.html', {
            'this_dir': this_dir,
            'this_dir_url': url,
            'url_list': url_list,
            'is_child_dir': is_child_dir,
            'parent_dir': parent_dir
        }, context_instance=RequestContext(request))

    # For false url.

    else:
        return HttpResponse("FALSE URL")

def get_list_filesys(request):
    this_dir = request.GET.get('this_dir', None)

    try:
        this_list = Filesys.objects.filter(parent_dir=this_dir).extra(select={'lower_name':'lower(name)'}).order_by('lower_name')
        auth_dir_list = []
        auth_file_list = []

        dir_list = []
        file_list = []

        # Sorting

        for item in this_list:
            if request.user.is_authenticated():
                if item.is_dir:
                    auth_dir_list.append(item)
                else:
                    auth_file_list.append(item)
            else:
                if not item.is_secured:
                    if item.is_dir:
                        auth_dir_list.append(item)
                    else:
                        auth_file_list.append(item)

        # Content appending

        for item in auth_dir_list:
            dir_list.append({
                'name': '/' + item.name,
                'url': item.url,
                'date': '-',
                'uploader': '-',
                'thumbnail': '',
                'is_secured': item.is_secured,
                'format': item.format
            })

        for item in auth_file_list:
            file_list.append({
                'name': item.name,
                'url': item.url,
                'date': item.date,
                'uploader': item.uploader.username,
                'thumbnail': item.thumbnail.name,
                'is_secured': item.is_secured,
                'format': item.format
            })

        contents = {'dir_list': dir_list, 'file_list': file_list}
        output = json.dumps(contents, ensure_ascii=False, indent=4, cls=DjangoJSONEncoder)

        return HttpResponse(output)

    except:
        return HttpResponseBadRequest()

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
