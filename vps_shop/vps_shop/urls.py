"""
URL configuration for vps_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from servers.views import VpsViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView)



vpsRouter = routers.DefaultRouter()
vpsRouter.register(r'vps', VpsViewSet, basename='vps')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('servers.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/auth/', include('rest_framework.urls')), # /login and /logout
    path('api/v2/', include(vpsRouter.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #DRFSJWT
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), #DRFSJWT
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'), #DRFSJWT
    re_path('api/v2/auth', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    # path('api/v2/vpslist/', VpsViewSet.as_view({'get':'list', 'post': 'create'})),
    # path('api/v2/vpslist/<int:uid>', VpsViewSet.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'}))
]
