from django.test import TestCase, LiveServerTestCase
from django.test import Client

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from selenium import webdriver
import factory
import factory.django
from installer_config.models import EnvironmentProfile, UserChoice, Step

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


    def login_user(self, user, password):
        """login user"""
        self.driver.get(TEST_DOMAIN_NAME + reverse('auth_login'))
        username_field = self.driver.find_element_by_id('id_username')
        username_field.send_keys(user)
        password_field = self.driver.find_element_by_id('id_password')
        password_field.send_keys(password)
        form = self.driver.find_element_by_tag_name('form')
        form.submit()

    # def test_create_profile(self):
    #     # .save() is here instead of setUp to save time
    #     self.user.save()
    #     self.login_user('user1', 'pass')
    #     self.driver.get(TEST_DOMAIN_NAME +
    #                     reverse('installer_config:CreateEnv'))
    #     self.assertIn("profileform", self.driver.page_source)

    #     # fill out form
    #     description = "Test description."
    #     field = self.driver.find_element_by_id('id_description')
    #     field.send_keys(description)

    #     form = self.driver.find_element_by_tag_name('form')
    #     form.submit()
    #     self.assertIn("userprofile", self.driver.page_source)
    #     self.assertIn(description, self.driver.page_source)


    # def test_update_profile(self):
    #     # .save() is here instead of setUp to save time
    #     self.user.save()
    #     self.login_user('user1', 'pass')
    #     self.driver.get(TEST_DOMAIN_NAME +
    #                     reverse('installer_config:UpdateEnv',
    #                             kwargs={'pk': self.user.pk}))
    #     self.assertIn("profileform", self.driver.page_source)





        # 'UpdateEnv'    kwargs={'pk': self.user.pk}

        # 'DeleteEnv'    kwargs={'pk': self.user.pk}

        # 'download_profile'    kwargs={'pk': self.user.pk}

        # 'ViewEnv'     kwargs={'pk': self.user.pk}



class DownloadFileFormationTest(TestCase):
    def setUp(self):
        self.user = User(username='n00b')
        self.user.set_password('...')
        self.user.is_active = True
        self.client = Client()

    def tearDown(self):
        pass

    def test_choice_presence_set1(self):
        # Verify the presence of the corresponding code in the downloaded
        # generated python script
        self.user.save()

        settings = [('important thing', 'core', 1),
                    ('your env', 'env', 1),
                    ('get', 'git', 1),
                    ('bash shenanigannns', 'prompt', 2),
                    ('text editor', 'subl', 2),
                    ('a pip package', 'pkg', 3),
                    ('other', 'other', 3),]

        choices = []
        for name, category, priority in settings:
            choices.append(UserChoice(name=name, category=category, priority=priority))
            choices[-1].save()

        # Set up steps association with choices
        for choice in UserChoice.objects.filter(priority=1):
            Step(step_type='dl', user_choice=choice).save()
            Step(step_type='edfile', user_choice=choice).save()
            Step(step_type='edprof', user_choice=choice).save()
        for choice in UserChoice.objects.filter(priority=2):
            Step(step_type='env', user_choice=choice).save()
            Step(step_type='exec', user_choice=choice).save()
            Step(step_type='pip', user_choice=choice).save()

        profiles = [
            EnvironmentProfile(user=self.user, description='oneses'),#, choices=UserChoice.objects.filter(priority=1)),
            EnvironmentProfile(user=self.user, description='twos'),#, choices=UserChoice.objects.filter(priority=2)),
            EnvironmentProfile(user=self.user, description='threes'),#, choices=UserChoice.objects.filter(priority=3)),
            ]

        for order, profile in enumerate(profiles):
            profile.save()
            sub_choices = UserChoice.objects.filter(priority=order+1)
            for item in sub_choices:
                profile.choices.add(item)

        response = self.client.get(reverse('installer_config:download_profile', kwargs={'pk': profiles[0].pk}))

        # Check that the steps for choices selected and only choices selected
        # for a given environment are present in the generated python file
        self.assertIn('# Download and run', response.content)
        self.assertIn('# Edit a file', response.content)
        self.assertIn('# Edit a profile', response.content)

    def test_choice_presence_set2(self):
        self.user.save()