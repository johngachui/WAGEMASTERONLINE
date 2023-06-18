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
from wagemaster_online.views import company_detail, company_list, company_create, company_update, company_delete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('company/', company_detail, name='company_detail'),
    path('company/list/', company_list, name='company_list'),
    path('company/create/', company_create, name='company_create'),
    path('company/update/<int:company_id>/', company_update, name='company_update'),
    path('company/delete/<int:company_id>/', company_delete, name='company_delete'),
]
