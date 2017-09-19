from django.contrib import sitemaps
from django.core.urlresolvers import reverse
# from foundation_public.models.organization import PublicOrganization


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['at_index_master',]

    def location(self, item):
        return reverse(item)
