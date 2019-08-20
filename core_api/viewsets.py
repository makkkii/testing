from rest_framework import viewsets

from core.models import Company, Address, Timezone
from core_api.serializers import CompanySerializer, AddressSerializer, TimezoneSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given Company.

    list:
    Return a list of all the existing Companies.

    create:
    Create a new Company instance.

    update:
    Update existing Company instance.

    partial_update:
    Partial update existing Company instance.

    destroy:
    Destroy existing Company instance.
    """

    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class AddressViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given Address.

    list:
    Return a list of all the existing Companies.

    create:
    Create a new Address instance.

    update:
    Update existing Company instance.

    partial_update:
    Partial update existing Company instance.

    destroy:
    Destroy existing Company instance.
    """

    def get_queryset(self):
        """
        This view should return a list of all the Profiles for
        the user as determined by currently logged in user.
        """
        queryset = Address.objects.all()
        if not ((self.request.user.is_superuser or self.request.user.is_staff) and self.request.user.company is None):
            queryset.filter(company=self.request.user.company)
        return queryset

    serializer_class = AddressSerializer


class CountryViewSet(viewsets.ModelViewSet):

    queryset = Timezone.objects.all()

    def get_queryset(self):
        """
        This view should return a list of all the Timezones except those disabled.
        """
        return Timezone.objects.filter(enabled=True)

    serializer_class = TimezoneSerializer


class StateViewSet(viewsets.ModelViewSet):

    queryset = Timezone.objects.all()

    def get_queryset(self):
        """
        This view should return a list of all the Timezones except those disabled.
        """
        return Timezone.objects.filter(enabled=True)

    serializer_class = TimezoneSerializer


class TimezoneViewSet(viewsets.ModelViewSet):

    queryset = Timezone.objects.all()

    def get_queryset(self):
        """
        This view should return a list of all the Timezones except those disabled.
        """
        return Timezone.objects.filter(enabled=True)

    serializer_class = TimezoneSerializer
















