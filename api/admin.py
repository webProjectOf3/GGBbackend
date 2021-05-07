from django.contrib import admin

from .models import ProductImage, Product, Category

admin.site.register(ProductImage)
admin.site.register(Product)
admin.site.register(Category)
