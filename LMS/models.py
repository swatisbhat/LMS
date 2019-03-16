from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q

# Create your models here.
class Book(models.Model):
	bookid = models.IntegerField(primary_key=True,unique=True)
	title = models.CharField(max_length=100, unique=True)
	author = models.CharField(max_length=100)
	yop = models.IntegerField()
	copies = models.IntegerField()

	def __str__(self):
		return self.title

class Student(models.Model):
	DEPT_CHOICES=[ 'Chemical', 'Civil', 'Computer Science', 'Electronics', 'Electrical', 'Information Technology', 'Mechanical']
	rollno = models.IntegerField(primary_key=True,unique=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	department = models.CharField(max_length=30, choices=[(x,x) for x in DEPT_CHOICES])
	email = models.EmailField(unique=True)

	def __str__(self):
		return str(self.rollno)


class IssueBook(models.Model):
	
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	book = models.ForeignKey(Book, on_delete=models.CASCADE, limit_choices_to = Q(copies__gt=0))

	def __str__(self):
		return str(self.student.rollno)+'-'+str(self.book.bookid)

	def save(self, *args, **kwargs):
		book = Book.objects.get(bookid=self.book.bookid)
		book.copies-=1
		book.save()
		super().save(*args, **kwargs)  # Call the "real" save() method.

	def delete(self, *args, **kwargs):
		book = Book.objects.get(bookid=self.book.bookid)
		book.copies+=1
		book.save()
		super().delete(*args, **kwargs)

	class Meta:
		unique_together = ('student', 'book')
	
		

