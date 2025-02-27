"""Contains forms for 'main' app"""
from django import forms
from django.contrib.auth import get_user_model
from . models import TextTitle, GraphicTitle, TextTitleChapter, GraphicTitleChapter, GraphicTitlePage

class TextTitleForm(forms.ModelForm):
    class Meta:
        model = TextTitle
        fields = ['title_name_rus', 'title_name_eng', 'title_author', 'title_description']


class GraphicTitleForm(forms.ModelForm):
    class Meta:
        model = GraphicTitle
        fields = ['title_name_rus', 'title_name_eng', 'title_author', 'title_description']

class TextTitleChapterForm(forms.ModelForm):
    class Meta:
        model = TextTitleChapter
        fields = ['title', 'chapter_name', 'text_content']


class GraphicTitleChapterForm(forms.ModelForm):
    class Meta:
        model = GraphicTitleChapter
        fields = ['title', 'chapter_name']


class GraphicTitlePageForm(forms.ModelForm):
    class Meta:
        model = GraphicTitlePage
        fields = ['chapter', 'image', 'page_number']
