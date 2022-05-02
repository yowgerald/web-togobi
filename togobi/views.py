from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone

from togobi.forms import ContentForm, ContentJoinForm
from togobi.models import Content, ContentJoin

# Create your views here.

def content_list(request):
    return render(request, 'home.html', {})

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
        content_join.status = 2 # status pending
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
    content_form = ContentForm(request.POST or None, instance = content)
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
def attendees_list(request, id):
    content_join = ContentJoin.objects.filter(content_id=id).select_related('user')
    return render(request, 'manage/attendees/attendees.html', {
        'content_join': content_join
    })

@login_required
def attendee_edit(request, id, attendee_id):
    content_join = get_object_or_404(ContentJoin, content_id=id, user_id=attendee_id)
    content_join_form = ContentJoinForm(request.POST or None, instance=content_join)
    if request.method == 'POST':
        if content_join_form.is_valid():
            content_join_form.save()
            return redirect('own_content_attendees', content_join.content_id)
    else:
        return render(request, 'manage/attendees/edit.html', {
            'content_join_form': content_join_form, 
            'content_join': content_join
        })
