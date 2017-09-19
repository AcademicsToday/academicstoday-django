from django.contrib import admin
from shared_foundation.models.university import SharedUniversity
from shared_foundation.models.university import SharedUniveristyDomain
from shared_foundation.models.universityregistration import SharedUniversityRegistration

# Register your models here.
admin.site.register(SharedUniversity)
admin.site.register(SharedUniveristyDomain)
admin.site.register(SharedUniversityRegistration)
