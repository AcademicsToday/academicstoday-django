from django.contrib import admin
from shared_foundation.models.profile import SharedProfile
from shared_foundation.models.university import SharedUniversity
from shared_foundation.models.university import SharedUniveristyDomain

# Register your models here.
admin.site.register(SharedProfile)
admin.site.register(SharedUniversity)
admin.site.register(SharedUniveristyDomain)
