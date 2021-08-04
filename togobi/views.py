from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import timedelta, date
from django.db.models import Count, TextField, Q
from django.db.models.functions import Concat
from django.utils import timezone
from pathlib import Path
from pymediainfo import MediaInfo

from togobi.forms import ContentForm
from togobi.models import Content, ContentFile, ContentJoin
from togobi.serializers import ContentSerializer, ContentFileSerializer, ContentTopSerializer

from google.auth.transport.requests import AuthorizedSession
from google.resumable_media.requests import ResumableUpload
import io
import os
from google.cloud import storage

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

# Create your views here.
time_threshold = timezone.now() + timedelta(hours=1)

def content_list(request):
    return render(request, 'home.html', {})

def get_filetype(file):
    fileInfo = MediaInfo.parse(file)
    _type = False
    for track in fileInfo.tracks:
        if track.track_type == "Image":
            _type = track.track_type
        elif track.track_type == "Video":
            _type = track.track_type
    return _type

@login_required
def content_add(request):
    if request.method == 'POST':
        content_form = ContentForm(request.POST)
        if content_form.is_valid():
            content = content_form.save(commit=False)
            content.user = request.user
            content.creation_step = 2
            content.save()
            return redirect('own_content_edit', content.id)
        else:
            # TODO: change back creation_step?
            # TODO: return with error
            print('not valid')
    else:
        return render(request, 'content_add.html', {})

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
        content_join.application_date = timezone.now()
        content_join.status = 1 # status pending
        content_join.save()
        return render(request, 'content_ticket.html', {'content': content})

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
    content = get_object_or_404(Content, id=id, user_id=request.user)
    content_form = ContentForm(request.POST or None, instance = content, edit_check = True)
    if request.method == 'POST':
        if content_form.is_valid():
            content_form.save()
        return redirect('own_content_edit', id=id)
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

# TODO: return status codes of all api call
# APIs
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def form_content(request):
    content_form = ContentForm(initial={})
    id = request.GET.get('id', False)
    if (id):
        content = get_object_or_404(Content, id=id, user_id=request.user)
        content_form = ContentForm(request.POST or None, instance = content, edit_check = True)
    content_form = content_form.as_p()
    return Response({
        'form': str(content_form)
    })

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def content_collection(request):
    # TODO: search also by location
    query = request.GET.get('q')
    if query:
        lookups= (Q(title__icontains=query) | Q(description__icontains=query) | Q(tags__icontains=query)
            | Q(user__username__icontains=query))
        contents = Content.objects.filter(
            lookups, target_date__gt=time_threshold).annotate(total_attendees=Count('contentjoin')).order_by('-target_date')
    else:
        contents = Content.objects.filter(
            target_date__gt=time_threshold).annotate(total_attendees=Count('contentjoin')).order_by('-target_date')
    page = request.GET.get('page', 1)
    paginator = Paginator(contents, 20)
    contents = paginator.page(page)
    serializer = ContentSerializer(contents, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def content_file_collection(request, id):
    content_files = ContentFile.objects.filter(content=id, is_active=True).order_by('f_type').reverse()
    page = request.GET.get('page')
    paginator = Paginator(content_files, 5)
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

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def content_file_delete(request, id):
    if (id):
        storage_client = storage.Client()
        bucket = storage_client.bucket(settings.GCP_BUCKET_NAME)

        content_file = get_object_or_404(ContentFile, id = id)
        blob = bucket.blob(content_file.source)
        blob.delete()
        content_file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def contents_today(request):
    cs_today = Content.objects.filter(
            target_date__day=date.today().day).order_by('-target_date')
    serializer = ContentSerializer(cs_today, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def contents_top(request):
    # TODO: may need to return the number of attendees
    t_contents = ContentJoin.objects.annotate(distinct_name=Concat(
        'content_id', 'content_id', output_field=TextField())).order_by('distinct_name').distinct('distinct_name')
    serializer = ContentTopSerializer(t_contents, many=True)
    return Response(serializer.data)

def __gen_signed_url(file):
    url = None
    if file is not None:
        client = storage.Client()
        bucket = client.get_bucket(settings.GCP_BUCKET_NAME)
        blob = bucket.get_blob(file)
        expiration = timezone.now() + timedelta(hours=1)
        url = blob.generate_signed_url(expiration=expiration)
    return url

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def contentfile_upload(request, id):
    # TODO: may need to be in try catch
    storage_client = storage.Client()
    transport = AuthorizedSession(credentials=storage_client._credentials)
    bucket = settings.GCP_BUCKET_NAME

    file = request.data.get('file', False)
    if not file or not get_filetype(file):
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
    filename = settings.GCP_FOLDER_UPLOAD + "/" + "_".join(["file", timezone.now().strftime("%y%m%d_%H%M%S") + ext])
    metadata = {u'name': filename, }
    content_type = u'image/png'
    response = upload.initiate(transport, stream, metadata, content_type)
    content = get_object_or_404(Content, id=id)
    while not upload.finished:
        upload.transmit_next_chunk(transport)
    content_file = ContentFile()
    content_file.source = filename
    content_file.f_type = f_type
    content_file.content = content
    content_file.save()

    serializer = ContentFileSerializer(content_file)
    return Response({
        'result': serializer.data
    })
