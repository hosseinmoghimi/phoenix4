from django.contrib import admin
from .models import ProductSpecification,Blog, Brand, Cart, CartLine, Customer, Employee, Guarantee, Offer, Order, OrderInWareHouse, OrderLine, Product,Category, ProductFeature, ProductInStock, Shipper, Shop, ShopRegion, Supplier, UnitName, WareHouse

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(UnitName)
admin.site.register(Customer)
admin.site.register(Blog)
admin.site.register(Offer)
admin.site.register(Supplier)
admin.site.register(Shipper)
admin.site.register(CartLine)
admin.site.register(Order)
admin.site.register(OrderLine)
admin.site.register(Shop)
admin.site.register(ShopRegion)

admin.site.register(ProductSpecification)

admin.site.register(Guarantee)
admin.site.register(ProductFeature)
admin.site.register(ProductInStock)
admin.site.register(Brand)
admin.site.register(WareHouse)
admin.site.register(Employee)
admin.site.register(OrderInWareHouse)
admin.site.register(Cart)
