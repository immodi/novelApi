from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

class DownloadForm(forms.Form):
    file_id = forms.IntegerField(required=True)