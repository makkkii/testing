import logging
import re
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext as _

auto_manage = True
UserModel = get_user_model()
SELECT_EMPTY = ('', '------')

CONTACT_MODULE = "contact"
TIME_MODULE = "time"
MAINTENANCE_MODULE = "maintenance"
ACCOUNTING_MODULE = "accounting"
SUCCESS_MODULE = "success"
TEAM_MODULE = "team"
LEAD_MODULE = "lead"
PROCESS_MODULE = "process"
COMMUNICATION_MODULE = "communication"

log = logging.getLogger("{}.*".format(__package__))
log.setLevel(settings.LOGGING_LEVEL)


class BaseModel(models.Model):
    _batch_id = None
    _original = {}
    _editable_together = []

    class Meta:
        abstract = True


class StampedModel(BaseModel):

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    enabled = models.BooleanField(default=True, )

    class Meta:
        abstract = True


class StampedUpdaterModel(StampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    updated_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def update_tracked(self, user):
        self.updated_by = user

    class Meta:
        abstract = True


class TrackedModel(StampedUpdaterModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def update_tracked(self, user):
        self.updated_by = user

    class Meta:
        abstract = True


class Address(TrackedModel):
    BILLING = "Billing"; RESIDENTIAL = "Residential"; OFFICE = "Office"; BUILDING = "Building"; UNIT = "Unit";
    TYPES = (SELECT_EMPTY, (BILLING, "Billing"), (BUILDING, "Building"), (RESIDENTIAL, "Residential"), (OFFICE, "Office"))
    OFFICIAL_TYPE = (SELECT_EMPTY, (BILLING, "Billing"), (OFFICE, "Office"))
    NO_BILLING = (SELECT_EMPTY, (RESIDENTIAL, "Residential"), (OFFICE, "Office"))

    type = models.CharField(max_length=32, verbose_name="Address Type", choices=TYPES)
    line_1 = models.CharField(max_length=254, verbose_name="Address")
    line_2 = models.CharField(max_length=254, verbose_name="Ste or Apt", null=True, blank=True, default=None)
    city = models.CharField(max_length=32)
    state = models.ForeignKey('State', on_delete=models.PROTECT)
    zip = models.CharField(max_length=8)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, default="us", )
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.line_1

    def can_save(self):
        if self.type and self.line_1 and self.city and self.state and self.zip and self.country:
            return True
        return False

    @classmethod
    def get_add_url(cls):
        return reverse('core:address-add')

    @classmethod
    def get_list_url(cls):
        return reverse('core:address-list')

    # def get_absolute_url(self):
    #     return reverse('core:address-detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('core:address-edit', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('core:address-delete', kwargs={'pk': self.pk})

    def get_admin_url(self):
        return reverse('admin:{}_{}_change'.format(self._meta.app_label, self._meta.model_name), args=(self.pk,))

    class Meta:
        ordering = ('line_1',)
        managed = auto_manage
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')


class Company(StampedUpdaterModel):
    """
    Company model:
    A property management company is a SavvyBiz customer.

    """
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    STATUS = (
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive")
    )



    # On Completion submit to our Lead Developer Paul Via Sk ype @pauldiconline
    name = models.CharField(_('name'), max_length=254, unique=True)
    phone = models.CharField(_('phone'), max_length=15)
    fax = models.CharField(_('fax'), max_length=15, default=None, null=True, blank=True)
    email = models.EmailField(_('email'), max_length=128)
    website = models.URLField(_('website'), max_length=254, default=None, null=True, blank=True)
    facebook = models.URLField(_('facebook link'), max_length=254, default=None, null=True, blank=True)
    twitter = models.URLField(_('twitter link'), max_length=254, default=None, null=True, blank=True)
    linkedin = models.URLField(_('linkedIn link'), max_length=254, default=None, null=True, blank=True)
    instagram = models.URLField(_('instagram link'), max_length=254, default=None, null=True, blank=True)
    youtube = models.URLField(_('youtube channel'), max_length=254, default=None, null=True, blank=True)
    timezone = models.ForeignKey("Timezone", on_delete=models.CASCADE)
    addresses = models.ManyToManyField(Address, related_name="companies")

    status = models.CharField(max_length=16, choices=STATUS, default=ACTIVE)

    @property
    def default_address(self):
        return self.addresses.filter(default=True).order_by("updated").first()

    @classmethod
    def companies(cls):
        items = [(c.id, c.name) for c in cls.objects.all()]
        items.insert(0, ("aaaa0000-bb11-cc22-dd33-eeeeee555555", "--- SavvyBiz ---"))
        return items

    class Meta:
        ordering = ('name',)
        managed = auto_manage
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    def __str__(self):
        return "{}".format(self.name)

    def get_admin_url(self):
        return reverse('admin:{}_{}_change'.format(self._meta.app_label, self._meta.model_name), args=(self.pk,))

    @classmethod
    def get_add_url(cls):
        return reverse('core:company-add')

    @classmethod
    def get_list_url(cls):
        return reverse('core:company-list')

    def get_absolute_url(self):
        return reverse('core:company-detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('core:company-edit', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('core:company-delete', kwargs={'pk': self.pk})

    def get_absolute_api_url(self):
        return reverse('core_api:company-detail', kwargs={'pk': self.pk})


class Country(BaseModel):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=64)
    name_plain = models.CharField(max_length=64)
    is_active = models.BooleanField(default=False)
    dial_code = models.CharField(max_length=4, blank=True, null=True)
    flag = models.CharField(max_length=4, blank=True, null=True)
    capital = models.CharField(max_length=64, blank=True, null=True)
    region = models.CharField(max_length=64, blank=True, null=True)
    region_des = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_admin_url(self):
        return reverse('admin:{}_{}_change'.format(self._meta.app_label, self._meta.model_name), args=(self.pk,))

    class Meta:
        ordering = ('name',)
        managed = auto_manage
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')


class State(BaseModel):
    code = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=64)
    capital = models.CharField(max_length=64, null=True, blank=True, default=None)
    appellation = models.CharField(max_length=64, null=True, blank=True, default=None)
    country = models.ForeignKey(Country, models.DO_NOTHING, db_column='country', default="us")

    def __str__(self):
        return self.name

    def get_admin_url(self):
        return reverse('admin:{}_{}_change'.format(self._meta.app_label, self._meta.model_name), args=(self.pk,))

    class Meta:
        ordering = ('name',)
        managed = auto_manage
        verbose_name = _('State')
        verbose_name_plural = _('States')


class Timezone(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utc = models.CharField(_('utc'), max_length=64, db_index=True)
    label = models.CharField(_('label'), max_length=64)
    alias = models.CharField(_('alias'), max_length=8)
    offset = models.IntegerField(_('offset'),)
    is_dst = models.BooleanField(_('is dst'),)
    description = models.CharField(_('description'), max_length=128)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        # return "{} ({})".format(self.description, self.utc)
        return self.utc

    class Meta:
        ordering = ('offset',)
        managed = auto_manage
        verbose_name = _('Timezone')
        verbose_name_plural = _('Timezones')

