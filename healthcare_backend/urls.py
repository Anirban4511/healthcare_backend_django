from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Auth endpoints (register and login will be defined in core app)
    # path('api/auth/', include('core.urls')),
    # JWT endpoints (login/token/refresh)
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Patient, Doctor, and Mapping endpoints will be included from core app
    path('api/', include('core.urls')),
]
