from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Mentorship, User, MentorshipRequest
from .forms import MentorshipForm, MentorshipAcceptanceForm
from django.http import HttpResponse
from .forms import MentoringRequestForm
from functools import wraps
from django.shortcuts import redirect
import requests
import json

API_KEY = 'bb54bf85ce07f436c71736d80745cd09d63e6879'
APP_ID = '2376329b22aae31d'

def create_group(group_name, owner_id, members):
    url = f'https://2376329b22aae31d.api-us.cometchat.io/v3'
    headers = {
        'Content-Type': 'application/json',
        'appId': APP_ID,
        'apiKey': API_KEY,
    }
    data = {
        'name': group_name,
        'type': 'public',
        'owner': str(owner_id),
        'members': members,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['data']['guid']
    else:
        raise ValueError(f'Error creating group: {response.json()}')



def create_chatroom(mentor_id, mentee_id, app_id, api_key):
    url = f'https://2376329b22aae31d.api-us.cometchat.io/v3'
    headers = {'Content-Type': 'application/json', 'apiKey': API_KEY, 'appId': APP_ID}
    data = {
        'name': f'{mentor_id}_and_{mentee_id}',
        'type': 'private',
        'members': [mentor_id, mentee_id]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        chatroom_id = response.json()['data']['guid']
        print(f'Successfully created chatroom with ID {chatroom_id}')
    else:
        print(f'Error creating chatroom: {response.json()}')



def mentor_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_mentor:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrapper

@login_required
def mentorship_request(request):
    user = request.user
    if request.method == 'POST':
        form = MentoringRequestForm(user, request.POST)
        if form.is_valid():
            mentorship_request = form.save(commit=False)
            mentorship_request.mentee = user
            mentorship_request.save()
            messages.success(request, "Mentorship request sent successfully.")
            return redirect('mentoring:mentorship_list')
    else:
        form = MentoringRequestForm(user)
    return render(request, 'mentoring/mentorship_request.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
def mentorship_requests(request):
    mentorship_requests = Mentorship.objects.all()
    return render(request, 'mentoring/requests.html', {'mentorship_requests': mentorship_requests})

# @login_required
# #@mentor_required
# def mentorship_request_acceptance(request, pk):
#     mentorship_request = get_object_or_404(MentorshipRequest, pk=pk)
#     if request.method == 'POST':
#         mentorship = Mentorship(mentor = mentorship_request.mentor, mentee = mentorship_request.mentee, title = mentorship_request.title, description = mentorship_request.description)
#         mentorship.accept()
#         return redirect('mentoring:mentorship_list')

#     return render(request, 'mentoring/mentorship_request_acceptance.html', {'mentorship_request': mentorship_request})

@login_required
@mentor_required
def mentorship_request_acceptance(request, pk):
    mentorship_request = get_object_or_404(MentorshipRequest, pk=pk)
    if request.method == 'POST':
        mentorship = Mentorship(mentor = mentorship_request.mentor, mentee = mentorship_request.mentee, title = mentorship_request.title, description = mentorship_request.description)
        mentorship.accept()

        # Create chat room
        mentor_id = mentorship.mentor.id
        mentee_id = mentorship.mentee.id
        app_id = APP_ID
        api_key = API_KEY
        create_chatroom(mentor_id, mentee_id, app_id, api_key)

        return redirect('mentoring:mentorship_list')

    return render(request, 'mentoring/mentorship_request_acceptance.html', {'mentorship_request': mentorship_request})



def index(request):
    mentorship_requests = MentorshipRequest.objects.filter(mentor_id=request.user.id)
    context = {'mentorship_requests': mentorship_requests}
    return render(request, 'mentoring/index.html', context)

def create_request(request):
    if request.method == 'POST':
        form = MentorshipForm(request.POST)
        if form.is_valid():
            mentorship = form.save(commit=False)
            mentorship.mentee = request.user
            mentorship.mentor = request.user
            mentorship.save()
            messages.success(request, 'Your mentorship request has been submitted.')
            return redirect('mentoring:index')
    else:
        form = MentorshipForm()
    return render(request, 'mentoring/request.html', {'form': form})

def mentorship_list(request):
    mentorships = Mentorship.objects.all()
    return render(request, 'mentoring/mentorship_list.html', {'mentorships': mentorships})
