from django.contrib.auth.models import User
from .models import Review
from django import forms
from django.core.urlresolvers import reverse
from ckeditor.widgets import CKEditorWidget


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'email']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            msg = "password doesn't match"
            self.add_error('confirm_password', msg)
        return cleaned_data

class ReviewForm(forms.ModelForm):
    #review=forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Review
        fields =['topic','review','rating']
