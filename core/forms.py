import logging

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import ProgrammingError
from django.forms import modelformset_factory
from django.utils.safestring import mark_safe

from core.models import Timezone, Company, Address

log = logging.getLogger("{}.*".format(__package__))
log.setLevel(settings.LOGGING_LEVEL)

UserModel = get_user_model()


class StampedUpdaterModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(StampedUpdaterModelForm, self).__init__(*args, **kwargs)  # populates the post

        if self.fields.get("updated_by", False):
            del self.fields["updated_by"]


class TrackedModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TrackedModelForm, self).__init__(*args, **kwargs)  # populates the post

        if self.fields.get("company", False):
            del self.fields["company"]

        if self.fields.get("updated_by", False):
            del self.fields["updated_by"]


class AddressForm(TrackedModelForm):

    # def __init__(self, *args, **kwargs):
    #     self.readonly = kwargs.pop('readonly', False)
    #     self.types = kwargs.pop('types', None)

    class Meta:
        model = Address
        # fields = '__all__'
        exclude = ('country', 'enabled')

        widgets = {
            'state': forms.Select(attrs={'class': 'form-control select2', 'data-type': 'select2'}),
            'type': forms.Select(attrs={'class': 'form-control select2', 'data-type': 'select2'}),
        }


try:
    AddressFormSet = modelformset_factory(Address, form=AddressForm, extra=1, max_num=len(Address.OFFICIAL_TYPE) - 1,
                                          can_delete=True)
except ProgrammingError:
    AddressFormSet = modelformset_factory(Address, form=AddressForm, extra=1, max_num=0, can_delete=True)


class CompanyForm(StampedUpdaterModelForm):

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)  # populates the post

        self.fields['timezone'].queryset = Timezone.objects.filter(enabled=True)
        self.fields['timezone'].label = "Time Zone"

    class Meta:
        model = Company
        fields = '__all__'
        exclude = ('addresses', 'alias', 'enabled',)

        widgets = {
            'timezone': forms.Select(attrs={'class': 'form-control select2'}),
            'status': forms.Select(attrs={'class': 'form-control select2'}),
            'state': forms.Select(attrs={'class': 'form-control select2'}),
            # 'about': forms.Textarea(attrs={'rows': 2}),
            # 'note': forms.Textarea(attrs={'rows': 2}),
        }















