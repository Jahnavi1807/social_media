#from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import MentorshipRequest, Mentorship

admin.site.register(MentorshipRequest)
admin.site.register(Mentorship)

