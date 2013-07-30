"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import timezone
from sample_board.models import DjangoBoard
from .forms import UploadFileForm

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class ModelTestCase(TestCase):
    def test_model_create(self):
        self.assertEqual(DjangoBoard.objects.all().count(), 0)
        br = DjangoBoard.objects.create(subject = 'subject',
                name = 'name',
                mail = 'mail',
                memo = 'memo',
                created_date = timezone.now(),
                hits = 0,
                likes = 0
                )
        br.save() # just update? yes maybe, below test passed!
        self.assertEqual(DjangoBoard.objects.all().count(), 1)
        self.assertEqual(br.name, 'name')

        # is it work when click board hyperlink in board list 
        resp = self.client.post('/viewWork/?memo_id=1&current_page=1&searchStr=None')
        self.assertEqual(resp.status_code, 200)
    #def test_form_valid(self):
        #form = UploadFileForm(instance=br) # do i need to override init with instance?
        #self.assertTrue(form.is_valid())

# admin page test
class BoardAdminTestCase(TestCase):
    def test_index(self):
        resp = self.client.post('/admin')
        self.assertEqual(resp.status_code, 301) # Moved Permanently, why occur?

        resp = self.client.post('/admin/')
        self.assertEqual(resp.status_code, 200)

# list page test
class ListSpecificPageTestCase(TestCase):
    def test_index(self):
        # home
        resp = self.client.post('')
        self.assertEqual(resp.status_code, 200)

        # home two
        resp = self.client.post('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('boardList' in resp.context)

        # request nope
        resp = self.client.post('/listSpecificPageWork')
        self.assertEqual(resp.status_code, 301)

        # page 1
        resp = self.client.post('/listSpecificPageWork/?current_page=1')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('boardList' in resp.context)

        # rows Per Page modify
        resp = self.client.post('/rowmodify/',{'rowsPerPage':1})
        self.assertEqual(resp.status_code, 302)

# write board page test
class writeBoardTestCase(TestCase):
    def test_index(self):
        # redirect test
        resp = self.client.get('/show_write_form')
        self.assertEqual(resp.status_code, 301)

        resp = self.client.get('/DoWriteBoard')
        self.assertEqual(resp.status_code, 301)

    def test_write_post(self):
        resp = self.client.post('/DoWriteBoard/', {'subject':'Subject',
                                                                                        'name':'Name',
                                                                                        'mail':'Mail',
                                                                                        'memo':'Memo'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'], 'http://testserver/listSpecificPageWork?current_page=1')

        self.assertEqual(DjangoBoard.objects.all().count(), 1)

# view memo page test
class ViewMemoTestCase(TestCase):
    def test_index(self):
        # Ensure a non-existant memo_id throw a Not Found(404).
        resp = self.client.post('/viewWork/memo_id=1&current_page=1&searchStr=None')
        self.assertEqual(resp.status_code, 404)

class FileTestCase(TestCase):
    def test_index(self):
        resp = self.client.post('/upload')
        self.assertEqual(resp.status_code, 301)

# modify memo page test
class modifyMemoTestCase(TestCase):
    def test_index(self):
        br = DjangoBoard.objects.create(subject = 'subject',
                name = 'name',
                mail = 'mail',
                memo = 'memo',
                created_date = timezone.now(),
                hits = 0,
                likes = 0
                )
        self.assertEqual(DjangoBoard.objects.all().count(), 1)
        resp = self.client.post('/listSpecificPageWork_to_update')
        self.assertEqual(resp.status_code, 301)

        resp = self.client.post('/updateBoard/', {'memo_id':br.id,'current_page':1,'searchStr':'','name':'Name','mail':'Mail','subject':'Subject_modify','memo':'Memo'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'], 'http://testserver/listSpecificPageWork?current_page=1')
        self.assertEqual(DjangoBoard.objects.all()[0].subject, 'Subject_modify')
        self.assertEqual(DjangoBoard.objects.all().count(), 1)

class deleteMemoTestCase(TestCase):
    def test_index(self):
        br = DjangoBoard.objects.create(subject = 'subject',
                name = 'name',
                mail = 'mail',
                memo = 'memo',
                created_date = timezone.now(),
                hits = 0,
                likes = 0
                )
        self.assertEqual(br.id, 2L)
        self.assertEqual(DjangoBoard.objects.all().count(), 1)
        resp = self.client.post('/DeleteSpecificRow')
        self.assertEqual(resp.status_code, 301)

        resp = self.client.post('/DeleteSpecificRow/?memo_id=2&current_page=1')
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp['Location'], 'http://testserver/listSpecificPageWork?current_page=0') 
        self.assertEqual(DjangoBoard.objects.all().count(), 0)

# search page test
class SearchMemoTestCase(TestCase):
    def test_index(self):
        resp = self.client.post('/searchWithSubject')
        self.assertEqual(resp.status_code, 301)

        # non-data must be missing
        resp = self.client.post('/searchWithSubject/', {'searchStr':'df', 'pageForView':1})
        self.assertEqual(resp.status_code, 302)

