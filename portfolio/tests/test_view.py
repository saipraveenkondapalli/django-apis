from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from portfolio.models import Site


class TestSiteView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password="12345")
        self.client.login(username='testuser', password='12345')
        self.site = Site.objects.create(name='Test Site', user=self.user, url='http://test.com')

        self.site_view_url = reverse('portfolio:dashboard')
        self.site_delete_view_url = reverse('portfolio:delete_site', args=[self.site.client_id])

    def test_site_view_GET(self):
        response = self.client.get(self.site_view_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/dashboard.html')
        self.assertContains(response, 'Test Site')
        self.assertContains(response, 'http://test.com')

    def test_site_view_Search_GET(self):
        response = self.client.get(self.site_view_url + '?search=Test Site')

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/dashboard.html')
        self.assertContains(response, 'Test Site')
        self.assertContains(response, 'http://test.com')

    def test_site_view_search_no_result_GET(self):
        response = self.client.get(self.site_view_url + '?search=Test Site 2')

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/dashboard.html')
        self.assertNotContains(response, 'Test Site')
        self.assertNotContains(response, 'http://test.com')
        self.assertContains(response, 'No sites')

    def test_site_delete_view_GET(self):
        response = self.client.get(self.site_delete_view_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/site_confirm_delete_view.html')
        self.assertContains(response, 'Are you sure you want to delete')
        self.assertContains(response, 'Test Site')

    def test_site_delete_view_POST(self):
        response = self.client.post(self.site_delete_view_url, follow=True)

        messages = list(response.context.get('messages'))
        self.assertEqual(str(messages[0]), 'Site deleted successfully')

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/dashboard.html')

        self.assertEquals(Site.objects.count(), 0)

    def test_site_delete_view_POST_unauthorized(self):
        # create a new post with a different user
        user = User.objects.create_user(username='testuser2', password="12345")
        site = Site.objects.create(name='Test Site2', user=user, url='http://test2.com')
        site_delete_view_url = reverse('portfolio:delete_site', args=[site.client_id])  # get the url for the new post

        # use user 1 to delete user 2's post
        response = self.client.post(site_delete_view_url, follow=True)

        # check if the user is redirected to the dashboard
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/dashboard.html')

        # check if the user gets an error message

        messages = list(response.context.get('messages'))
        self.assertEqual(str(messages[0]), 'You are not authorized to delete this site')

        # check if the post still exists
        self.assertEquals(Site.objects.get(client_id=site.client_id).name, 'Test Site2')
