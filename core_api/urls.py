from django.urls import path, include
from rest_framework import routers
from rest_framework.schemas import get_schema_view

from core_api.viewsets import *
from .apps import CoreApiConfig

router_v1 = routers.DefaultRouter()

router_v1.register(r'country', CountryViewSet, basename="country")
router_v1.register(r'company', CompanyViewSet, basename="company")
router_v1.register(r'state', StateViewSet, basename='states')
router_v1.register(r'timezone', TimezoneViewSet, basename='timezone')


schema_view = get_schema_view(title=CoreApiConfig.verbose_name)


app_name = 'core_api'
urlpatterns = [
    path('', include(router_v1.urls)),
]
