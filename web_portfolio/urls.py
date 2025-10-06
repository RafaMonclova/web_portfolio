"""
URL configuration for web_portfolio project.

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
from django.urls import path
from users.views import CustomLoginView, WebLoginView, web_logout
from rest_framework.routers import DefaultRouter
from users.views import UserView
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from core.views import home


router = DefaultRouter()
router.register(r'users', UserView)

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('apiweb/admin/', admin.site.urls),
    path('apiweb/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('apiweb/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('apiweb/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('apiweb/', include(router.urls)),

    path('apiweb/auth/login/', CustomLoginView.as_view(), name='login'),  # Login
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh

    path('', home, name='home'),
    path('blog/', include('blog.urls')),  # Incluir las URLs de la app blog
    path('login/', WebLoginView.as_view(), name='login'),
    path('logout/', web_logout, name='logout'),
    path('about/', include('about.urls')),
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
