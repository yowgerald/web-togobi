from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date
from django.db.models import Count
from django.db.models import TextField
from django.db.models.functions import Concat
from pathlib import Path
from pymediainfo import MediaInfo

from togobi.forms import ContentForm, ContentFileForm
from togobi.models import Content, ContentFile, ContentJoin
from togobi.serializers import ContentSerializer, ContentFileSerializer

from google.auth.transport.requests import AuthorizedSession
from google.resumable_media.requests import ResumableUpload
import io
import os
from google.cloud import storage

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.
time_threshold = datetime.now() + timedelta(hours=1)

def content_list(request):
    contents = __get_contents(request)
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


def get_filetype(file):
    fileInfo = MediaInfo.parse(file)
    _type = False
    for track in fileInfo.tracks:
        if track.track_type == "Image":
            _type = track.track_type
        elif track.track_type == "Video":
            _type = track.track_type
    return _type

def contentfile_upload(files, content):
    # TODO: may need to be in try catch
    storage_client = storage.Client()
    transport = AuthorizedSession(credentials=storage_client._credentials)
    bucket = settings.GCP_BUCKET_NAME
    valid_files = True
    for file in files:
        if not get_filetype(file):
            valid_files = False
    return True
    if valid_files:
        for file in files:
            f_type = get_filetype(file)
            file.open()
            data = file.read()
            # file.seek(0, os.SEEK_END)
            # fsize = file.tell()
            # TODO: need to check the file size of the video, allowed size is 10mb of free users?
            file.close()
            url_template = (
                u'https://www.googleapis.com/upload/storage/v1/b/{bucket}/o?uploadType=resumable')
            upload_url = url_template.format(bucket=bucket)
            chunk_size = 1024 * 1024  # 1MB or 256 x 1024 bytes (256 KB)
            upload = ResumableUpload(upload_url, chunk_size)
            stream = io.BytesIO(data)
            ext = Path(file.name).suffix
            filename = settings.GCP_FOLDER_UPLOAD + "/" + "_".join(["file", datetime.now().strftime("%y%m%d_%H%M%S") + ext])
            metadata = {u'name': filename, }
            content_type = u'image/png'
            response = upload.initiate(transport, stream, metadata, content_type)
            while not upload.finished:
                upload.transmit_next_chunk(transport)
            content_file = ContentFile()
            content_file.source = filename
            content_file.f_type = f_type
            content_file.content = content
            content_file.save()
        return True
    else:
        return False

@login_required
def content_add(request):
    if request.method == 'POST':
        content_form = ContentForm(request.POST)
        if content_form.is_valid():
            content = content_form.save(commit=False)
            content.user = request.user
            content.save()
            files = request.FILES.getlist('content-file', False)
            if files:
                exclusions = request.POST.get('exclusions', False)
                final_files = []
                if (exclusions):
                    exs = exclusions.split(",")
                    exs[:] = list(map(int, exs))
                    for idx, f in enumerate(files):
                        if idx not in exs:
                            final_files.append(f)
                if (final_files):
                    success_upload = contentfile_upload(final_files, content)
                    if success_upload:
                        return redirect('content_details', id=content.id)
        else:
            print('not valid')
    else:
        content_form = ContentForm(initial={})
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

def __get_contents(request):
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
@permission_classes([IsAuthenticatedOrReadOnly])
def content_collection(request):
    contents = __get_contents(request)
    serializer = ContentSerializer(contents, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def content_file_collection(request, id):
    content_files = ContentFile.objects.filter(content=id, is_active=True)
    page = request.GET.get('page')
    paginator = Paginator(content_files, 2)
    content_files = paginator.page(page)
    next_page = prev_page = None
    if content_files.has_other_pages():
        if content_files.has_next():
            next_page = content_files.next_page_number()
        if content_files.has_previous():
            prev_page = content_files.previous_page_number()
    for cf in content_files:
        cf.signed_url = __gen_signed_url(cf.source)
    serializer = ContentFileSerializer(content_files, many=True)
    return Response({
            'next': next_page,
            'previous': prev_page,
            'result': serializer.data
        })

def __gen_signed_url(file):
    url = None
    if file is not None:
        client = storage.Client()
        bucket = client.get_bucket(settings.GCP_BUCKET_NAME)
        blob = bucket.get_blob(file)
        expiration = datetime.now() + timedelta(hours=1)
        url = blob.generate_signed_url(expiration=expiration)
    return url

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