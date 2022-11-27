from django.contrib import admin

from Eshop.models import MyUser, Product, Purchase, Return

admin.site.register(MyUser)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(Return)
