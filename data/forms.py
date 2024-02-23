from django import forms

class FileForm(forms.Form):
    mimeType = forms.CharField(max_length=500, required=True)
    name = forms.CharField(max_length=9999, required=True)
    size = forms.IntegerField(required=True)
    path = forms.CharField(max_length=9999, required=True)