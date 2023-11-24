from __future__ import annotations

from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import LoginViewSet
from .views import MeViewSet
from .views import RegisterViewSet, CountryTableView  # Correct the import here

router = DefaultRouter(trailing_slash=False)

router.register(r'register', RegisterViewSet, basename='register')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'me', MeViewSet, basename='me')
# router.register(r'country_table', CountryTableView.as_view(), basename='country_table')

urlpatterns = [
    path(r'country_table', CountryTableView.as_view(), name='country_table'),
    path(r'', include(router.urls)),
]