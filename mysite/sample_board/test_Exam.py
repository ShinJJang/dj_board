__author__ = 'Shin'

from django.test import TestCase
from django.conf import settings
from django.utils.importlib import import_module

class SessionAndCookieTestCase(TestCase):
    def test_session_and_cookie(self):
        # not yet find way that check session and cookie in response
        # TODO. FYI Visit http://code.djangoproject.com/ticket/10899
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
        session = self.client.session
        session.update({'key':'value', 'sns':'good'})
        session.save()

        self.assertEqual(session['key'], 'value')
        self.assertEqual(session['sns'], 'good')

        response = self.client.post('/')

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
        response = self.client.get('/') # TODO. need to setting url after redirect to check Location
        expected_redirect_url = 'http://testserver/' # default test url

        # Location, read-only header represents the URL the response will redirect to.
        self.assertEqual(response['Location'], expected_redirect_url)