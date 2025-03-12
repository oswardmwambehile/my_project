from django.contrib import admin
from.models import Product,Customer ,Cart,Payment, Order

class ProductAdmin(admin.ModelAdmin):
    list_display=('id','title','selling_price','discount_price','category')
admin.site.register(Product, ProductAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display=('id','user','name','locality','city','country','zipcode','mobile')
admin.site.register(Customer, CustomerAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display=('id','user','product','quantity')
admin.site.register(Cart, CartAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display=('id','user','amount','paid')
admin.site.register(Payment, PaymentAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display=('id','user','customer','product','quantity','order_date','status','payment')
admin.site.register(Order, OrderAdmin)

