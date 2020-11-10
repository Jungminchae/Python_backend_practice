from django import forms
from . import models 

class RegisterForm(forms.ModelForm):

    password = forms.CharField(label='password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='confirm_password', widget=forms.PasswordInput)

    class Meta:
        model = models.User
        fields = ['username', 'firt_name', 'last_name', 'email']

    def clean_confirm_password(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['password'] != cleaned_data['confirm_password']:
            raise forms.ValidationError("Password does not match")

        return cleaned_data['confirm_password']