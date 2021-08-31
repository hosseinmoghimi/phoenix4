from django.contrib import admin
from .models import CartLine, Customer, Order, OrderLine, Product,Category, Shipper, Shop, Supplier, UnitName

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(UnitName)
admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Shipper)
admin.site.register(CartLine)
admin.site.register(Order)
admin.site.register(OrderLine)
admin.site.register(Shop)
