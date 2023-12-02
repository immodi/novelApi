from django import forms

class NovelsForm(forms.Form):
    novel_name = forms.CharField(required=True, label="Novel Name", max_length=999)
    novel_url = forms.CharField(required=True, label="Novel URL", max_length=9999999)
    starting_chapter = forms.CharField(required=True, max_length=9999)
    novel_source = forms.CharField(required=False, max_length=9999)