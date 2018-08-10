import random
import string

from django.shortcuts import render, redirect, reverse
from django.urls.exceptions import NoReverseMatch
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseBadRequest
from scatterauth.forms import LoginForm, SignupForm
from django.utils.translation import ugettext_lazy as _
from scatterauth.settings import app_settings
from django.views.decorators.csrf import csrf_exempt
import json
from django.http.request import split_domain_port


def get_redirect_url(request):
    if request.GET.get('next'):
        return request.GET.get('next')
    elif request.POST.get('next'):
        return request.POST.get('next')
    elif settings.LOGIN_REDIRECT_URL:
        try:
            url = reverse(settings.LOGIN_REDIRECT_URL)
        except NoReverseMatch:
            url = settings.LOGIN_REDIRECT_URL
        return url



@require_http_methods(["POST"])
def login_api(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        signature, pubkey = form.cleaned_data.get("signature"), form.cleaned_data.get("pubkey")
        if not signature or not pubkey:
            return JsonResponse({'error': _(
                "Please pass signature and public key"),
                'success': False})
        if app_settings.SCATTERAUTH_DOMAIN == '':
            host = request.get_host()
            domain, port = split_domain_port(host)
            msg = domain
        else:
            msg = app_settings.SCATTERAUTH_DOMAIN
        user = authenticate(request, msg=msg, pubkey=pubkey, signature=signature)
        if user:
            login(request, user, 'scatterauth.backend.ScatterAuthBackend')
            return JsonResponse({'success': True, 'redirect_url': get_redirect_url(request)})
        else:
            error = _("Can't find a user for the provided signature with public key {pubkey}").format(
                pubkey=pubkey)
            return JsonResponse({'success': False, 'error': error})
    else:
        return JsonResponse({'success': False, 'error': json.loads(form.errors.as_json())})


@csrf_exempt
@require_http_methods(["POST"])
def signup_api(request):
    if not app_settings.SCATTERAUTH_SIGNUP_ENABLED:
        return JsonResponse({'success': False, 'error': _("Sorry, signup's are currently disabled")})
    form = SignupForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        pubkey_field = app_settings.SCATTERAUTH_USER_PUBKEY_FIELD
        setattr(user, pubkey_field, form.cleaned_data[pubkey_field])
        user.save()
        login(request, user, 'scatterauth.backend.ScatterAuthBackend')
        return JsonResponse({'success': True, 'redirect_url': get_redirect_url(request)})
    else:
        return JsonResponse({'success': False, 'error': json.loads(form.errors.as_json())})


@require_http_methods(["GET", "POST"])
def signup_view(request, template_name='scatterauth/signup.html'):
    """
    1. Creates an instance of a SignupForm.
    2. Checks if the registration is enabled.
    3. If the registration is closed or form has errors, returns form with errors
    4. If the form is valid, saves the user without saving to DB
    5. Sets the user address from the form, saves it to DB
    6. Logins the user using scatterauth.backend.ScatterAuthBackend
    7. Redirects the user to LOGIN_REDIRECT_URL or 'next' in get or post params
    :param request: Django request
    :param template_name: Template to render
    :return: rendered template with form
    """
    form = SignupForm()
    if not app_settings.SCATTERAUTH_SIGNUP_ENABLED:
        form.add_error(None, _("Sorry, signup's are currently disabled"))
    else:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                pubkey_field = app_settings.SCATTERAUTH_USER_PUBKEY_FIELD
                setattr(user, pubkey_field, form.cleaned_data[pubkey_field])
                user.save()
                login(request, user, 'scatterauth.backend.ScatterAuthBackend')
                return redirect(get_redirect_url(request))
    return render(request,
                  template_name,
                  {'form': form})
