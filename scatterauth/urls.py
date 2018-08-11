from django.conf.urls import url

from scatterauth import views

urlpatterns = [
    url(r'^login_api/$', views.login_api, name='scatterauth_login_api'),
    url(r'^signup_api/$', views.signup_api, name='scatterauth_signup_api'),
    url(r'^signup/$', views.signup_view, name='scatterauth_signup'),
]
