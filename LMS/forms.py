from django import forms
import datetime

class RegisterForm(forms.Form):
	DEPT_CHOICES=[ 'Choose Department', 'Chemical', 'Civil', 'Computer Science', 'Electronics', 'Electrical', 'Information Technology', 'Mechanical']
	rollno = forms.IntegerField(min_value=10001,max_value=50000,  widget=forms.NumberInput(attrs={'placeholder': 'Regisration No.'}))
	first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
	last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
	department = forms.ChoiceField(choices=[(x, x) for x in DEPT_CHOICES])
	email = forms.EmailField( widget=forms.TextInput(attrs={'placeholder': 'Email'}))











