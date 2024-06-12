from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.test import TestCase

from portfolio.models import Site, Contact, Resume, JobApplication


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


class TestResumeModel(TestCase):
    user = None
    site = None
    resume = None

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345',
                                            email="test@example.com")
        cls.site = Site.objects.create(name='Test Site', user=cls.user, url='http://test.com')
        cls.resume = Resume.objects.create(name='Test Resume', site=cls.site, url='http://test.com')

    def test_create_resume(self):
        self.assertEqual(self.resume.name, 'Test Resume')
        self.assertEqual(self.resume.site, self.site)
        self.assertEqual(self.resume.url, 'http://test.com')

    def test_resume_str(self):
        self.assertEqual(str(self.resume), 'Test Resume')

    def test_resume_updated_time(self):
        self.resume.url = 'http://test2.com'
        self.resume.save()
        self.assertIsNotNone(self.resume.last_updated)
        self.assertIsNotNone(self.resume.created_at)
        self.assertNotEqual(self.resume.last_updated, self.resume.created_at)

    def test_resume_non_existent_site(self):
        test_site = Site(name='Test Site', user=self.user, url='http://test2.com')
        test_site.save()
        test_site.delete()
        with self.assertRaises(Exception) as raised:
            resume = Resume(name='Test Resume 2',
                            site=test_site,
                            url='http://test.com')
            resume.save()
        self.assertEqual(raised.exception.__class__, ValueError)


class TestJobApplicationModel(TestCase):
    user = None
    site = None
    resume = None
    job_application = None

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345',
                                            email="test@example.com")
        cls.site = Site.objects.create(name='Test Site', user=cls.user, url='http://test.com')
        cls.resume = Resume.objects.create(name='Test Resume', site=cls.site, url='http://test.com')
        cls.job_application = JobApplication.objects.create(title='Test Job Application',
                                                            company='Test Company',
                                                            url='http://test.com',
                                                            resume=cls.resume)

    def test_create_job_application(self):
        self.assertEqual(self.job_application.title, 'Test Job Application')
        self.assertEqual(self.job_application.company, 'Test Company')
        self.assertEqual(self.job_application.url, 'http://test.com')
        self.assertEqual(self.job_application.resume, self.resume)

    def test_job_application_str(self):
        self.assertEqual(str(self.job_application), 'Test Job Application')

    def test_job_application_updated_time(self):
        self.job_application.url = 'http://test2.com'
        self.job_application.save()
        self.assertIsNotNone(self.job_application.last_updated)
        self.assertIsNotNone(self.job_application.created_at)
        self.assertNotEqual(self.job_application.last_updated, self.job_application.created_at)

    def test_job_application_non_existent_resume(self):
        test_resume = Resume(name='Test Resume', site=self.site, url='http://test2.com')
        test_resume.save()
        test_resume.delete()
        with self.assertRaises(Exception) as raised:
            job_application = JobApplication(title='Test Job Application 2',
                                             company='Test Company 2',
                                             url='http://test.com',
                                             resume=test_resume)
            job_application.save()
        self.assertEqual(raised.exception.__class__, ValueError)
