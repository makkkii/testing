from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase, APIRequestFactory, force_authenticate
from core.models import Company, Timezone, Country, Address, State
from core_api.viewsets import CompanyViewSet

class CompanyTests(APITestCase):

  fixtures = [
      'core/fixtures/init.json'
    ]

  def setUp(self):
    """
    Setup class for creating initial data.
    """
    self.url = reverse('coreapi:company-list')
    self.username = 'testuser'
    self.password = 'test1245'
    self.user = User.objects.create(username=self.username,
    password=self.password)
    generate_initial_data()
  

  def test_company_list(self):
    """
    Test Company list view.
    """
    factory = APIRequestFactory()
    view = CompanyViewSet.as_view(actions={'get': 'list'})
    request = factory.get("")
    response_unauthenticated = view(request)
    self.assertEquals(response_unauthenticated.status_code, 403) # Without authentication ie. 403.
    force_authenticate(request, user=self.user)
    response_authenticated = view(request)
    self.assertEquals(response_authenticated.status_code, 200) # With authentication.

  def test_company_detail(self):
    factory = APIRequestFactory()
    view = CompanyViewSet.as_view(actions={'get': 'retrieve'})
    request = factory.get("")
    company_id = Company.objects.first().id
    response_unauthenticated = view(request, id=company_id)
    self.assertEquals(response_unauthenticated.status_code, 403) # Without authentication ie. 403.
    force_authenticate(request, user=self.user)
    response_authenticated = view(request, pk=company_id)
    self.assertEquals(response_authenticated.status_code, 200) # With authentication.

  def test_company_creation(self):
    client = APIClient()
    json_data = {
    "enabled": "false", "name": "testt", "phone": "testt", "fax": "testt",
    "email": "test@testtt.tt", "website": "https://test.testt",
    "facebook": "https://test.testt", "twitter": "https://test.testt",
    "linkedin": "https://test.testt", "instagram": "https://test.testt",
    "youtube": "https://test.testt", "status": "Active", "updated_by": 1,
    "timezone": Timezone.objects.first().id, "addresses": [Address.objects.first().id]
    }
    response_unauthenticated = client.post(path=self.url, format='json', data=json_data)
    self.assertEquals(response_unauthenticated.status_code, 403) # Without authentication.
    client.force_authenticate(user=self.user)
    response_authenticated = client.post(path=self.url, format='json', data=json_data)
    self.assertEquals(response_authenticated.status_code, 201) # With authentication. 



def generate_initial_data():
  Timezone.objects.create(utc='Etc/GMT+12', label='Dateline Standard Time',
    alias='DST', offset=-12, is_dst=True, description='(UTC-12:00) International Date Line West'
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