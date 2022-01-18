from market.repo import GuaranteeRepo
from .models import Brand, Cart, CartLine, Category, Customer, Guarantee, Menu, Order, OrderLine, Product, ProductFeature, ProductSpecification, Shop, Supplier, UnitName, WareHouse
from rest_framework import serializers
from authentication.serializers import ProfileSerializer

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'thumbnail', 'get_absolute_url','barcode']

class UnitNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitName
        fields = ['id', 'name']

class CustomerSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model = Customer
        fields = ['id', 'profile','title', 'get_absolute_url']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title','parent_id', 'get_absolute_url', 'thumbnail']


class SupplierSerializerForShop(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'title','get_absolute_url','region','image']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'title','get_absolute_url','get_logo_link']


class ProductSerializerForShop(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title','barcode','get_absolute_url','thumbnail']


class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ['id','name','value','get_edit_url']

class ShopSerializer(serializers.ModelSerializer):
    supplier=SupplierSerializerForShop()
    product=ProductSerializerForShop()
    specifications=ProductSpecificationSerializer(many=True)
    class Meta:
        model = Shop
        fields = ['id','specifications', 'supplier','level','product', 'unit_name', 'available', 'unit_price','get_edit_url']

class CartLineSerializer(serializers.ModelSerializer):
    shop=ShopSerializer()
    class Meta:
        model = CartLine
        fields = ['id','quantity','shop','line_total']

class GuaranteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guarantee
        fields = ['id','barcode','serial_no','get_absolute_url','get_print_url','get_qrcode_url','persian_start_date','persian_end_date','get_edit_url']

class OrderLineSerializer(serializers.ModelSerializer):
    product=ProductSerializer()
    guarantees=GuaranteeSerializer(many=True)
    class Meta:
        model = OrderLine
        fields = ['id','quantity','unit_name','unit_price','product','guarantees','description','get_absolute_url']

class OrderSerializer(serializers.ModelSerializer):
    customer=CustomerSerializer()
    supplier=SupplierSerializerForShop()
    lines=OrderLineSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id','lines','customer','supplier','sum_total','lines_total','total','get_absolute_url']
class CartSerializer(serializers.ModelSerializer):
    orders=OrderSerializer(many=True)
    lines=CartLineSerializer(many=True)
    class Meta:
        model = Cart
        fields = ['id','customer','orders','lines']
class WareHouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = WareHouse
        fields = ['id','name','address','get_absolute_url']
class ProductFeatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductFeature
        fields = ['id','title','short_description','get_absolute_url']

class MenuSerializer(serializers.ModelSerializer):
    shops=ShopSerializer(many=True)
    class Meta:
        model = Menu
        fields = ['id','shops','title', 'get_absolute_url']



class MenuLineSerializer(serializers.ModelSerializer):
    shops=ShopSerializer(many=True)
    class Meta:
        model = Menu
        fields = ['id','shops','title', 'get_absolute_url']


