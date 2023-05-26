from django import forms
from django_countries.fields import CountryField


class MyForm(forms.Form):
    username = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"placeholder": "Enter username"})
    )
    email = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"placeholder": "Enter email"})
    )
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={"placeholder": "Enter password"}),
    )
    repeated_password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={"placeholder": "Repeat password"}),
    )
    phone = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={"placeholder": "Enter phone number"}),
    )
    country = CountryField().formfield()
    pesel = forms.CharField(
        max_length=20, widget=forms.TextInput(attrs={"placeholder": "Enter PESEL"})
    )
    first_name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"placeholder": "Enter first name"})
    )
    second_name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"placeholder": "Enter last name"})
    )


class MyCompanyForm(forms.Form):
    username = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"placeholder": "Enter username"})
    )
    email = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"placeholder": "Enter email"})
    )
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={"placeholder": "Enter password"}),
    )
    repeated_password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={"placeholder": "Repeat password"}),
    )
    phone = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={"placeholder": "Enter phone number"}),
    )
    country = CountryField().formfield()
    nip = forms.CharField(
        max_length=20, widget=forms.TextInput(attrs={"placeholder": "Enter NIP"})
    )
    name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"placeholder": "Enter name"})
    )
    sector = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"placeholder": "Enter sector"})
    )
