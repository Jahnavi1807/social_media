# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser



# class Mentorship(models.Model):
#     mentor = models.ForeignKey(User, related_name='mentorship_mentor', on_delete=models.CASCADE)
#     mentee = models.ForeignKey(User, related_name='mentorship_mentee', on_delete=models.CASCADE)
#     title = models.CharField(max_length=255, default='Untitled')
#     description = models.TextField(blank=True)
#     created_at = models.DateTimeField(default=timezone.now)
#     accepted_at = models.DateTimeField(null=True, blank=True, default=None)

#     def accept(self):
#         self.accepted_at = timezone.now()
#         self.save()

#     def decline(self):
#         self.delete()


# # class MentorshipRequest(models.Model):
# #     mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentee_requests')
# #     mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentor_requests')
# #     created_at = models.DateTimeField(auto_now_add=True)
# #     status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending')

# #     def accept(self):
# #         self.status = 'accepted'
# #         self.save()

# #     def decline(self):
# #         self.status = 'declined'
# #         self.save()

# class MentorshipRequest(models.Model):
#     mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentor_requests')
#     mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentee_requests')
#     title = models.CharField(max_length=255, blank=True)
#     description = models.TextField(blank=True)
#     status_choices = (
#         ('PENDING', 'Pending'),
#         ('ACCEPTED', 'Accepted'),
#         ('REJECTED', 'Rejected')
#     )
#     status = models.CharField(max_length=10, choices=status_choices, default='PENDING')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'Mentorship request from {self.mentee.username} to {self.mentor.username}'
#     def clean(self):
#         if self.mentor == self.mentee:
#             raise ValidationError("You cannot request mentorship from yourself.")




# class User(AbstractUser):
#     is_mentor = models.BooleanField(default=False)
    
#     # Add related_name argument to avoid clashes with auth app
#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='mentoring_users',
#         blank=True,
#         help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
#         verbose_name='groups',
#     )
    
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='mentoring_users',
#         blank=True,
#         help_text='Specific permissions for this user.',
#         verbose_name='user permissions',
#     )

class Mentorship(models.Model):
    mentor = models.ForeignKey(User, related_name='mentorship_mentor', on_delete=models.CASCADE)
    mentee = models.ForeignKey(User, related_name='mentorship_mentee', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default='Untitled')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    accepted_at = models.DateTimeField(null=True, blank=True, default=None)

    def accept(self):
        self.accepted_at = timezone.now()
        self.save()

    def decline(self):
        self.delete()


class MentorshipRequest(models.Model):
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentor_requests')
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentee_requests')
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    status_choices = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected')
    )
    status = models.CharField(max_length=10, choices=status_choices, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Mentorship request from {self.mentee.username} to {self.mentor.username}'
    
    def clean(self):
        if self.mentor == self.mentee:
            raise ValidationError("You cannot request mentorship from yourself.")
