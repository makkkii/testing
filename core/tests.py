from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from core.models import Company, Timezone, Country, Address, State
from core.forms import CompanyForm


class CompanyTests(TestCase):
  fixtures = [
    'core/fixtures/init.json'
  ]

  def setUp(self):
    self.client = Client()
    self.url = reverse('core:company-add')
    self.user = User.objects.create_user('testuser', 'test@test.com', 'test@1234')
    generate_initial_data()

  def test_template_rendered(self):
    self.client.login(username='testuser', password='test@1234')
    response = self.client.get(self.url)
    response.client = Client()
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'core/company-form.html')

  def test_uses_company_form(self):
    self.client.login(username='testuser', password='test@1234')
    response = self.client.get(self.url)
    self.assertIsInstance(response.context['company_form'], CompanyForm)

  def test_company_creation(self):
    self.client.login(username='testuser', password='test@1234')
    form = CompanyForm({
      "enabled": "false", "name": "testt", "phone": "testt", "fax": "testt",
      "email": "test@testtt.tt", "website": "https://test.testt",
      "facebook": "https://test.testt", "twitter": "https://test.testt",
      "linkedin": "https://test.testt", "instagram": "https://test.testt",
      "youtube": "https://test.testt", "status": "Active", "updated_by": 1,
      "timezone": Timezone.objects.filter(utc__iexact='Pacific/Midway').first().id, "addresses": [Address.objects.first().id]
    })
    self.assertTrue(form.is_valid())
    current_objs = Company.objects.count() # No. of objects before saving the form.
    company = form.save(commit=False)
    company.update_tracked(self.user)
    company.save()
    self.assertEqual(Company.objects.count(), current_objs + 1) # Object count increased by 1 after successful form save.
    



def generate_initial_data():
  username = 'testtest'
  password = '1111@test'
  User.objects.create(username=username,
  password=password)

  Timezone.objects.create(utc='Pacific/Midway', label='UTC-11',
    alias='U', offset=-11, is_dst=False, description='(UTC-11:00) Coordinated Universal Time-11'
  )

  Company.objects.create(name='Test company name',phone='235125554',fax='e52415454',
        email='test@test.com',website='https://test.test',facebook='https://test.test',
        twitter='https://test.test',linkedin='https://test.test',instagram='https://test.test',
        youtube='https://test.test', timezone=Timezone.objects.first(), status='Active',updated_by_id=1    
      )
  
  Address.objects.create(type="Billing", line_1="Whitefield Boulevard", line_2="Manhattan",
        city="Newyork", state=State.objects.first(), country=Country.objects.first(), zip="12345678",
        updated_by_id=1
    )