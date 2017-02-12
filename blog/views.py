from urllib import quote_plus
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404,redirect,render_to_response,redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .forms import PostForm,UserLoginForm,UserRegisterForm
from .models import Post
from comments.forms import CommentForm
from comments.models import Comment
from django.contrib.auth import (authenticate,get_user_model,login,logout,)
from django.contrib.auth.decorators import login_required
from .utils import get_read_time

def base(request):
    context = RequestContext(request)
    return render_to_response('base.html', context)

def login_view(request):
    form=UserLoginForm(request.POST or None)
    next=request.GET.get('next')
    if form.is_valid() :
         username = form.cleaned_data.get("username")
         password = form.cleaned_data.get("password")
         user=authenticate(username=username,password=password)
         login(request,user)
         if next:
             return redirect(next)
         return redirect("/")
    return render(request,"login.html",{"form":form})

def logout_view(request):
    logout(request)
    return redirect("/")

def register_view(request):
    form=UserRegisterForm(request.POST or None)
    next=request.GET.get('next')
    if form.is_valid() :
        user = form.save(commit=False)
        password=form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        new_user=authenticate(username=user.username,password=password)
        login(request,new_user)
        if next:
            return redirect(next)
        return redirect("/")
    context = {
        "form": form,
    }
    return render(request,"login.html",context)

@login_required(login_url='/login')
def post_create(request):
    form = PostForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user=request.user
        instance.save()
        # message success
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_detail(request,id): #retrieve
    instance = get_object_or_404(Post, id=id)
    share_string=quote_plus(instance.content)
    comment_form=CommentForm(request.POST)
    if comment_form.is_valid():
        print(comment_form.cleaned_data)

    baseurl = request.build_absolute_uri()
    content_type = ContentType.objects.get_for_model(Post)
    obj_id = instance.id
    comments = Comment.objects.filter(content_type=content_type, object_id=obj_id)

    context = {
        "title": instance.title,
        "instance": instance,
        "baseurl" :baseurl,
        "share_string" : share_string,
        "comments" : comments,
        "comment_form" :comment_form,
    }
    return render(request, "post_detail.html", context)


def post_list(request): #list items
    queryset_list = Post.objects.all().order_by("-timestamp")
    query=request.GET.get("q")
    if query:
        queryset_list=queryset_list.filter(title__icontains=query)
    paginator = Paginator(queryset_list, 5) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
# If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
# If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)


    context = {
        "object_list": queryset,
        "title": "List"
            }
    return render(request, "index.html", context)


def post_update(request,id=None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None,request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form":form,
    }
    return render(request, "post_form.html", context)





@login_required(login_url='/login')
def post_delete(request,id=None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    queryset = Post.objects.all()
    context = {
        "object_list": queryset,
        "title": "List"
            }
    messages.success(request, "Successfully deleted")
    return render(request,"index.html",context)
