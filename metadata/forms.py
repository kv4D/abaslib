"""Contains forms for 'metadata' app"""
from django import forms
from django.utils.translation import gettext_lazy as _
from . models import Tag, TagGenre


class FilterTagForm(forms.Form):
    """
    Form for filter tag selection
    """
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    genres = forms.ModelMultipleChoiceField(
        queryset=TagGenre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        labels = {
            'tags': _('Теги'),
            'genres': _('Жанры')
        }

