from django import forms

class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=9999)
    file = forms.FileField()