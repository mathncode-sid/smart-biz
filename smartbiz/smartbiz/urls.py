"""
URL configuration for smartbiz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from core import views as core_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", core_views.landing_page, name="landing"),

    path("login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", core_views.register, name="register"),
    path("onboarding/", core_views.onboarding, name="onboarding"),

    path("dashboard/", core_views.dashboard, name="dashboard"),
    path("products/", core_views.product_list, name="product_list"),
    path("products/new/", core_views.product_create, name="product_create"),
    path("products/<int:product_id>/edit/", core_views.product_edit, name="product_edit"),
    path("products/<int:product_id>/delete/", core_views.product_delete, name="product_delete"),
    path("products/<int:product_id>/sale/", core_views.record_sale, name="record_sale"),
    path("sales/history/", core_views.sales_history, name="sales_history"),

    path("subscription/required/", core_views.subscription_required_view, name="subscription_required"),
    path("subscription/expired/", core_views.subscription_expired_view, name="subscription_expired"),
    path("subscription/plans/", core_views.subscription_plans, name="subscription_plans"),
    path("subscription/plans/<int:plan_id>/renew/", core_views.renew_subscription, name="renew_subscription"),
    path("subscription/status/", core_views.subscription_status, name="subscription_status"),

    # Admin Routes
    path("admin-dashboard/", core_views.admin_dashboard, name="admin_dashboard"),
    path("admin-users/", core_views.admin_users, name="admin_users"),
    path("admin-subscriptions/", core_views.admin_subscriptions, name="admin_subscriptions"),
    path("admin-users/<int:user_id>/toggle/", core_views.toggle_user_status, name="toggle_user_status"),
    path("admin-subscriptions/<int:subscription_id>/toggle/", core_views.toggle_subscription_status, name="toggle_subscription_status"),
]

