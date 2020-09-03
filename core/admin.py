from django.contrib import admin
from core.models import Product

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'price']
    list_display = ['name', 'price', 'store']
    list_filter = ['price']
    list_per_page = 200


admin.site.register(Product, ProductAdmin)