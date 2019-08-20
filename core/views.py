import json
import logging

from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction, IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from core.forms import CompanyForm, AddressFormSet
from core.models import Company, Address

log = logging.getLogger("{}.*".format(__package__))
log.setLevel(settings.LOGGING_LEVEL)

UserModel = get_user_model()
TITLE_SUCCESS = "Success Response!!!"
TITLE_ERROR = "Error Response!!!"
DUPLICATE_ERROR = "Attempt to create a duplicate entry for '{}' has been averted"
FORM_ERROR = "Please check you have filled the form correctly"
INVALD_TIMEZONE_WARNING = "Your profile have invalid Timezone and this may result to inconsistent datetime"

ADDED_SUCCESS = "{} ({}) successfully added"
CREATE_SUCCESS = "{} ({}) successfully created"
UPDATE_SUCCESS = "{} <i>({})</i> successfully updated"
DELETE_SUCCESS = "{} ({}) successfully deleted"

TYPE_INFO = "info"
TYPE_SUCCESS = "success"
TYPE_ERROR = "error"


def index(request):
    # On Completion submit to our Lead Developer Paul Via Sk ype @pauldiconline
    if request.user.is_authenticated:
        return redirect(reverse("core:dashboard"))
    return render(request, "core/home.html", context={})


@login_required
def home(request):
    context = {}
    # On Completion submit to our Lead Developer Paul Via Sk ype @pauldiconline
    return render(request, "core/dashboard.html", context=context)


def error_403(request, exception):
    """
    Page not found Error 404
    """

    return render(request, 'core/403.html', context={})


def error_404(request, exception):
    log.error("****** 404")
    return render(request, 'core/404.html', context={})


def error_500(request):
    log.error("****** 500")
    return render(request, 'core/500.html', context={})


@login_required
def company_create(request, item=None):
    if request.method == "POST":
        company_form = CompanyForm(request.POST, prefix='company', request=request, instance=item)
        address_formset = AddressFormSet(request.POST, prefix='address',
                                         queryset=item.addresses.all() if item else Address.objects.none())

        if company_form.is_valid() and address_formset.is_valid():
            with transaction.atomic():
                company = company_form.save(commit=False)
                company.update_tracked(auth.get_user(request))
                addresses = address_formset.save(commit=False)
                try:
                    company.save()

                    for address in addresses:
                        address.update_tracked(auth.get_user(request))
                        address.save()

                    company.addresses.set(addresses)
                except IntegrityError as err:
                    log.error(err)
                    ok = False
                    transaction.set_rollback(rollback=True)
                    msg = "Sorry, alias '{}' not allowed".format("...")
                    if request.is_ajax():
                        return JsonResponse({"msg": msg, "type": FORM_ERROR, "data": {"pk": company_form.instance.pk}}, safe=True)
                    else:
                        messages.warning(request, msg)

                # company_form.save_m2m()

                msg = UPDATE_SUCCESS.format(company._meta.verbose_name, company) if item else CREATE_SUCCESS.format(company._meta.verbose_name, company)
                if request.is_ajax():
                    return JsonResponse({"msg": msg, "type": TYPE_SUCCESS, "data": {"pk": company_form.instance.pk}}, safe=True)
                else:
                    messages.success(request, msg, TITLE_SUCCESS)
                    return redirect(company_form.instance.get_absolute_url())
        else:
            logging.warning(json.dumps(company_form.errors))
            logging.warning(json.dumps(address_formset.errors))
            if request.is_ajax():
                data = {**json.dumps(company_form.errors), **json.dumps(address_formset.errors)}
                return JsonResponse({"msg": FORM_ERROR, "type": TYPE_INFO, "data": data}, safe=True)
            else:
                messages.warning(request, FORM_ERROR, TITLE_ERROR)
    else:
        company_form = CompanyForm(prefix='company', request=request, instance=item)
        address_formset = AddressFormSet(prefix='address', queryset=item.addresses.all() if item else Address.objects.none())

    template = "core/company-form.html" if request.is_ajax() else "core/company-add.html"
    context = {'company_form': company_form, 'address_formset': address_formset}

    return render(request, template, context=context)


@login_required
def company_update(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == "POST" and request.is_ajax() and request.POST.get("level_0_limit", False):
        company.save()
        return JsonResponse({"msg": "Email Timeout Limits Updated", "type": TYPE_SUCCESS, "data": {}}, safe=True)

    return company_create(request, company)


@login_required
def company_list(request):
    items = Company.objects.all()
    return render(request, "core/company-list.html", context={"items": items})


@login_required
def company_detail(request, pk):
    instance = Company.objects.get(pk=pk)

    return render(request, "core/company-add.html", context={"instance": instance, "domain": get_current_site(request)})


@login_required
def company_delete(request, pk):
    item = get_object_or_404(Company, pk=pk)
    msg = DELETE_SUCCESS.format(item._meta.verbose_name, item)
    item.delete()

    if request.is_ajax():
        return JsonResponse({"msg": msg, "type": TYPE_SUCCESS}, safe=True)
    else:
        messages.warning(request, msg, TITLE_SUCCESS)
    return redirect(Company.get_list_url())

















