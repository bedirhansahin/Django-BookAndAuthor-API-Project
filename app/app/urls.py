from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from user.api import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/user/', include('user.api.urls'), name='user'),
    path('api-auth/', include('rest_framework.urls')),  # Adds login button to 'rest framework' screen
    path('api/schema', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/docs', SpectacularSwaggerView.as_view(url_name='schema')),
]
