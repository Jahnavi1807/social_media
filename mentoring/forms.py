from django import forms
from django.contrib.auth.models import User
from .models import Mentorship
from .models import MentorshipRequest
from App_login.models import Follow

# class MentoringRequestForm(forms.ModelForm):
#     mentor = forms.ModelChoiceField(queryset=None)

#     class Meta:
#         model = MentorshipRequest
#         fields = ['title', 'description']

#     def __init__(self, user, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['mentor'].queryset = User.objects.filter(
#             id__in=user.following.values_list('following_id', flat=True)
#         )

#     def clean(self):
#         cleaned_data = super().clean()
#         mentor = cleaned_data.get('mentor')
#         mentee = self.instance.mentee if self.instance else self.initial.get('mentee')
#         if mentor == mentee:
#             raise forms.ValidationError("Mentor and mentee cannot be the same.")
#         return cleaned_data

class MentoringRequestForm(forms.ModelForm):
    class Meta:
        model = MentorshipRequest
        fields = ['title', 'description', 'mentor']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.mentee = user
        self.fields['mentor'].queryset = User.objects.filter(
            id__in=Follow.objects.filter(follower=user.id).values_list('following_id', flat=True)
        )

    def clean(self):
        cleaned_data = super().clean()
        mentor = cleaned_data.get('mentor')
        mentee = self.mentee
        if mentor == mentee:
            raise forms.ValidationError("Mentor and mentee cannot be the same.")
        return cleaned_data


class MentorshipForm(forms.ModelForm):
    mentor = forms.ModelChoiceField(queryset=User.objects.all())

    class Meta:
        model = Mentorship
        fields = ['mentor']
        widgets = {
            'mentor': forms.Select(attrs={'class': 'form-control'})
        }


class MentorshipAcceptanceForm(forms.ModelForm):
    class Meta:
        model = Mentorship
        fields = ['mentor', 'mentee']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
