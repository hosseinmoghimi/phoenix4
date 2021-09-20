from market import apis
from .apps import APP_NAME
from . import views,apis
from django.urls import path,include
app_name=APP_NAME
urlpatterns = [
    path("",views.BasicViews().home,name="home"),
    path("product/<int:pk>/",views.ProductViews().product,name="product"),
    path("category/<int:pk>/",views.CategoryViews().category,name="category"),
    path("blog/<int:pk>/",views.BlogViews().blog,name="blog"),
    path("offer/<int:pk>/",views.OfferViews().offer,name="offer"),
    path("order_invoice/<int:pk>/",views.OrderViews().order_invoice,name="order_invoice"),
    path("order/<int:pk>/",views.OrderViews().order,name="order"),
    path("orders/<int:customer_id>/<int:supplier_id>/<int:shipper_id>",views.OrderViews().orders,name="orders"),
    path("customer/<int:pk>/",views.CustomerViews().customer,name="customer"),
    path("supplier/<int:pk>/",views.SupplierViews().supplier,name="supplier"),
    path("shipper/<int:pk>/",views.ShipperViews().shipper,name="shipper"),
    path("brand/<int:pk>/",views.ProductViews().brand,name="brand"),
    path("guarantee/<int:pk>/",views.GuaranteeView().guarantee,name="guarantee"),
    path("cart/",views.CartViews().cart,name="cart"),
    path('do_pack_order/',views.OrderViews().do_pack_order,name='do_pack_order'),
    path('do_deliver_order/',views.OrderViews().do_deliver_order,name='do_deliver_order'),
    path('add_product/<int:category_id>/',views.ProductViews().add_product,name='add_product_view'),
    path('do_cancel_order/',views.OrderViews().do_cancel_order,name='do_cancel_order'),
    path('do_ship_order/',views.OrderViews().do_ship_order,name='do_ship_order'),
    path("confirm_cart/",views.CartViews().confirm,name="confirm_cart"),
    path("cart/<int:customer_id>/",views.CartViews().cart,name="customer_cart"),
    path("shop/<int:pk>/",views.ShopViews().shop,name="shop"),
    path("employee/<int:pk>/",views.EmployeeViews().employee,name="employee"),
    path("ware_house/<int:pk>/",views.WareHouseViews().ware_house,name="ware_house"),
    path("ware_houses/",views.WareHouseViews().ware_houses,name="ware_houses"),

    path("api/products/<int:category_id>/",apis.ProductApi().products,name="products"),
    path("api/add_product/",apis.ProductApi().add_product,name="add_product"),
    path("api/add_product_for_shop/",apis.ProductApi().add_product_for_shop,name="add_product_for_shop"),
    path("api/add_product_specification/",apis.ProductApi().add_product_specification,name="add_product_specification"),
    path("api/add_category/",apis.CategoryApi().add_category,name="add_category"),
    path("api/add_shop/",apis.ShopApi().add_shop,name="add_shop"),
    path("api/add_to_cart/",apis.CartApi().add_to_cart,name="add_to_cart"),
    path("api/checkout_cart/",apis.CartApi().checkout_cart,name="checkout_cart"),
    path("api/add_warehouse/",apis.WareHouseApi().add_warehouse,name="add_warehouse"),
    
]
