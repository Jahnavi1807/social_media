from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
# Create your views here.
from App_login.models import UserProfile, Follow
from django.contrib.auth.models import User

from App_Posts.models import Post, Like
from django.conf import settings
# @login_required
# def home(request):
# 	if request.method== "GET":
# 		search = request.GET.get('search')
# 		result  = User.objects.filter(username__icontains=search)

# 	return render(request,'App_Posts/home.html',context={'title':'Home Page','search':search,'result':result})
@login_required
def home(request):
    following_list = Follow.objects.filter(follower=request.user)
    posts = Post.objects.filter(author__in=following_list.values_list('following'))
    liked_post = Like.objects.filter(user=request.user)
    liked_post_list = liked_post.values_list('post', flat=True)

    search = request.GET.get('search')
    result = None  # Initialize result to None

    if search:  # Check if search is not None
        result = User.objects.filter(username__icontains=search)

    context = {'title': 'Home Page', 'search': search, 'result': result,'posts':posts, 'liked_post_list':liked_post_list}
    return render(request, 'App_Posts/home.html', context)

@login_required
def liked(request, pk):
    post = Post.objects.get(pk= pk)
    already_liked = Like.objects.filter(post=post, user=request.user)
    if not already_liked:
        liked_post = Like(post=post,user=request.user)
        liked_post.save()
    return HttpResponseRedirect(reverse('home'))

@login_required
def unliked(request,pk):
    post = Post.objects.get(pk= pk)
    already_liked = Like.objects.filter(post=post, user=request.user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('home'))




def search_news(request):
    query = request.GET.get('query')
    api_key = settings.TIDALWAVES_API_KEY
    url = f'https://api.tidalwaves.io/v1/news?query={query}'
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(url, headers=headers)
    data = response.json()
    return render(request, 'App_Posts/news.html', {'news': data['articles'], 'query': query})
