from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, StreamingHttpResponse
from olim.apps.storage.models import Filesys
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.encoding import smart_str
from django.conf import settings
import json, mimetypes, os.path
from django.core.exceptions import ObjectDoesNotExist

def index(request):
    path = request.META["PATH_INFO"]
    ch_url = _check_dir_url(path)

    if ch_url[0]:
        p_dir = ch_url[1]

        if p_dir.is_secured and not request.user.is_authenticated():
            return HttpResponseRedirect('/nlogin/?n='+p_dir.url+'&r=secured_dir')
        else:
            return render_to_response('index.html', {
                'p_dir_id': p_dir.id,
                'p_dir_name': p_dir.name,
                'p_dir_url': p_dir.url,
            }, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/wrong_url')

def get_url_data(request):
    try:
        p_dir_id = request.GET.get('p_dir_id', None)
        p_dir_url = request.GET.get('p_dir_url', None)
        p_dir = ''

        if p_dir_id == '':
            p_dir = Filesys.objects.get(url=p_dir_url)
            p_dir_id = p_dir.id
        else:
            p_dir = Filesys.objects.get(id=p_dir_id)
            p_dir_url = p_dir.url

        # Get quick path

        quick_path = []
        p_dir_list = filter(None, p_dir_url.split("/"))

        for i, item in enumerate(p_dir_list):
            url = ""
            for j in range(i+1):
                url += "/" + p_dir_list[j]
            quick_path.append({'name':p_dir_list[i], 'url':url})

        # Link to parent dir

        pp_dir = ""

        if p_dir.parent_dir is not None:
            pp_obj = Filesys.objects.get(id=p_dir.parent_dir)
            pp_dir = {
                'id': pp_obj.id,
                'name': pp_obj.name,
                'url': pp_obj.url
            }

        # Get filesys data

        c_dirs = []
        c_files = []
        auth_c_list = []

        if request.user.is_authenticated():
            auth_c_list = Filesys.objects.filter(parent_dir=p_dir_id).extra(select={'lower_name':'lower(name)'}).order_by('lower_name')
        else:
            auth_c_list = Filesys.objects.filter(parent_dir=p_dir_id, is_secured=False).extra(select={'lower_name':'lower(name)'}).order_by('lower_name')

        for item in auth_c_list:
            if item.is_dir:
                c_dirs.append({
                    'id': item.id,
                    'name': "/" + item.name,
                    'url': item.url,
                    'date': "-",
                    'uploader': "-",
                    'thumbnail': "",
                    'is_secured': item.is_secured,
                    'format': item.format
                })
            else:
                c_files.append({
                    'id': item.id,
                    'name': item.name,
                    'url': item.url,
                    'date': item.date,
                    'uploader': item.uploader.username,
                    'thumbnail': item.thumbnail.name,
                    'is_secured': item.is_secured,
                    'format': item.format
                })

        contents = {
            'p_dir': {
                'id': p_dir.id,
                'name': p_dir.name,
                'url': p_dir.url
            },
            'quick_path': quick_path,
            'pp_dir': pp_dir,
            'dir_list': c_dirs,
            'file_list': c_files
        }
        output = json.dumps(contents, ensure_ascii=False, indent=4, cls=DjangoJSONEncoder)

        return HttpResponse(output)
    except:
        return HttpResponseBadRequest("Something went wrong.")

def get_file_data(request):
    try:
        file_url = request.META['PATH_INFO']
        file_obj = Filesys.objects.get(url=file_url)

        if file_obj.is_secured and not request.user.is_authenticated():
            return HttpResponseRedirect('/nlogin/?n='+file_obj.url+'&r=secured_file')

        file_nf = file_obj.name + '.' + file_obj.format

        response =  StreamingHttpResponse(file_obj.file)
        response['Content-Type'] = mimetypes.guess_type(file_nf)[0]
        response['Content-Disposition'] = 'attachment; filename=%s' % (smart_str(file_nf))

        return response
    except:
        return HttpResponseBadRequest("Wrong file path or error happened.")

def _check_dir_url(url):
    try:
        dir = Filesys.objects.get(url=url)
        return True, dir
    except ObjectDoesNotExist:
        return False, 0
