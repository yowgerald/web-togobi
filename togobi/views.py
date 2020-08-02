from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from togobi.models import Content
from togobi.serializers import ContentSerializer
from datetime import datetime, timedelta
from django.core.paginator import Paginator

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

# Create your views here.


def content_list(request):
    contents = get_contents(request)
    return render(request, 'home.html', {'contents': contents})


def content_details(request, id):
    if request.method == 'GET':
        content = Content.objects.get(id=id)
    return render(request, 'content_details.html', {'content': content})


def content_add(request):
    return render(request, 'content_add.html', {})


def content_join(request, id):
    return render(request, 'content_join.html', {})


def get_contents(request):
    if request.method == 'GET':
        time_threshold = datetime.now() + timedelta(hours=5)
        contents = Content.objects.filter(
            target_date__gt=time_threshold).order_by('-target_date')
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
