"""
URL configuration for clubmanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from two_factor.admin import AdminSiteOTPRequired
from two_factor.urls import urlpatterns as two_factor_urls
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from api.api import api

# admin.site.__class__ = AdminSiteOTPRequired

urlpatterns = [
    path("", include(two_factor_urls)),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("accounts/profile/", RedirectView.as_view(pattern_name="clubmanager:index"), name="profile"),
    path("api/", api.urls),
    path("clubmanager/admin/", include("clubmanager.clubmanager_admin_urls")),
    path("clubmanager/", include("clubmanager.clubmanager_urls")),
    path("initials-avatar/", include("django_initials_avatar.urls")),
    path("markdownx/", include("markdownx.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns = urlpatterns + debug_toolbar_urls()
