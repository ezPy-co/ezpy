from django.test import TestCase, LiveServerTestCase
from django.test import Client

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from selenium import webdriver
import factory
import factory.django
from installer_config.models import EnvironmentProfile

from selenium import webdriver
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
