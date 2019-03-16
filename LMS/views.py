from django.shortcuts import render
from .forms import RegisterForm
from django.contrib import messages
from .models import Student,Book
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from .filters import BookFilter

# Create your views here.
def register(request):
	if request.method=='POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			rollno_ = cd['rollno']
			first_name_ = cd['first_name']
			last_name_ = cd['last_name']
			department_ = cd['department']
			email_ = cd['email']

			try:
				rollno_exists = Student.objects.get(rollno=rollno_)
				messages.error(request, 'Roll no / Email already exists!')
				return render(request,'form.html',{'form':form,'name':'Register'})

			except ObjectDoesNotExist:

				try:
					email_exists = Student.objects.get(email=email_)
					messages.error(request, 'Roll no / Email already exists!')
					return render(request,'form.html',{'form':form,'name':'Register'})

				except ObjectDoesNotExist:

					if department_ == 'Choose Department':
						messages.error(request, 'Please choose your department.')
						return render(request,'form.html',{'form':form,'name':'Register'})

					else:
						registered_user = Student(rollno=rollno_,first_name=first_name_,last_name=last_name_,department=department_,email=email_)
						registered_user.save()
						messages.success(request, 'Registration successful.')
						form = RegisterForm()
						return render(request,'form.html',{'form':form,'name':'Register'})

		else:
			messages.error(request, 'Enter a valid email id.')
			return render(request,'form.html',{'form':form,'name':'Register'})

	form = RegisterForm()
	return render(request,'form.html',{'form':form,'name':'Register'})


def search(request):
	books = Book.objects.all()
	book_filter = BookFilter(request.GET,queryset=books)
	return render(request,'search.html',{'filter':book_filter})

