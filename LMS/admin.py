from django.contrib import admin
from LMS.models import Student,Book, IssueBook

# Register your models here.

class BookAdmin(admin.ModelAdmin):
	list_display=('bookid','title','author','yop','copies')
	search_fields=('bookid','title','author')

class StudentAdmin(admin.ModelAdmin):
	list_display=('rollno','first_name','last_name','department','email')
	search_fields=('rollno','first_name','last_name','department','email')


class IssueBookAdmin(admin.ModelAdmin):
	list_display=('student','book')
	search_fields=('student','book')

	
admin.site.register(Student, StudentAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(IssueBook, IssueBookAdmin)
