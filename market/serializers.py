from market.repo import GuaranteeRepo
from .models import Cart, CartLine, Category, Customer, Guarantee, Order, OrderLine, Product, Shop, Supplier
from rest_framework import serializers
from authentication.serializers import ProfileSerializer

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'thumbnail', 'get_absolute_url']


class CustomerSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model = Customer
        fields = ['id', 'profile','title', 'get_absolute_url']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'get_absolute_url', 'thumbnail']


class SupplierSerializerForShop(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'title','get_absolute_url']


class ProductSerializerForShop(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title','get_absolute_url','thumbnail']


class ShopSerializer(serializers.ModelSerializer):
    supplier=SupplierSerializerForShop()
    product=ProductSerializerForShop()
    class Meta:
        model = Shop
        fields = ['id', 'supplier','level','product', 'unit_name', 'available', 'unit_price']

class CartLineSerializer(serializers.ModelSerializer):
    shop=ShopSerializer()
    class Meta:
        model = CartLine
        fields = ['id','quantity','shop','line_total']

class GuaranteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guarantee
        fields = ['id','barcode','serial_no','get_qrcode_url','persian_start_date','persian_end_date']

class OrderLineSerializer(serializers.ModelSerializer):
    product=ProductSerializer()
    guarantees=GuaranteeSerializer(many=True)
    class Meta:
        model = OrderLine
        fields = ['id','quantity','unit_name','unit_price','product','guarantees']

        
class OrderSerializer(serializers.ModelSerializer):
    customer=CustomerSerializer()
    supplier=SupplierSerializerForShop()
    lines=OrderLineSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id','lines','customer','supplier','sum_total','lines_total','total']
class CartSerializer(serializers.ModelSerializer):
    orders=OrderSerializer(many=True)
    lines=CartLineSerializer(many=True)
    class Meta:
        model = Cart
        fields = ['id','customer','orders','lines']