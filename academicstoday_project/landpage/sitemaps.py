from django.contrib import sitemaps
from django.core.urlresolvers import reverse

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'
    
    def items(self):
        return ['landpage','robots','humans','google_plus_verify','terms','privacy',]
    
    def location(self, item):
        return reverse(item)

# https://docs.djangoproject.com/en/1.8/ref/contrib/sitemaps/