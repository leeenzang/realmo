from django import forms

class DateRangeForm(forms.Form):
    DURATION_CHOICES = [
        (30, '30일'),
        (45, '45일'),
        (60, '60일')
    ]
    duration = forms.ChoiceField(choices=DURATION_CHOICES, initial=30, label="기간 선택")
