from django.contrib import admin
from .models import Review, Cart, Product, Category

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Cart)


