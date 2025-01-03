from datetime import date

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import ClearableFileInput
from django_countries.fields import CountryField

from sheetmusic.models import Score, BillingProfile, Profile

class ScoreCreateForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'load sheetmusic form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Upload sheetmusic', css_class='mt-2'))

    class Meta:
        model = Score
        exclude = ['arranger', 'publication_date', 'pages', 'cover']

        widgets = {
            'title' : forms.TextInput(attrs={'placeholder': 'Insert title'}),
            'youtube_video_link' : forms.TextInput(attrs={'placeholder': 'https://www.youtube.com/watch?v=dD1Y6LiSBVo'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Insert first Name', 'class': 'form-control'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Insert last Name', 'class': 'form-control'}))
    email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Insert Email', 'class': 'form-control'}))

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
            'profile_image': ClearableFileInput(attrs={'class': 'form-control', 'style': 'min-width: 600px'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['bio'].help_text = "Write a short bio about yourself."
        self.fields['mantra'].help_text = "Write a short phrase or statement that inspires and motivates you."

        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

    field_order = ['first_name', 'last_name', 'email', 'profile_image', 'bio', 'mantra', 'birth_date',
                   'youtube_account_id', 'instagram_account_id', 'x_account_id']

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age <= 18:
            raise forms.ValidationError('You have to be at least 18 to sign up.')
        return birth_date

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        if not profile.profile_image:
            profile.profile_image = 'media/profiles/profile_imgs/profile-default.1024x1023.png'
        if commit:
            user.save()
            profile.save()
        return profile


class CheckoutForm(forms.ModelForm):

    class Meta:
        model = BillingProfile
        exclude = ['user']
        widgets = {
            'receiving_email':forms.TextInput(attrs={'class': 'form-control', 'style': 'font-weight: bold'}),
        }

    country = CountryField(blank_label='Select Country')
    score_receiving_email = forms.TextInput(),

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['receiving_email'].help_text = "Care, this is where we are sending the score pdf, make sure it's right."
        if self.user:
            b_profile = BillingProfile.objects.get(user=self.user)
            if b_profile.receiving_email:
                self.fields['receiving_email'].initial = b_profile.receiving_email
            else:
                self.fields['receiving_email'].initial = self.user.email
