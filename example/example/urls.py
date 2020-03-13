"""example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.shortcuts import render, redirect
from django.views.generic import RedirectView, TemplateView


def auto_login(request):
    from django.conf import settings
    if not request.user.is_authenticated:
        return render(request, 'scatterauth/autologin.html', context={'settings': settings})
    else:
        return redirect('/')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='scatterauth/home.html')),
    url(r'^auto_login/', auto_login, name='autologin'),
    url(r'', include('scatterauth.urls')),
    url(r'django_auth/', include('django.contrib.auth.urls')),

]
