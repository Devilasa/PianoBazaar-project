from datetime import date

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
            'birth_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'youtube_account_id': forms.TextInput(attrs={'placeholder': 'insert yt id or link to the account'}),
            'instagram_account_id': forms.TextInput(attrs={'placeholder': 'insert ig id or link to the account'}),
            'x_account_id': forms.TextInput(attrs={'placeholder': 'insert x id or link to the account'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bio'].help_text = "Write a short bio about yourself."
        self.fields['mantra'].help_text = "Write a short phrase or statement that inspires and motivates you."

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age <= 18 :
            raise forms.ValidationError('You have to be at least 18 to sign up.')
        return birth_date

