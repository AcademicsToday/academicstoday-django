from django.conf.urls import patterns, include, url
from django.conf.urls.static import static, settings
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'academicstoday_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    # This regex makes the default URL for the website to launch this view.
    url(r'', include('landpage.urls')),
    url(r'', include('account.urls')),
    url(r'', include('registrar.urls')),
    url(r'', include('student.urls')),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
