"""Contains forms for 'titles' app"""
from django import forms
from django.utils.translation import gettext_lazy as _
from titles.models import TextTitle, GraphicTitle, TextTitleChapter, \
    GraphicTitleChapter
from metadata.models import Tag, TagGenre, TitleGenre, TitleTag

class TextTitleForm(forms.ModelForm):
    """
    Form for text titles
    """
    genres_field = forms.ModelMultipleChoiceField(
        queryset=TagGenre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label=_('Жанры')
    )

    tags_field = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label=_('Теги')
    )

    class Meta:
        model = TextTitle
        fields = [
            'title_name_rus',
            'title_name_eng',
            'title_author',
            'title_is_ongoing',
            'title_description',
            'genres_field',
            'tags_field',
            'publication_year',
            'title_cover'
            ]
        labels = {
            'title_name_rus': _('Название тайтла'),
            'title_name_eng': _('Название тайтла (английский, опционально)'),
            'title_author': _('Автор'),
            'title_is_ongoing': _('Тайтл все еще выходит'),
            'title_description': _('Описание'),
            'publication_year': _('Год выпуска'),
            'title_cover': _('Обложка'),
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
            'title_cover': forms.FileInput(
                attrs={
                    'class': 'form_input cover'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['genres_field'].initial = [
                genre.tag_genre for genre in
                TitleGenre.objects.filter(content_object=self.instance)
            ]
            self.fields['tags_field'].initial = [
                tag.tag for tag in
                TitleTag.objects.filter(content_object=self.instance)
            ]

    def save(self, commit=True):
        title = super().save(commit=commit)
        if commit:
            TitleGenre.objects.filter(content_object=title).delete()
            TitleTag.objects.filter(content_object=title).delete()

            for genre in self.cleaned_data['genres_field']:
                TitleGenre.objects.create(content_object=title, tag_genre=genre)
            for tag in self.cleaned_data['tags_field']:
                TitleTag.objects.create(content_object=title, tag=tag)
        return title


class GraphicTitleForm(forms.ModelForm):
    """
    Form for graphic titles
    """
    genres_field = forms.ModelMultipleChoiceField(
        queryset=TagGenre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label=_('Жанры')
    )

    tags_field = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label=_('Теги'),
    )

    class Meta:
        model = GraphicTitle
        fields = ['title_name_rus',
                  'title_name_eng',
                  'title_author',
                  'title_is_ongoing',
                  'title_description',
                  'genres_field',
                  'tags_field',
                  'publication_year',
                  'title_cover'
                  ]
        labels = {
            'title_name_rus': _('Название тайтла'),
            'title_name_eng': _('Название тайтла (английский, опционально)'),
            'title_author': _('Автор'),
            'title_is_ongoing': _('Тайтл все еще выходит'),
            'title_description': _('Описание'),
            'publication_year': _('Год выпуска'),
            'title_cover': _('Обложка'),
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
            'title_cover': forms.FileInput(
                attrs={
                    'class': 'form_input cover'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['genres_field'].initial = [
                genre.tag_genre for genre in self.instance.genres.all()
            ]
            self.fields['tags_field'].initial = [
                tag.tag for tag in self.instance.tags.all()
            ]

    def save(self, commit=True):
        title = super().save(commit=commit)
        if commit:
            title.genres.all().delete()
            title.tags.all().delete()

            for genre in self.cleaned_data['genres_field']:
                TitleGenre.objects.create(content_object=title, tag_genre=genre)
            for tag in self.cleaned_data['tags_field']:
                TitleTag.objects.create(content_object=title, tag=tag)
        return title

class TextTitleChapterForm(forms.ModelForm):
    """
    Form for text chapters
    """
    class Meta:
        model = TextTitleChapter
        fields = ['title',
                  'chapter_name',
                  'display_number',
                  'chapter_number',
                  'volume',
                  'text_content']
        labels = {
            'title': _('Тайтл'),
            'chapter_name': _('Название главы'),
            'display_number': _('Номер главы (для отображения)'),
            'chapter_number': _('Номер главы (фактический)'),
            'volume': _('Том главы'),
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
                    'placeholder': _('Фактический числовой номер главы'),
                    'class': 'form_input'
                    }
                ),
            'text_content': forms.ClearableFileInput(),
            'volume': forms.TextInput(
                attrs={
                    'placeholder': _('Если томов нет или он один, оставьте пустым'),
                    'class': 'form_input'
                }
            ),
            'display_number': forms.TextInput(
                attrs={
                    'placeholder': _('Символы допускаются'),
                    'class': 'form_input'
                    }
                ),
        }

    def __init__(self, *args, title=None, chapter_number=None, **kwargs):
        super().__init__(*args, **kwargs)
        if title:
            self.fields['title'].initial = title
            self.fields['title'].widget = forms.HiddenInput()
        if chapter_number:
            self.fields['chapter_number'].initial = chapter_number


class GraphicTitleChapterForm(forms.ModelForm):
    """
    Form for graphic chapters
    """
    class Meta:
        model = GraphicTitleChapter
        fields = ['title',
                  'chapter_name',
                  'display_number',
                  'chapter_number',
                  'volume',]
        labels = {
            'title': _('Тайтл'),
            'chapter_name': _('Название главы'),
            'display_number': _('Номер главы (для отображения)'),
            'chapter_number': _('Номер главы (фактический)'),
            'volume': _('Том главы'),
        }
        widgets = {
            'chapter_name': forms.TextInput(
                attrs={'placeholder': _('Введите название'),
                       'class': 'form_input'
                       }
                ),
            'chapter_number': forms.NumberInput(
                attrs={
                    'placeholder': _('Фактический числовой номер главы'),
                    'class': 'form_input'
                    }
                ),
                        'volume': forms.TextInput(
                attrs={
                    'placeholder': _('Если томов нет или он один, оставьте пустым'),
                    'class': 'form_input'
                }
            ),
            'display_number': forms.TextInput(
                attrs={
                    'placeholder': _('Символы допускаются'),
                    'class': 'form_input'
                    }
                ),
        }

    def __init__(self, *args, title=None, chapter_number=None, **kwargs):
        super().__init__(*args, **kwargs)
        if title:
            self.fields['title'].initial = title
            self.fields['title'].widget = forms.HiddenInput()
        if chapter_number:
            self.fields['chapter_number'].initial = chapter_number


class MultipleFileInput(forms.ClearableFileInput):
    """Allows uploading multiple files"""
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
