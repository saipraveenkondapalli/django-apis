from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.test import TestCase

from portfolio.models import Site, Contact


class TestSiteModel(TestCase):
    user = None

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345',
                                            email="test@test.com")
        cls.site = Site.objects.create(name='Test Site', user=cls.user, url='http://test.com')

    def test_site_model(self):
        self.assertEqual(self.site.name, 'Test Site')
        self.assertEqual(self.site.url, 'http://test.com')
        self.assertEqual(self.site.user, self.user)

    def test_site_str(self):
        self.assertEqual(str(self.site), 'Test Site')

    def test_sites_are_unique(self):
        with self.assertRaises(Exception) as raised:
            Site.objects.create(name='Test Site', user=self.user, url='http://test.com')
        self.assertEqual(raised.exception.__class__, IntegrityError)


class TestModelContact(TestCase):
    site = None
    user = None

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345',
                                            email="test@test.com")
        cls.site = Site.objects.create(name='Test Site', user=cls.user, url='http://test.com')

        cls.contact = Contact.objects.create(name='Test Contact User',
                                             email='contact@test.com',
                                             message='Test Message',
                                             site=cls.site)

    def test_contact_model(self):
        self.assertEqual(self.contact.name, 'Test Contact User')
        self.assertEqual(self.contact.email, 'contact@test.com')
        self.assertEqual(self.contact.message, 'Test Message')
        self.assertEqual(self.contact.site, self.site)

    def test_contact_str(self):
        self.assertEqual(str(self.contact), f'{self.contact.name} - {self.site.name} - {self.contact.created_at}')

    def test_contact_non_existent_site(self):
        test_site = Site(name='Test Site', user=self.user, url='http://test2.com')
        test_site.save()  # save the site
        test_site.delete()  # delete the site to simulate a non-existent site
        with self.assertRaises(Exception) as raised:
            contact = Contact(name='Test Contact User 2',
                              email="contact2@gmail.com",
                              message="Test Message 2",
                              site=test_site)
            contact.save()
        self.assertEqual(raised.exception.__class__, ValueError)
