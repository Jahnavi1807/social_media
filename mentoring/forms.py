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
    mentor = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = MentorshipRequest
        fields = ['title', 'description']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mentor'].queryset = User.objects.filter(
            id__in=user.following.values_list('following_id', flat=True)
        )

    def clean(self):
        cleaned_data = super().clean()
        mentor = cleaned_data.get('mentor')
        mentee = self.instance.mentee if self.instance else self.initial.get('mentee')
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



from .models import MentorshipRequest

class MentorshipRequestForm(forms.ModelForm):
    mentor = forms.CharField(widget=forms.HiddenInput())
    
    class Meta:
        model = Mentorship
        fields = ['mentee', 'mentor', 'subject', 'message']
        widgets = {
            'mentor': forms.HiddenInput(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }



class MentorshipAcceptanceForm(forms.ModelForm):
    class Meta:
        model = Mentorship
        fields = ['mentor', 'mentee']


class MentoringRequestForm(forms.ModelForm):
    mentor = forms.ModelChoiceField(queryset=User.objects.filter(is_mentor=True))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))

    class Meta:
        model = MentoringRequest
        fields = ('mentor', 'message')