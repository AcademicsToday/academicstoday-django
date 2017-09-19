"""academicstoday URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from academicstoday.sitemaps import StaticViewSitemap


sitemaps = {
    'static': StaticViewSitemap,
}


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url('^', include('django.contrib.auth.urls')),
    url(r'^', include('shared_api.urls')),

     # Sitemap
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # Django-RQ
    url(r'^django-rq/', include('django_rq.urls')),
]


urlpatterns += i18n_patterns(
    url(r'^', include('shared_api.urls')),
    url(r'^', include('shared_authentication.urls')),
    url(r'^', include('shared_dashboard.urls')),
    url(r'^', include('shared_foundation.urls')),
    url(r'^', include('shared_index.urls')),
    url(r'^', include('shared_university.urls')),
)


# Custom errors.
# handler403 = "public_home.views.http_403_page"
# handler404 = "public_home.views.http_404_page"
# handler500 = "public_home.views.http_500_page"
