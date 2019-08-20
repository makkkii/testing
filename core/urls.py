from django.urls import path
from django.views.generic import TemplateView

from .apps import CoreConfig
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.home, name='dashboard'),

    path('company/add/', view=views.company_create, name='company-add'),
    path('company/delete/<uuid:pk>/', view=views.company_delete, name='company-delete'),
    path('company/detail/<uuid:pk>/', view=views.company_detail, name='company-detail'),
    path('company/edit/<uuid:pk>/', view=views.company_update, name='company-edit'),
    path('company/list/', view=views.company_list, name='company-list'),

]

