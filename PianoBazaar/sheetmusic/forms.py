from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.templatetags.crispy_forms_field import css_class
from django import forms

from sheetmusic.models import Score


class ScoreCreateForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'load sheetmusic form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Upload sheetmusic', css_class='mt-2'))

    class Meta:
        model = Score
        exclude = ['publication_date', 'pages', 'cover']

        widgets = {
            'title' : forms.TextInput(attrs={'placeholder': 'Insert title'}),
            'youtube_video_link' : forms.TextInput(attrs={'placeholder': 'https://www.youtube.com/watch?v=dD1Y6LiSBVo'}),
        }
