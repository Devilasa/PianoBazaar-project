from dataclasses import fields
from datetime import date

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

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
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Insert first Name', 'class': 'form-control'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Insert last Name', 'class': 'form-control'}))

    class Meta:
        model = Profile
        exclude = ['user', 'liked_scores', 'purchased_scores', 'shopping_cart']

        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'mantra': forms.Textarea(attrs={'rows': 3}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'youtube_account_id': forms.TextInput(attrs={'placeholder': 'Insert yt id or link to the account'}),
            'instagram_account_id': forms.TextInput(attrs={'placeholder': 'Insert ig id or link to the account'}),
            'x_account_id': forms.TextInput(attrs={'placeholder': 'Insert x id or link to the account'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bio'].help_text = "Write a short bio about yourself."
        self.fields['mantra'].help_text = "Write a short phrase or statement that inspires and motivates you."


    field_order = ['first_name', 'last_name', 'profile_image', 'bio', 'mantra', 'birth_date',
                   'youtube_account_id', 'instagram_account_id', 'x_account_id']

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age <= 18 :
            raise forms.ValidationError('You have to be at least 18 to sign up.')
        return birth_date

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        if commit:
            user.save()
            profile.save()
        return profile

class StaffUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email",]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].help_text = "Staff member email."

    def clean_email(self):
        email = self.cleaned_data.get('email') # ottieni il valore corrente del campo email dopo che ha superato i test di validazione fatti fino a questo momento
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit)
        user.is_staff = True
        # g = Group.objects.get(name="Staff Member")
        # g.user_set.add(user)
        return user
