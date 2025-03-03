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
    
    def __init__(self, *args, title=None, **kwargs):
        super().__init__(*args, **kwargs)
        if title:
            self.fields['title'].initial = title
            self.fields['title'].widget = forms.HiddenInput()


class GraphicTitleChapterForm(forms.ModelForm):
    class Meta:
        model = GraphicTitleChapter
        fields = ['title', 'chapter_name']
    
    def __init__(self, *args, title=None, **kwargs):
        super().__init__(*args, **kwargs)
        if title:
            self.fields['title'].initial = title
            self.fields['title'].widget = forms.HiddenInput()


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class GraphicTitlePageForm(forms.ModelForm):
    image = MultipleFileField(label='Select files', required=False)
    
    class Meta:
        model = GraphicTitlePage
        fields = ['page_number', 'image']


# allows uploading multiple pages
GraphicTitlePageFormSet = forms.modelformset_factory(
    GraphicTitlePage,
    form=GraphicTitlePageForm,
    extra=10,
    can_delete=True
)
