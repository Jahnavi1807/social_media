from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Mentorship, User
from .forms import MentorshipForm, MentorshipAcceptanceForm
from django.http import HttpResponse
from .forms import MentorshipRequestForm, MentoringRequestForm


#MentorshipRequest
from functools import wraps
from django.shortcuts import redirect

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
        form = MentorshipRequestForm(user, request.POST)
        if form.is_valid():
            mentorship_request = form.save(commit=False)
            mentorship_request.mentee = user
            mentorship_request.save()
            messages.success(request, "Mentorship request sent successfully.")
            return redirect('mentoring:request_list')
    else:
        form = MentoringRequestForm(user)
    return render(request, 'mentoring/mentorship_request.html', {'form': form})



@user_passes_test(lambda u: u.is_staff)
def mentorship_requests(request):
    mentorship_requests = Mentorship.objects.all()
    return render(request, 'mentoring/requests.html', {'mentorship_requests': mentorship_requests})


@login_required
#@mentor_required
def mentorship_request_acceptance(request, pk):
    mentorship_request = get_object_or_404(MentorshipRequest, pk=pk)
    mentor = mentorship_request.mentor
    mentee = mentorship_request.mentee
    mentorship = Mentorship(mentor=mentor, mentee=mentee)
    form = MentorshipAcceptanceForm(request.POST or None, instance=mentorship)
    if form.is_valid():
        form.save()
        mentorship_request.accept()
        return redirect('mentoring:mentorship_list')
    return render(request, 'mentoring/mentorship_request_acceptance.html', {'form': form})


def index(request):
    mentorship_requests = Mentorship.objects.filter(accepted_at__isnull=True)
    print(mentorship_requests)
    context = {'mentorship_requests': mentorship_requests}
    return render(request, 'mentoring/index.html', context)


# def create_request(request):
#     if request.method == 'POST':
#         form = MentorshipForm(request.POST)
#         if form.is_valid():
#             mentorship = form.save(commit=False)
#             mentorship.mentee = request.user
#             mentorship.save()
#             messages.success(request, 'Your mentorship request has been submitted.')
#             return redirect('mentoring:index')
#     else:
#         form = MentorshipForm()
#     return render(request, 'mentoring/request.html', {'form': form})

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
