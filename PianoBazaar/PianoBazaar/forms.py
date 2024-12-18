from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from sheetmusic.models import Profile

class UserCreateForm(UserCreationForm):
    # bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2}))
    # email = forms.EmailField(required=True, unique=True)

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


class ProfileCreationForm(UserCreationForm, forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'profile creation form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Create Profile', css_class='btn btn-primary'))

    class Meta:
        model = Profile
        exclude = ['purchased_scores']
