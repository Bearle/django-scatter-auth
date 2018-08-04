from django.conf.urls import url

from web3auth import views

urlpatterns = [
    url(r'^login_api/$', views.login_api, name='web3auth_login_api'),
    url(r'^signup_api/$', views.signup_api, name='web3auth_signup_api'),
    url(r'^signup/$', views.signup_view, name='web3auth_signup'),
]
