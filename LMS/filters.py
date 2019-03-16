from LMS.models import Book
import django_filters

class BookFilter(django_filters.FilterSet):
	title = django_filters.CharFilter(lookup_expr='icontains')
	author = django_filters.CharFilter(lookup_expr='icontains')
	class Meta:
		model = Book
		fields = ['bookid','title','author','yop']