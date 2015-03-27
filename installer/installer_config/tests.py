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


class ChoiceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = UserChoice

    name = factory.Sequence(lambda n: u'name%d' % n)
    description = factory.Sequence(lambda n: u'description%d' % n)
    category = 'core'
    priority = 1


def login_user(driver, user, password):
    """login user"""
    driver.get(TEST_DOMAIN_NAME + reverse('auth_login'))
    username_field = driver.find_element_by_id('id_username')
    username_field.send_keys(user)
    password_field = driver.find_element_by_id('id_password')
    password_field.send_keys(password)
    form = driver.find_element_by_tag_name('form')
    form.submit()


class UserProfileDetailTestCase(LiveServerTestCase):
    """This class is for testing user login form"""
    def setUp(self):
        self.driver = webdriver.Firefox()
        super(UserProfileDetailTestCase, self).setUp
        self.user = User(username='user1')
        self.user.set_password('pass')
        self.user.is_active = True
        self.choice = []
        for i in range(3):
            self.choice.append(ChoiceFactory())
            self.choice[i].save()

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

    def test_create_profile_all(self):
        """If all choices selected, all are in the created profile"""
        # .save() is here instead of setUp to save time
        self.user.save()
        self.login_user('user1', 'pass')
        self.driver.get(TEST_DOMAIN_NAME +
                        reverse('installer_config:CreateEnv'))
        self.assertIn("profileform", self.driver.page_source)
        # fill out form
        description = "Test description."
        field = self.driver.find_element_by_id('id_description')
        field.send_keys(description)
        for i in range(3):
            choice = "".join(['id_choices_', str(i)])
            field = self.driver.find_element_by_id(choice)
            field.click()
        form = self.driver.find_element_by_tag_name('form')
        form.submit()
        # check if profile is created
        self.assertIn("userprofile", self.driver.page_source)
        self.assertIn(description, self.driver.page_source)
        # check script has the choices
        link = self.driver.find_elements_by_link_text('Test description.')
        link[0].click()
        for i in range(3):
            self.assertIn(self.choice[i].name, self.driver.page_source)
            self.assertIn(self.choice[i].description, self.driver.page_source)


    def test_create_profile_not_all(self):
        """If not all choices selected, the right ones are produced"""
        # .save() is here instead of setUp to save time
        self.user.save()
        self.login_user('user1', 'pass')
        self.driver.get(TEST_DOMAIN_NAME +
                        reverse('installer_config:CreateEnv'))
        self.assertIn("profileform", self.driver.page_source)
        # fill out form
        description = "Test description."
        field = self.driver.find_element_by_id('id_description')
        field.send_keys(description)
        for i in range(2):
            choice = "".join(['id_choices_', str(i)])
            field = self.driver.find_element_by_id(choice)
            field.click()
        form = self.driver.find_element_by_tag_name('form')
        form.submit()
        # check if profile is created
        self.assertIn("userprofile", self.driver.page_source)
        self.assertIn(description, self.driver.page_source)
        # check script has the choices
        link = self.driver.find_elements_by_link_text('Test description.')
        link[0].click()
        for i in range(2):
            self.assertIn(self.choice[i].name, self.driver.page_source)
            self.assertIn(self.choice[i].description, self.driver.page_source)
        # if not selected, then not in page that displays choices
        self.assertNotIn(self.choice[2].name, self.driver.page_source)
        self.assertNotIn(self.choice[2].description, self.driver.page_source)

# Will use these to write update and delete tests

    # def test_update_profile(self):
    #     # .save() is here instead of setUp to save time
    #     self.user.save()
    #     login_user(self.driver, 'user1', 'pass')
    #     self.driver.get(TEST_DOMAIN_NAME +
    #                     reverse('installer_config:UpdateEnv',
    #                             kwargs={'pk': self.user.pk}))
    #     self.assertIn("profileform", self.driver.page_source)


    # def test_delete_profile(self):
    #     # .save() is here instead of setUp to save time
    #     self.user.save()
    #     login_user(self.driver, 'user1', 'pass')
    #     self.driver.get(TEST_DOMAIN_NAME +
    #                     reverse('installer_config:DeleteEnv',
    #                             kwargs={'pk': self.user.pk}))
    #     self.assertIn("profileform", self.driver.page_source)


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
        inputs, profiles, choices = set_data(self.user)
        response = self.client.get(reverse('installer_config:download_profile', kwargs={'pk': profiles[0].pk}))

        # Verify that choices selected are present
        self.assertIn('# For choice important thing', response.content)
        self.assertIn('# For choice your env', response.content)
        self.assertIn('# For choice get', response.content)

        # Check that the steps for choices selected and only choices selected
        # for a given environment are present in the generated python file
        self.assertIn('# Download and run', response.content)
        self.assertIn('# Edit a file', response.content)
        self.assertIn('# Edit a profile', response.content)

        # Verify choices that don't belong are not present
        self.assertNotIn('# Add a key, value pair', response.content)
        self.assertNotIn('"Executing " + \' \'.join(command_line)', response.content)
        self.assertNotIn('# Pip install, assuming', response.content)

    def test_choice_presence_set2(self):
        self.user.save()
        inputs, profiles, choices = set_data(self.user)
        response = self.client.get(reverse('installer_config:download_profile', kwargs={'pk': profiles[1].pk}))

        self.assertIn('# For choice bash shenanigannns', response.content)
        self.assertIn('# For choice text editor', response.content)

        self.assertIn('# Add a key, value pair', response.content)
        self.assertIn('"Executing " + \' \'.join(command_line)', response.content)
        self.assertIn('# Pip install, assuming', response.content)

        self.assertNotIn('# Download and run', response.content)
        self.assertNotIn('# Edit a file', response.content)
        self.assertNotIn('# Edit a profile', response.content)

    def test_choice_presence_set3(self):
        self.user.save()
        inputs, profiles, choices = set_data(self.user)
        response = self.client.get(reverse('installer_config:download_profile', kwargs={'pk': profiles[2].pk}))

        self.assertIn('# For choice a pip package', response.content)
        self.assertIn('# For choice other', response.content)

        # Verify no steps for this set of choices
        self.assertNotIn('# Download and run', response.content)
        self.assertNotIn('# Edit a file', response.content)
        self.assertNotIn('# Edit a profile', response.content)
        self.assertNotIn('# Add a key, value pair', response.content)
        self.assertNotIn('"Executing " + \' \'.join(command_line)', response.content)
        self.assertNotIn('# Pip install, assuming', response.content)

def set_data(user):
    inputs = [('important thing', 'core', 1),
                ('your env', 'env', 1),
                ('get', 'git', 1),
                ('bash shenanigannns', 'prompt', 2),
                ('text editor', 'subl', 2),
                ('a pip package', 'pkg', 3),
                ('other', 'other', 3),]

    choices = []
    for name, category, priority in inputs:
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
        EnvironmentProfile(user=user, description='oneses'),#, choices=UserChoice.objects.filter(priority=1)),
        EnvironmentProfile(user=user, description='twos'),#, choices=UserChoice.objects.filter(priority=2)),
        EnvironmentProfile(user=user, description='threes'),#, choices=UserChoice.objects.filter(priority=3)),
        ]

    for order, profile in enumerate(profiles):
        profile.save()
        sub_choices = UserChoice.objects.filter(priority=order+1)
        for item in sub_choices:
            profile.choices.add(item)

    return inputs, profiles, choices

class UserProfileShowTestCase(LiveServerTestCase):
    """User profiles and choices display properly"""
    def setUp(self):
        self.driver = webdriver.Firefox()
        super(UserProfileShowTestCase, self).setUp
        self.user = User(username='user1')
        self.user.set_password('pass')
        self.user.is_active = True
        self.client = Client()

    def tearDown(self):
        self.driver.refresh()
        self.driver.quit()
        super(UserProfileShowTestCase, self).tearDown()

    def test_show_profile_all(self):
        """Profiles are in the created profile list."""
        # .save() is here instead of setUp to save time
        self.user.save()
        login_user(self.driver, 'user1', 'pass')
        self.profiles = set_data(self.user)[1]
        self.driver.implicitly_wait(2)

        self.driver.get(TEST_DOMAIN_NAME + reverse('profile'))

        # make sure all profiles are in profile page
        for profile in self.profiles:
            self.assertIn(profile.description, self.driver.page_source)

    def test_show_profile_choices(self):
        """Test for all choices in each profile list"""
        # .save() is here instead of setUp to save time
        self.user.save()
        login_user(self.driver, 'user1', 'pass')
        self.profiles = set_data(self.user)[1]
        self.driver.implicitly_wait(2)

        # go to each profile page and see if all choices are in them
        for profile in self.profiles:
            self.driver.get(TEST_DOMAIN_NAME + reverse('profile'))
            link = self.driver.find_elements_by_link_text(
                profile.description)
            link[0].click()
            for choice in profile.choices.all():
                self.assertIn(choice.description, self.driver.page_source)

class UserProfileDownloadTestCase(LiveServerTestCase):
    """User profile downloading properly"""
    def setUp(self):
        self.driver = webdriver.Firefox()
        super(UserProfileDownloadTestCase, self).setUp
        self.user = User(username='user1')
        self.user.set_password('pass')
        self.user.is_active = True
        self.client = Client()

    def tearDown(self):
        self.driver.refresh()
        self.driver.quit()
        super(UserProfileDownloadTestCase, self).tearDown()

    def test_show_profile_choices(self):
        """Test that download link exists for all choices in each profile list"""
        # .save() is here instead of setUp to save time
        self.user.save()
        login_user(self.driver, 'user1', 'pass')
        self.profiles = set_data(self.user)[1]
        self.driver.implicitly_wait(2)

        # go to each profile page and see if all choices are in them
        for profile in self.profiles:
            self.driver.get(TEST_DOMAIN_NAME + reverse('profile'))
            link = self.driver.find_elements_by_link_text(
                profile.description)
            link[0].click()
            # find the download link inside the profile detail page
            link = self.driver.find_elements_by_link_text('')
            self.assertTrue(link)
            
