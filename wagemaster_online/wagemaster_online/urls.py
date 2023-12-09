"""
URL configuration for wagemaster_online project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from wagemaster_online.views import company_detail, company_list, company_create, company_update, company_delete,create_client
from wagemaster_online.views import UserLoginView, register, home,administrator_dashboard, client_dashboard,client_list
from wagemaster_online.views import dashboard, fetch_companies,subscription_create,fetch_subscriptions
from wagemaster_online.views import client_update,check_username_availability,subscription_update,set_new_password
from django.contrib.auth import views as auth_views
from .views import ClientDeleteView,CompanyDeleteView,SubscriptionDeleteView

urlpatterns = [
    path('', home, name='home'),

    path('registration/', register, name='register'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('login/', UserLoginView.as_view(), name='login'),

    path('set_new_password/', set_new_password, name='set_new_password'),
  
    path('admin/dashboard/', administrator_dashboard, name='administrator_dashboard'),
    path('fetch_companies/', fetch_companies, name='fetch_companies'),
    path('fetch_subscriptions/', fetch_subscriptions, name='fetch_subscriptions'),
    #path('admin/dashboard/', dashboard, name='dashboard'),
    path('create-client/', create_client, name='create_client'),
    path('client/update/', client_update, name='client_update'),  
    path('check_username_availability/', check_username_availability, name='check_username_availability'),
    path('client-list/', client_list, name='client_list'),
    path('client/dashboard/', client_dashboard, name='client_dashboard'),

    path('client_delete/', ClientDeleteView.as_view(), name='client_delete'),
    path('company_delete/', CompanyDeleteView.as_view(), name='company_delete'),
    path('subscription_delete/', SubscriptionDeleteView.as_view(), name='subscription_delete'),

    path('company/list/', company_list, name='company_list'),
    path('company/create/', company_create, name='company_create'),
    path('company_update/', company_update, name='company_update'),
    path('subscription_update/', subscription_update, name='subscription_update'),
    path('subscription/create/', subscription_create, name='subscription_create'),
    path('admin/', admin.site.urls),
]
