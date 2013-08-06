__author__ = 'Shin'
"""
This is Django unit test example code.

Django unit test run with command,

    "manage.py test target_app_name"

    if you want test all app, let target_app_name blank

    "manage.py test"

and then coverage run, report with command,

    "python -m coverage run --source='.' manage.py test target_app_name"

    "python -m coverage report"

reference : https://docs.djangoproject.com/en/1.4/topics/testing/
            https://docs.djangoproject.com/en/1.5/topics/testing/advanced/#integration-with-coverage-py
            http://toastdriven.com/blog/2011/apr/10/guide-to-testing-in-django/
            http://toastdriven.com/blog/2011/apr/17/guide-to-testing-in-django-2/
"""

from django.test import TestCase
from django.conf import settings
from django.utils.importlib import import_module

class SessionAndCookieTestCase(TestCase):
    # suppose url(r'^post_comment/$', views.post_comment)
    """
    def post_comment(request, new_comment):
        if request.session.get('has_commented', False):
            return HttpResponse("You've already commented.")
        c = comments.Comment(comment=new_comment)
        c.save()
        request.session['has_commented'] = True
        return HttpResponse('Thanks for your comment!')
    """
    def test_session_and_cookie(self):
        # not yet find way that check session and cookie in response
        # TODO. FYI Visit http://code.djangoproject.com/ticket/10899
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
        session = self.client.session
        session.update({'key':'value', 'sns':'good', 'has_commented':False})
        session.save()

        self.assertEqual(session['key'], 'value')
        self.assertEqual(session['sns'], 'good')

        response = self.client.post('/post_comment/', {'comment':'comment'})
        # post comment success
        self.assertEqual(response.staus_code, 200)

        response = self.client.post('/post_comment/', {'comment':'comment'})
        # already commented. session have 'has_commented':True.
        self.assertEqual(response.status_code, 401)


        # session_key_resp is None. this not working
        session_key_resp = response.cookies.get(settings.SESSION_COOKIE_NAME)
        session_key = self.client.cookies.get(settings.SESSION_COOKIE_NAME)
        #self.assertEqual(session_key, session_key_resp)

class HtmlTestCase(TestCase):
    # HTML tag test
    def test_html(self):
        response = self.client.get('/')
        # check response have expected html tag and status code
        self.assertContains( response, '<p id="unittest" style="display: block"></p>', status_code=200 )
        # check template where response is from
        self.assertTemplateUsed( response, 'listSpecificPage.html' )

class ResponseTestCase(TestCase):
    # status code test
    def test_status_code(self):
        # method = get
        response_get = self.client.get('/')
        self.assertEqual(response_get.status_code, 200)

        # method = post
        response_post = self.client.post('/', {'rowsPerPage':'1'})
        self.assertEqual(response_post.status_code, 200)

    def test_http_header(self):
        url = '/listSpecificPageWork?current_page=1'
        response = self.client.post('/rowmodify/', {'rowsPerPage':'1'}) # TODO. need to setting url after redirect to check Location
        # default test url 'http://testserver/'
        expected_redirect_url = 'http://testserver/listSpecificPageWork?current_page=1' # TODO. setting redirect url

        # Location, read-only header represents the URL the response will redirect to.
        self.assertEqual(response['Location'], expected_redirect_url)