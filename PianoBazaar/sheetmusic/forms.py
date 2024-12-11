from decimal import Decimal

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, HTML, Field, Fieldset
from django import forms
from django.template.defaultfilters import title, default, floatformat

from sheetmusic.models import Score


class CreateSheetForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'add sheetmusic form'
    helper.form_method = 'POST'
    helper.layout = Layout(
        Field('title', css_class='form-control', placeholder='Insert title'),
                Field('arranger', css_class='form-control', title='ARRANGER'),
                Field('price', css_class='form-control', step='0.01', min='0', placeholder='Insert price'),
                Field('scoring', css_class='form-control', title='SCORING'),
                Field('score_type', css_class='form-control', title='SCORE TYPE'),
                Field('genre_1', css_class='form-control', title='GENRE 1'),
                Field('genre_2', css_class='form-control', title='GENRE 2'),
                Field('published_key', css_class='form-control', title='PUBLISHED KEY'),
                Field('pages_number', css_class='form-control', title='PAGES NUMBER'),
                Field('file', title='FILE'),
                Field('youtube_id_video', css_class='form-control', title='YOUTUBE ID VIDEO'),
        )
    helper.add_input(Submit('submit', 'Add sheetmusic'))

    class Meta:
        model = Score
        fields = '__all__'
