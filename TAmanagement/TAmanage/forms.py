from django import forms
from .models import *


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control','placeholder':'i.e:abc@xyz.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'********'}))


class CreateCourseForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'i.e: CS701'}))
    section = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'i.e: 401'}))


CHOICES = [
        (1, 'TA'),
        (2, 'Instructor'),
        (3, 'Administrator'),
    ]


class CreateUserForm(forms.Form):
    email = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'i.e:abc@xyz.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'********'}))
    role = forms.CharField(widget=forms.Select(choices=CHOICES))


class EditCourseForm(forms.Form):
    name = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'i.e:CS000'}))
    section = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'i.e:401'}))
    location = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'i.e:EMS'}))
    startTime = forms.TimeField(required=True, widget=forms.TimeInput(format='%H:%M',attrs={'placeholder':'i.e:13:00'}))
    endTime = forms.TimeField(required=True, widget=forms.TimeInput(format='%H:%M',attrs={'placeholder':'i.e:14:00'}))
    dates = forms.CharField(required=True, max_length=6, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'MTWRFS'}))


class EditUserForm(forms.Form):
    email = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'i.e:abc@xyz.com'}))
    firstName = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastName = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(required=False, max_length=15, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'123456789'}))
    address = forms.CharField(required=False, max_length=255, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'i.e:123 East Road'}))
    officeHours = forms.CharField(required=False, max_length=15, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'i.e:2pm'}))
    officeHoursDates = forms.CharField(required=False, max_length=6, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'i.e:MTWRFS'}))
    officeLocation = forms.CharField(required=False, max_length=6, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'i.e:EMS222'}))
    role = forms.CharField(widget=forms.Select(choices=CHOICES))
    resume = forms.CharField(required=False, max_length=5000, widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'i.e:I am a PhD student'}))
    schedule = forms.CharField(required=False, max_length=5000, widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'i.e:MW 12:30-13:50'}))
    preferences = forms.CharField(required=False, max_length=5000, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'i.e:TR 12:00-4:00'}))


class CreateLabForm(forms.Form):
    section = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'i.e:401'}))


class EditLabForm(forms.Form):
    section = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'i.e:401'}))
    location = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'i.e:EMS'}))
    startTime = forms.TimeField(required=True, widget=forms.TimeInput(format='%H:%M',attrs={'placeholder':'i.e:13:00'}))
    endTime = forms.TimeField(required=True, widget=forms.TimeInput(format='%H:%M',attrs={'placeholder':'i.e:14:00'}))
    dates = forms.CharField(required=True, max_length=6, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'i.e:MTWRFS'}))


'''class EditProfileForm(forms.Form):
    resume = forms.CharField(required=False, max_length=5000, widget=forms.Textarea(attrs={'class': 'form-control'}))
    schedule = forms.CharField(required=False, max_length=5000, widget=forms.Textarea(attrs={'class': 'form-control'}))
    preferences = forms.CharField(required=False, max_length=5000, widget=forms.Textarea(attrs={'class': 'form-control'}))'''


class AssignTaForm(forms.Form):
    course = forms.ModelChoiceField(widget=forms.Select, queryset=Course.objects.all(), to_field_name="name")
    tas = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=User.objects.all(), to_field_name="email")



