""" tento soubor si vytvorim rucne """
from django.contrib.auth.forms import UserCreationForm
from django import forms

from viewer import forms


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


    # password1 = forms.CharField(
    #     widget=forms.PasswordInput(attrs={'placeholder': 'Heslo'}),
    #     label="Heslo"
    # )
    # password2 = forms.CharField(
    #     widget=forms.PasswordInput(attrs={'placeholder': 'Heslo znovu'}),
    #     label="Heslo znovu"
    # )