from django import forms


__all__ = []


class EchoForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
