from django import forms

# CSV 파일 업로드 위한 form 
class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
