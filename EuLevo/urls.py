"""EuLevo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

from core.views import ProfileViewSet, SocialLoginView, RegisterView, UserPointViewSet
from eulevo.views import PackageViewSet, PackageImageViewSet, TravelViewSet, DealViewSet, DoneDealViewSet


router = routers.DefaultRouter()
router.register('user-points', UserPointViewSet)
router.register('profiles', ProfileViewSet)
router.register('packages', PackageViewSet)
router.register('package-images', PackageImageViewSet)
router.register('travels', TravelViewSet)
router.register('deals', DealViewSet)
router.register('done-deals', DoneDealViewSet)

from .site import site as el_site

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^el_admin/', el_site.urls),
    url(r'^api-register/', RegisterView.as_view()),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', SocialLoginView.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

