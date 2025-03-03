"""Contains forms for 'main' app"""
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from . models import TextTitle, GraphicTitle, TextTitleChapter, GraphicTitleChapter, GraphicTitlePage

class TextTitleForm(forms.ModelForm):
    class Meta:
        model = TextTitle
        fields = ['title_name_rus', 
                  'title_name_eng', 
                  'title_author', 
                  'title_is_ongoing',
                  'title_description', 
                  'publication_year']
        labels = {
            'title_name_rus': _('Название тайтла'),
            'title_name_eng': _('Название тайтла (английский, опционально)'), 
            'title_author': _('Автор'), 
            'title_is_ongoing': _('Статус'),
            'title_description': _('Описание'), 
            'publication_year': _('Год выпуска')
        }
        widgets = {
            'title_name_rus': forms.TextInput(attrs={'placeholder': 'Введите название', 'class': 'form-control'}),
            'title_name_eng': forms.TextInput(attrs={'placeholder': 'Введите название (если есть)', 'class': 'form-control'}),
            'title_author': forms.TextInput(attrs={'placeholder': 'Автор', 'class': 'form-control'}),
            'title_is_ongoing': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'title_description': forms.Textarea(attrs={'placeholder': 'Введите описание...', 'class': 'form-control', 'rows': 4}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        


class GraphicTitleForm(forms.ModelForm):
    class Meta:
        model = GraphicTitle
        fields = ['title_name_rus', 
                  'title_name_eng', 
                  'title_author', 
                  'title_is_ongoing',
                  'title_description', 
                  'publication_year']
        labels = {
            'title_name_rus': _('Название тайтла'),
            'title_name_eng': _('Название тайтла (английский, опционально)'), 
            'title_author': _('Автор'), 
            'title_is_ongoing': _('Статус'),
            'title_description': _('Описание'), 
            'publication_year': _('Год выпуска')
        }        
        widgets = {
            'title_name_rus': forms.TextInput(attrs={'placeholder': 'Введите название', 'class': 'form-control'}),
            'title_name_eng': forms.TextInput(attrs={'placeholder': 'Введите название (если есть)', 'class': 'form-control'}),
            'title_author': forms.TextInput(attrs={'placeholder': 'Автор', 'class': 'form-control'}),
            'title_is_ongoing': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'title_description': forms.Textarea(attrs={'placeholder': 'Введите описание...', 'class': 'form-control', 'rows': 4}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class TextTitleChapterForm(forms.ModelForm):
    class Meta:
        model = TextTitleChapter
        fields = ['title', 
                  'chapter_name', 
                  'chapter_number',
                  'text_content']
        labels = {
            'title': _('Тайтл'), 
            'chapter_name': _('Название главы'), 
            'chapter_number': _('Номер главы'),
            'text_content': _('Содержание главы')
        }
    
    def __init__(self, *args, title=None, **kwargs):
        super().__init__(*args, **kwargs)
        if title:
            self.fields['title'].initial = title
            self.fields['title'].widget = forms.HiddenInput()


class GraphicTitleChapterForm(forms.ModelForm):
    class Meta:
        model = GraphicTitleChapter
        fields = ['title', 
                  'chapter_name', 
                  'chapter_number']
        labels = {
            'title': _('Тайтл'), 
            'chapter_name': _('Название главы'), 
            'chapter_number': _('Номер главы')
        }
    
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
        fields = ['chapter', 
                  'page_number', 
                  'image']
        labels = {
            'chapter': _('Глава'), 
            'page_number': _('Номер страницы'), 
            'image': _('Страница (изображение)')
        }
        
    def __init__(self, *args, chapter=None, **kwargs):
        super().__init__(*args, **kwargs)
        if title:
            self.fields['chapter'].initial = chapter
            self.fields['chapter'].widget = forms.HiddenInput()


# allows uploading multiple pages
GraphicTitlePageFormSet = forms.modelformset_factory(
    GraphicTitlePage,
    form=GraphicTitlePageForm,
    extra=3,
    can_delete=True
)
