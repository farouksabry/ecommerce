from django.contrib import admin
from .models import Merchant, Store

class MerchantAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')

class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner')

admin.site.register(Merchant, MerchantAdmin)
admin.site.register(Store, StoreAdmin)
