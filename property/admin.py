from django.contrib import admin

from property.models import *

admin.site.register(Property)
admin.site.register(Client)
admin.site.register(Payment)
admin.site.register(Receipt)