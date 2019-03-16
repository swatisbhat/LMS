from django.test import TestCase
from LMS.models import Book, Student, IssueBook
from django.test import Client
from django.urls import reverse
import re



from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class RegisterViewSeleniumTest(LiveServerTestCase):

	def setUp(self):
		self.selenium = webdriver.Firefox()
		super(RegisterViewSeleniumTest, self).setUp()

	def tearDown(self):
		self.selenium.quit()
		super(RegisterViewSeleniumTest, self).tearDown()

	def test_register(self):
		selenium = self.selenium
		#Opening the link we want to test
		selenium.get('http://127.0.0.1:8000/register/')
		#find the form element
		rollno = selenium.find_element_by_id('id_rollno')
		first_name = selenium.find_element_by_id('id_first_name')
		last_name = selenium.find_element_by_id('id_last_name')
		department = selenium.find_element_by_id('id_department')
		email = selenium.find_element_by_id('id_email')

		submit = selenium.find_element_by_id('Register')

		#Fill the form with data
		rollno.send_keys(10025)
		first_name.send_keys('Tim')
		last_name.send_keys('Lee')
		department.send_keys('Chemical')
		email.send_keys('timlee@email.com')


		#submitting the form
		submit.click()
		element = WebDriverWait(selenium, 20).until(EC.visibility_of_element_located((By.ID, "message")))
		#check the returned result
		#assertEqual()
		assert 'Registration successful' in selenium.page_source

#------------- Model tests-------------#

class BookModelTest(TestCase):

    def test_create(self):
        Book.objects.create(bookid = 1, title = 'Book1', author = 'Author1',yop=1995,copies=1)
        self.assertEqual(Book.objects.count(), 1)

    def test_content(self):
        Book.objects.create(bookid = 1, title = 'Book1', author = 'Author1',yop=1995,copies=1)
        book = Book.objects.get(title='Book1')
        expected_object_name = book.title
        self.assertEqual(expected_object_name, 'Book1')

class StudentModelTest(TestCase):

    def test_create(self):
        Student.objects.create(rollno=10001, first_name='User1',last_name='User1L',department='Chemical',email='a@b.com')
        self.assertEqual(Student.objects.count(), 1)

    def test_content(self):
        Student.objects.create(rollno=10001, first_name='User1',last_name='User1L',department='Chemical',email='a@b.com')
        student = Student.objects.get(rollno=10001)
        expected_object_name = student.email
        self.assertEqual(expected_object_name, 'a@b.com')

class IssueBookModelTest(TestCase):


	def setUp(self):
		Book.objects.create(bookid = 1, title = 'Book1', author = 'Author1',yop=1995,copies=1)
		Student.objects.create(rollno=10001, first_name='User1',last_name='User1L',department='Chemical',email='a@b.com')

	def test_create(self):
		student = Student.objects.get(rollno=10001)
		book = Book.objects.get(bookid=1)
		IssueBook.objects.create(student=student, book=book)
		self.assertEqual(IssueBook.objects.count(), 1)

	def test_content(self):
		student = Student.objects.get(rollno=10001)
		book = Book.objects.get(bookid=1)
		IssueBook.objects.create(student=student, book=book)
		student = IssueBook.objects.get(student=10001)
		expected_object_name = student.book.bookid
		self.assertEqual(expected_object_name,1)

	def test_book_count(self):
		student = Student.objects.get(rollno=10001)
		book = Book.objects.get(bookid=1)
		# test book count on issue (save method)
		IssueBook.objects.create(student=student, book=book)
		book_count = Book.objects.get(bookid=1).copies
		self.assertEqual(book_count, 0)
		# test book count on return (delete method)
		book = IssueBook.objects.get(book=1)
		book.delete()
		book_count = Book.objects.get(bookid=1).copies
		self.assertEqual(book_count, 1)



#---------- View tests ----------#

class SearchViewTest(TestCase):

	def setUp(self):
		Book.objects.create(bookid = 1, title = 'Book1', author = 'Author1',yop=1995,copies=1)
		Book.objects.create(bookid = 2, title = 'Book2', author = 'Author2',yop=1996,copies=1)

	def test_url_exists_at_proper_location(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code,200)

	def test_url_by_name(self):
		response = self.client.get(reverse('search'))
		self.assertEqual(response.status_code,200)

	def test_uses_correct_template(self):
		response = self.client.get(reverse('search'))
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,'search.html')

	def test_filter(self):
		c=Client()
		response = c.post('/',{'bookid': 1 ,'title':'','author':'','yop':None})
		data = response.content.decode('utf-8')
		#filtered_books = list((response.context['filter']).qs)
		#filtered_books_count = Book.objects.filter(bookid=1).count()
		#self.assertEqual(str(filtered_books[0]),'Book1')
		#self.assertEqual(filtered_books[1],'hey')

		#self.assertEqual(Book.objects.count(),2)
		#self.assertEqual(filtered_books_count,filtered_books)
		found = re.search('Book1',data).group(0)
		self.assertEqual(found, 'Book1')






class RegisterViewTest(TestCase):

	def test_url_exists_at_proper_location(self):
		response = self.client.get('/register/')
		self.assertEqual(response.status_code,200)

	def test_url_by_name(self):
		response = self.client.get(reverse('register'))
		self.assertEqual(response.status_code,200)

	def test_uses_correct_template(self):
		response = self.client.get(reverse('register'))
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response,'form.html')

	def test_register_valid_input(self):
		c = Client()
		response = c.post('/register/',{'rollno': 10001,'first_name':'first_name','last_name':'last_name','department':'Chemical','email':'a@b.com'})
		self.assertEqual(response.status_code,200)

	def test_register_valid_input(self):
		c = Client()
		response = c.post('/register/',{'rollno': 10001,'first_name':'first_name','last_name':'last_name','department':'Chemical','email':'a@b.com'})
		m = list(response.context['messages'])
		self.assertEqual(response.status_code,200)
		self.assertEqual(len(m), 1)
		#self.assertIn('Registration successful.',m)
		self.assertEqual(str(m[0]),'Registration successful.')

	def test_register_rollno_already_exixts_input(self):
		Student.objects.create(rollno=10001, first_name='User1',last_name='User1L',department='Chemical',email='a@c.com')
		c = Client()
		response = c.post('/register/',{'rollno': 10001,'first_name':'first_name','last_name':'last_name','department':'Chemical','email':'a@b.com'})
		m = list(response.context['messages'])
		self.assertEqual(response.status_code,200)
		self.assertEqual(len(m), 1)
		self.assertEqual('Roll no / Email already exists!',str(m[0]))

	def test_register_email_already_exixts_input(self):
		Student.objects.create(rollno=10001, first_name='User1',last_name='User1L',department='Chemical',email='a@c.com')
		c = Client()
		response = c.post('/register/',{'rollno': 10002,'first_name':'first_name','last_name':'last_name','department':'Chemical','email':'a@c.com'})
		m = list(response.context['messages'])
		self.assertEqual(response.status_code,200)
		self.assertEqual(len(m), 1)
		self.assertEqual('Roll no / Email already exists!',str(m[0]))

	def test_register_department_not_chosen_input(self):
		c = Client()
		response = c.post('/register/',{'rollno': 10002,'first_name':'first_name','last_name':'last_name','department':'Choose Department','email':'a@c.com'})
		m = list(response.context['messages'])
		self.assertEqual(response.status_code,200)
		self.assertEqual(len(m), 1)
		self.assertEqual('Please choose your department.',str(m[0]))

	def test_register_invalid_email_input(self):
		c = Client()
		response = c.post('/register/',{'rollno': 10002,'first_name':'first_name','last_name':'last_name','department':'Choose Department','email':'abc'})
		m = list(response.context['messages'])
		self.assertEqual(response.status_code,200)
		self.assertEqual(len(m), 1)
		self.assertEqual('Enter a valid email id.',str(m[0]))


