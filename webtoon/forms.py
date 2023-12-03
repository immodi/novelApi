from django import forms

class WebtoonsForm(forms.Form):
    webtoon_name = forms.CharField(required=True, label="Webtoon Name", max_length=999)
    webtoon_url = forms.CharField(required=True, label="Webtoon URL", max_length=9999999)
    starting_chapter = forms.IntegerField(required=True)
    total_chapters = forms.IntegerField(required=True)
    webtoon_source = forms.CharField(required=False, max_length=9999)