from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from sheetmusic.models import Profile

class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email",]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].help_text = "Make sure to use an email you have access to, this is where we will send you your digital sheet music."

    def clean_email(self):
        email = self.cleaned_data.get('email') # ottieni il valore corrente del campo email dopo che ha superato i test di validazione fatti fino a questo momento
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email


class ProfileCreationForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ['user', 'purchased_scores']

        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'mantra': forms.Textarea(attrs={'rows': 3}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'YYYY-MM-DD'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_image'].help_text = "This will be shown on your profile page."
        self.fields['bio'].help_text = "Write a short bio about yourself."
        self.fields['mantra'].help_text = "Write a short phrase or statement that inspires and motivates you."
        self.fields['youtube_account_id'].help_text = "You can also drop the link to your channel and we'll extract the id."
        self.fields['instagram_account_id'].help_text = "Or the link to your account."
        self.fields['x_account_id'].help_text = "Or the link to your account."