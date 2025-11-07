from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import MarketingJob, Proposal


User = get_user_model()


class MarketingTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_job_requires_login(self):
        url = reverse('marketing:job_create')
        resp = self.client.get(url)
        # should redirect to login
        self.assertEqual(resp.status_code, 302)

    def test_proposal_post_creates_proposal(self):
        # create poster and provider
        poster = User.objects.create_user('poster', password='x')
        provider = User.objects.create_user('provider', password='x')
        job = MarketingJob.objects.create(title='Test', description='web site', poster=poster)

        self.client.login(username='provider', password='x')
        url = reverse('marketing:proposal_create', kwargs={'pk': job.pk})
        resp = self.client.post(url, {'message': 'I can help', 'price': '100.00', 'eta_days': 5})
        self.assertIn(resp.status_code, (200, 302))
        self.assertEqual(Proposal.objects.filter(job=job, provider=provider).count(), 1)


