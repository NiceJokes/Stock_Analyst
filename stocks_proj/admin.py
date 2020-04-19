from django.contrib import admin

# Register your models here.
from .models import API_keys,Items_table, Indicators


class ItemAdmin(admin.ModelAdmin):
    search_fields = ['category','dataset','symbol','description']
    list_filter = ('dataset','category')
    list_display = ('description','category','subcategory','country','dataset','symbol')


admin.site.register(API_keys)
admin.site.register(Items_table, ItemAdmin)
admin.site.register(Indicators)