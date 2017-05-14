from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Caracolien


# import os

# from selenium import webdriver


class CaracolienTests(TestCase):
    def setUp(self):
        for guy in 'abc':
            User.objects.create_user(guy, email='%s@example.org' % guy, password=guy)
        a, b, c = Caracolien.objects.order_by('pk')
        a.phone_number = '+33641452777'
        a.adhesion = date.today() - timedelta(days=100)
        b.adhesion = date.today() - timedelta(days=1000)
        a.save()
        b.save()

    # MODELS

    def test_caracolien_str(self):
        a, b, c = Caracolien.objects.order_by('pk')
        self.assertEqual(str(a), 'a')
        self.assertEqual(str(b), 'b')
        self.assertEqual(str(c), 'c')

    def test_adherent(self):
        a, b, c = Caracolien.objects.order_by('pk')
        self.assertTrue(a.adherent())
        self.assertFalse(b.adherent())
        self.assertFalse(c.adherent())

    # VIEWS

    def test_views_status(self):
        self.assertEqual(self.client.get(reverse('profil')).status_code, 302)
        self.client.login(username='a', password='a')
        self.assertEqual(self.client.get(reverse('profil')).status_code, 200)
        self.assertEqual(self.client.get(reverse('profil-password')).status_code, 200)

    def test_phone(self):
        self.client.login(username='b', password='b')
        self.client.post(reverse('profil'), {'phone_number': '06 424.83 000', 'address': ''})
        self.assertEqual(Caracolien.objects.get(user__username='b').phone_number, '+33642483000')


class RegistrationTests(TestCase):
    def test_registration(self):
        self.assertEqual(len(mail.outbox), 0)
        ret = self.client.post(reverse('registration_register'), {
            'username': 'pipo', 'email': 'pipo@bot.com', 'password1': 'Aik4aaPh', 'password2': 'Aik4aaPh'})
        self.assertEqual(ret.status_code, 302)
        ret = self.client.get(ret.url)
        self.assertIn("Veuillez consulter votre boîte mail pour terminer le processus d'enregistrement",
                      ret.content.decode())
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Activation du compte sur vide grenier caracole')
        self.assertIn('caracole.totheweb.fr/accounts/activate/', mail.outbox[0].body)


# TODO
# class CaracolienFunctionnalTests(TestCase):
#    def setUp(self):
#        if "TRAVIS" in os.environ:
#            capabilities = {
#                "tunnel-identifier": os.environ["TRAVIS_JOB_NUMBER"],
#                "build": os.environ["TRAVIS_BUILD_NUMBER"],
#                "tags": [os.environ["TRAVIS_PYTHON_VERSION"], "CI"],
#                'browserName': "firefox",
#                'platform': "Linux",
#                'version': "45.0",
#            }
#            hub_url = "%s:%s@localhost:4445/wd/hub" % (os.environ["SAUCE_USERNAME"], os.environ["SAUCE_ACCESS_KEY"])
#            self.browser = webdriver.Remote(desired_capabilities=capabilities, command_executor="http://%s" % hub_url)
#        else:
#            self.browser = webdriver.Firefox()

#    def tearDown(self):
#        self.browser.quit()

#    def test_simple_user(self):
#        self.browser.get('http://localhost:8000')
#        self.assertTrue(self.browser.title.startswith('Caracole'))
