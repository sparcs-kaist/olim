from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import *
from olim.apps.storage.models import Filesys
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import smart_str
from django.conf import settings
import json, mimetypes, os.path

# Listing the directory

def directory_index(request):
    this_dir_url = request.META["PATH_INFO"]

    if _check_dir_url(this_dir_url):
        dir_list = filter(None, this_dir_url.split("/"))
        this_dir = dir_list[-1]
        this_dir_data = Filesys.objects.filter(name=this_dir)[0]

        # Response Values.

        url_list = []
        is_child_dir = False
        parent_dir = ""

        # For secured dir.

        if this_dir_data.is_secured and not request.user.is_authenticated():
            return HttpResponseRedirect('/login/?next='+this_dir_url)

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

    # For wrong url.

    else:
        return HttpResponse("WRONG URL")

def file_index(request):
    this_file_url = request.META["PATH_INFO"]
    this_file_hash = filter(None, this_file_url.split("/"))[-1]
    this_file_data = Filesys.objects.filter(url=this_file_url)[0]
    this_file_path = os.path.join(settings.FILES_ROOT, this_file_hash)

    if this_file_data:

        # For secured file.

        if this_file_data.is_secured and not request.user.is_authenticated():
            return HttpResponseRedirect('/login/?next='+this_file_url)
        else:
            this_file = this_file_data.name + '.' + this_file_data.format

            response = HttpResponse(file(this_file_path))
            response['Content-Type'] = mimetypes.guess_type(this_file)[0]
            response['Content-Disposition'] = 'attachment; filename=%s' % (smart_str(this_file))

            return response
    else:

        # For wrong file path.

        return HttpResponse("WRONG FILE PATH")

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

def _check_dir_url(url):
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
