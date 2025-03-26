"""Contains forms for 'main' app"""
from django import forms
from django.utils.translation import gettext_lazy as _
from . models import TextTitle, GraphicTitle, TextTitleChapter, \
    GraphicTitleChapter

class TextTitleForm(forms.ModelForm):
    """
    Form for text titles
    """
    class Meta:
        model = TextTitle
        fields = ['title_name_rus',
                  'title_name_eng',
                  'title_author',
                  'title_is_ongoing',
                  'title_description',
                  'publication_year'
                  ]
        labels = {
            'title_name_rus': _('Название тайтла'),
            'title_name_eng': _('Название тайтла (английский, опционально)'),
            'title_author': _('Автор'),
            'title_is_ongoing': _('Тайтл все еще выходит'),
            'title_description': _('Описание'),
            'publication_year': _('Год выпуска')
        }
        widgets = {
            'title_name_rus': forms.TextInput(
                attrs={
                    'placeholder': _('Введите название'),
                    'class': 'form_input'
                    }
                ),
            'title_name_eng': forms.TextInput(
                attrs={
                    'placeholder': _('Введите название (если есть)'),
                    'class': 'form_input'
                    }
                ),
            'title_author': forms.TextInput(
                attrs={
                    'placeholder': _('Автор'),
                    'class': 'form_input'
                    }
                ),
            'title_is_ongoing': forms.CheckboxInput(
                attrs={
                    'class': 'form_checkbox_input'
                    }
                ),
            'title_description': forms.Textarea(
                attrs={
                    'placeholder': _('Введите описание...'),
                    'class': 'form_input',
                    'rows': 10
                    }
                ),
            'publication_year': forms.NumberInput(
                attrs={
                    'class': 'form_input'
                    }
                ),
        }



class GraphicTitleForm(forms.ModelForm):
    """
    Form for graphic titles
    """
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
            'title_is_ongoing': _('Тайтл все еще выходит'),
            'title_description': _('Описание'),
            'publication_year': _('Год выпуска')
        }
        widgets = {
            'title_name_rus': forms.TextInput(
                attrs={
                    'placeholder': _('Введите название'),
                    'class': 'form_input'
                    }
                ),
            'title_name_eng': forms.TextInput(
                attrs={
                    'placeholder': _('Введите название (если есть)'),
                    'class': 'form_input'
                    }
                ),
            'title_author': forms.TextInput(
                attrs={
                    'placeholder': _('Автор'),
                    'class': 'form_input'
                    }
                ),
            'title_is_ongoing': forms.CheckboxInput(
                attrs={
                    'class': 'form_checkbox_input'
                       }
                ),
            'title_description': forms.Textarea(
                attrs={
                    'placeholder': _('Введите описание...'),
                    'class': 'form_input',
                    'rows': 10
                    }
                ),
            'publication_year': forms.NumberInput(
                attrs={
                    'class': 'form_input'
                       }
                ),
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
        widgets = {
            'chapter_name': forms.TextInput(
                attrs={
                    'placeholder': _('Введите название'),
                    'class': 'form_input'
                    }
                ),
            'chapter_number': forms.NumberInput(
                attrs={
                    'class': 'form_input'
                    }
                ),
            'text_content': forms.ClearableFileInput(
                attrs={
                    
                }
            )
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
        widgets = {
            'chapter_name': forms.TextInput(
                attrs={'placeholder': _('Введите название'),
                       'class': 'form_input'
                       }
                ),
            'chapter_number': forms.NumberInput(
                attrs={
                    'class': 'form_input'
                    }
                ),
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
            result = [single_file_clean(data, initial)]
        return result


class GraphicTitlePagesForm(forms.Form):
    """Form for uploading multiple pages for graphic titles"""
    images = MultipleFileField(label=_('Выберите страницы (не забудьте пронумеровать файлы)'),
                               required=True
                               )
