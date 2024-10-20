from django.contrib import admin

# Register your models here.

from .models import PhoneNumber, Address, Profile

admin.site.register(PhoneNumber)
admin.site.register(Profile)
admin.site.register(Address)
