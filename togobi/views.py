from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date
from django.http import JsonResponse
from django.db.models import Count
from django.db.models import TextField
from django.db.models.functions import Concat
from pathlib import Path
from pymediainfo import MediaInfo

from togobi.forms import ContentForm, ContentFileForm
from togobi.models import Content, ContentFile, ContentJoin
from togobi.serializers import ContentSerializer

from google.auth.transport.requests import AuthorizedSession
from google.resumable_media.requests import ResumableUpload
import io
from google.cloud import storage

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

# Create your views here.
time_threshold = datetime.now() + timedelta(hours=1)

def content_list(request):
    contents = get_contents(request)
    contents_today = Content.objects.filter(
            target_date__day=date.today().day).order_by('-target_date')
    contents_top = ContentJoin.objects.annotate(distinct_name=Concat(
        'content_id', 'content_id', output_field=TextField())).order_by('distinct_name').distinct('distinct_name')
    return render(request, 'home.html', {
        'contents': contents,
        'contents_today' : contents_today,
        'contents_top' : contents_top,
        })


def content_details(request, id):
    if request.method == 'GET':
        content = get_object_or_404(Content, id=id)
    return render(request, 'content_details.html', {'content': content})


@login_required
def content_add(request):
    if request.method == 'POST':
        content_form = ContentForm(request.POST)
        if content_form.is_valid():
            content = content_form.save(commit=False)
            content.user = request.user
            content.save()
            return redirect('content_details', id=content.id)
        else:
            print('not valid')
    else:
        content_form = ContentForm(initial={})
    # TODO: catch exception, saying internet speed is not good for uploading
        context = {
            'content_form': content_form,
            'content_file_form': ContentFileForm(initial={}),
        }
        return render(request, 'content_add.html', context)


@login_required
def content_join(request, id):
    if request.method == 'GET':
        content = get_object_or_404(Content, id=id)
        content_join = ContentJoin.objects.filter(
            user=request.user, content=content
        ).first()
        
        if not content_join:
            return render(request, 'content_join.html', {'content': content})
        else:
            return render(request, 'content_ticket_lost.html', {'content': content})
    else:
        content = Content.objects.get(id=id)

        content_join = ContentJoin()
        content_join.user = request.user
        content_join.content = content
        content_join.application_date = datetime.now()
        content_join.status = 1 # status pending
        content_join.save()
        return render(request, 'content_ticket.html', {'content': content})

@login_required
def contentfile_upload(request):
    storage_client = storage.Client()
    transport = AuthorizedSession(credentials=storage_client._credentials)
    bucket = settings.GCP_BUCKET_NAME
    file = request.FILES.get('file', False)
    if (file):
        fileInfo = MediaInfo.parse(file)
        f_type = False
        # TODO: need to check the file size of the video, allowed size is 10mb of free users?
        for track in fileInfo.tracks:
            if track.track_type == "Image":
                f_type = track.track_type
            elif track.track_type == "Video":
                f_type = track.track_type
    if (f_type):
        file.open()
        data = file.read()
        file.close()
        url_template = (
            u'https://www.googleapis.com/upload/storage/v1/b/{bucket}/o?uploadType=resumable')
        upload_url = url_template.format(bucket=bucket)
        chunk_size = 1024 * 1024  # 1MB
        upload = ResumableUpload(upload_url, chunk_size)
        stream = io.BytesIO(data)
        ext = Path(file.name).suffix
        filename = settings.GCP_FOLDER_UPLOAD + "/" + "_".join(["file", datetime.now().strftime("%y%m%d_%H%M%S") + ext])
        metadata = {u'name': filename, }
        content_type = u'image/png'
        response = upload.initiate(transport, stream, metadata, content_type)
        response0 = upload.transmit_next_chunk(transport)
        return JsonResponse({'status':'success'}, status=200, safe=False)

    return JsonResponse({'status':'failed'}, status=400, safe=False)

def get_contents(request):  # common
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            contents = Content.objects.filter(
                title__icontains = query, target_date__gt=time_threshold).annotate(total_attendees=Count('contentjoin')).order_by('-target_date')
        else:
            contents = Content.objects.filter(
                target_date__gt=time_threshold).annotate(total_attendees=Count('contentjoin')).order_by('-target_date')
        page = request.GET.get('page', 1)
        paginator = Paginator(contents, 20)
        contents = paginator.page(page)
    return contents

# APIs
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def content_collection(request):
    contents = get_contents(request)
    serializer = ContentSerializer(contents, many=True)
    return Response(serializer.data)


# Manage own
@login_required
def own_contents(request):
    query = request.GET.get('q')
    if query:
        contents = Content.objects.filter(
            title__icontains = query, user_id = request.user.id).annotate(total_attendees=Count('contentjoin')).order_by('-created_at')
    else:
        contents = Content.objects.filter(
            user_id = request.user.id).annotate(total_attendees=Count('contentjoin')).order_by('-created_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(contents, 20)
    contents = paginator.page(page)
    return render(request, 'manage/own_contents.html', {
        'my_contents': contents,
    })

@login_required
def own_content_edit(request, id):
    content = get_object_or_404(Content, id=id)
    content_form = ContentForm(request.POST or None, instance = content, edit_check = True)
    if request.method == 'POST':
        if content_form.is_valid():
            content_form.save()
        return redirect('own_contents')
    else:
        return render(request, 'manage/own_content_edit.html', {
            'content_form': content_form,
            'content': content
        })

@login_required
def own_content_delete(request, id):
    content = get_object_or_404(Content, id=id)
    return render(request, 'manage/own_content_delete.html', {
        'content': content
    })

@login_required
def own_content_details(request, id):
    dtabs = ['prim', 'attnds']
    dtab = request.GET.get('dtab')
    if dtab not in dtabs:
        dtab = None
    content = get_object_or_404(Content, id=id)
    return render(request, 'manage/details/dets_tab.html', {
        'content': content,
        'dtab': dtab
    })

@login_required
def notifs(request):
    system = []
    messages = []
    ntabs = ['msg', 'anncmnt']
    ntab = request.GET.get('ntab')
    if ntab not in ntabs:
        ntab = None
    return render(request, 'notifs/ntf_tab.html', {
        'system': system,
        'messages': messages,
        'ntab': ntab
    })