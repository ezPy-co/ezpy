from django.test import TestCase, LiveServerTestCase
from django.test import Client
import datetime
import time
# from django.utils import timezone

from django.contrib.auth.models import User
from registration.models import RegistrationProfile
from django.core.urlresolvers import reverse

from selenium import webdriver
import factory
import factory.django
from installer_config.models import EnvironmentProfile

import os


TEST_DOMAIN_NAME = "http://127.0.0.1:8081"


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: u'username%d' % n)


class EnvironmentProfileFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = EnvironmentProfile

    title = factory.Sequence(lambda n: u'EnvironmentalProfile%d' % n)
    user = factory.SubFactory(UserFactory)


class CreateUserTestCase(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.user1.save()

    def test_user(self):
        """Test to see if user is being created."""
        self.user2 = UserFactory()
        self.user2.save()
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(username=self.user1.username), self.user1)
        self.assertEqual(User.objects.get(username=self.user2.username), self.user2)


class RegistrationTestCase(TestCase):

    def setUp(self):
        self.user = {}
        self.user['user1'] = User.objects.create_user(username='username1',
                                                      password='secret')
        self.client1 = Client()

    def test_login_unauthorized(self):
        """Test that an unauthorized user cannot get in."""
        response = self.client1.post('/accounts/login/',
                                     {'username': 'hacker', 'password': 'badpass'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Please enter a correct username and password.', response.content)
        is_logged_in = self.client1.login(username='hacker', password='badpass')
        self.assertFalse(is_logged_in)

    def test_login_authorized(self):
        """Test that an authorized user can get in."""
        response = self.client1.post('/accounts/login/',
                                     {'username': self.user['user1'].username,
                                      'password': 'secret'})
        self.assertEqual(response.status_code, 302)
        is_logged_in = self.client1.login(username=self.user['user1'].username,
                                          password='secret')
        self.assertTrue(is_logged_in)


    def test_logout(self):
        """Test that an authorized user can log out."""
        is_logged_in = self.client1.login(username=self.user['user1'].username,
                                          password='secret')
        self.assertTrue(is_logged_in)
        response = self.client1.post('/accounts/logout/')
        # Goes to an intermediate page that the user never sees before
        # going back to the home page
        self.assertIn('You are now logged out.', response.content)

class UserProfileDetailTestCase(LiveServerTestCase):
    """This class is for testing user login form"""
    def setUp(self):
        self.driver = webdriver.Firefox()
        super(UserProfileDetailTestCase, self).setUp
        self.user = User(username='user1')
        self.user.set_password('pass')
        self.user.is_active = True

    def tearDown(self):
        self.driver.refresh()
        self.driver.quit()
        super(UserProfileDetailTestCase, self).tearDown()

    def test_goto_homepage(self):
        self.driver.get(self.live_server_url)
        self.assertIn("ezPy", self.driver.title)

    def login_user(self):
        """login user"""
        self.driver.get(TEST_DOMAIN_NAME + reverse('auth_login'))
        username_field = self.driver.find_element_by_id('id_username')
        username_field.send_keys('user1')
        password_field = self.driver.find_element_by_id('id_password')
        password_field.send_keys('pass')
        form = self.driver.find_element_by_tag_name('form')
        form.submit()

    def test_login_authorized(self):
        """Test that a registered user can get in."""
        self.user.save()
        self.login_user()
        self.assertIn(self.user.username, self.driver.page_source)

    def test_login_unregistered(self):
        """Test that an unregistered user cannot get in."""
        self.unregistered_user = User(username='unregistered')
        self.user.set_password('pass')
        self.user.is_active = False
        self.assertNotIn(self.unregistered_user.username, self.driver.page_source)

