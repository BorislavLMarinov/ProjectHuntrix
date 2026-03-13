from django import forms
from django.core.exceptions import ValidationError


class HuntrixVerificationForm(forms.Form):
    username = forms.CharField(
        label="Architect Name",
        help_text="The username you used during debut.",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. teacher_rose', 'class': 'form-control'})
    )

    email = forms.EmailField(
        label="Verified Email",
        help_text="The email associated with your Huntrix account.",
        widget=forms.EmailInput(attrs={'placeholder': 'idol@huntrix.com', 'class': 'form-control'})
    )

    age = forms.IntegerField(
        label="Verification Age",
        help_text="Confirm your age (must be 18+).",
        widget=forms.NumberInput(attrs={'placeholder': '25', 'class': 'form-control'})
    )

    password = forms.CharField(
        label="Security Key",
        widget=forms.PasswordInput(attrs={'placeholder': '••••••••', 'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        age = cleaned_data.get('age')

        if age and age < 18:
            raise ValidationError("Access Denied: You must be at least 18 years old to access the Creator Center.")

        return cleaned_data