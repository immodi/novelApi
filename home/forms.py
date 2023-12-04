from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()


class DownloadFileForm(forms.Form):
    file_id = forms.IntegerField()