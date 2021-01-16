from django.contrib.auth.models import User
from django.shortcuts import render, redirect
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

from togobi.forms import ContentAddForm, ContentFileAddForm
from togobi.models import Content, ContentFile, ContentBookmark, ContentJoin
from togobi.serializers import ContentSerializer

from google.auth.transport.requests import AuthorizedSession
from google.resumable_media.requests import MultipartUpload
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
    contents_bookmark = []
    contents_top = ContentJoin.objects.annotate(distinct_name=Concat(
        'content_id', 'content_id', output_field=TextField())).order_by('distinct_name').distinct('distinct_name')
    if request.user.is_authenticated:
        contents_bookmark = ContentBookmark.objects.filter(
            user = request.user, content__target_date__gt=time_threshold).order_by('-content__target_date')
    return render(request, 'home.html', {
        'contents': contents,
        'contents_today' : contents_today,
        'contents_top' : contents_top,
        'contents_bookmark' : contents_bookmark
        })


def content_details(request):
    if request.method == 'GET':
        content = Content.objects.get(id=request.GET.get("content"))
    return render(request, 'content_details.html', {'content': content})


@login_required
def content_add(request):
    if request.method == 'POST':
        content_form = ContentAddForm(request.POST)
        if content_form.is_valid():
            content = content_form.save(commit=False)
            content.user = request.user
            content.save()

            file = request.FILES.get('source', False)
            fileInfo = MediaInfo.parse(file)
            f_type = False
            # TODO: need to check the file size of the video, allowed size is 10mb of free users?
            for track in fileInfo.tracks:
                if track.track_type == "Image":
                    f_type = track.track_type
                elif track.track_type == "Video":
                    f_type = track.track_type
            if (file and f_type):
                storage_client = storage.Client()
                transport = AuthorizedSession(credentials=storage_client._credentials)
                bucket = settings.GCP_BUCKET_NAME
                # TODO: need refactor
                file.open()
                data = file.read()
                file.close()
                url_template = (
                    u'https://www.googleapis.com/upload/storage/v1/b/{bucket}/o?uploadType=multipart')
                upload_url = url_template.format(bucket=bucket)
                upload = MultipartUpload(upload_url)
                ext = Path(file.name).suffix
                filename = "_".join(["file", datetime.now().strftime("%y%m%d_%H%M%S") + ext])
                metadata = {u'name': filename, }
                response = upload.transmit(
                    transport, data, metadata, file.content_type)
                content_file = ContentFile()
                content_file.source = filename
                content_file.f_type = f_type
                content_file.content = content
                content_file.save()
            return render(request, 'content_details.html', {'content': content})
        else:
            print('not valid')
    else:
        content_form = ContentAddForm(initial={})
    # TODO: catch exception, saying internet speed is not good for uploading
    context = {
        'content_form': content_form,
        'content_file_form': ContentFileAddForm(initial={}),
    }
    return render(request, 'content_add.html', context)


@login_required
def content_join(request):
    if request.method == 'GET':
        content = Content.objects.get(id=request.GET.get("content"))
        content_join = ContentJoin.objects.filter(
            user=request.user, content=content
        ).first()
        
        if not content_join:
            return render(request, 'content_join.html', {'content': content})
        else:
            return render(request, 'content_ticket_lost.html', {'content': content})
    else:
        content = Content.objects.get(id=request.POST.get("content"))

        content_join = ContentJoin()
        content_join.user = request.user
        content_join.content = content
        content_join.application_date = datetime.now()
        content_join.status = 1 # status pending
        content_join.save()
        return render(request, 'content_ticket.html', {'content': content})


def content_bookmark(request):
    content = Content.objects.get(id=request.POST.get("content"))
    user = User.objects.get(id=request.POST.get("user"))
    if content and user:
        content_bookmark = ContentBookmark.objects.filter(
            content=content, user=user
        ).first()
        if not content_bookmark:
            content_bookmark = ContentBookmark()
            content_bookmark.content = content
            content_bookmark.user = user
            content_bookmark.save()
            return JsonResponse({'success': 'true'})

    return JsonResponse({'success': 'false'})


def get_contents(request):  # common
    if request.method == 'GET':
        contents = Content.objects.filter(
            target_date__gt=time_threshold).annotate(total_attendees=Count('contentjoin')).order_by('-target_date')
        page = request.GET.get('page', 1)
        paginator = Paginator(contents, 10)
        contents = paginator.page(page)
    return contents

# APIs
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def content_collection(request):
    contents = get_contents(request)
    serializer = ContentSerializer(contents, many=True)
    return Response(serializer.data)
