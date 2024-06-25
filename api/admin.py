from django.contrib import admin
from .models import Organization, User, Individual, Tag, Partner, Resource, Event

# Register your models here.
admin.site.register(Organization)
admin.site.register(User)
admin.site.register(Individual)
admin.site.register(Tag)
admin.site.register(Partner)
admin.site.register(Resource)
admin.site.register(Event)