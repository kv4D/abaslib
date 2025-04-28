"""Contains forms for 'comments' app"""
from django import forms
from django.utils.translation import gettext_lazy as _


ATTRS = {
    'rows': '5',
    'placeholder': _('...')
}

class CommentForm(forms.Form):
    """
    Form for comment
    """
    text = forms.CharField(widget=forms.Textarea(attrs=ATTRS), label=_('Ваш комментарий...'))
    