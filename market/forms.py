from django import forms
from core import forms as CoreForms

class CheckoutCartForm(forms.Form):
    cart_lines=forms.CharField(max_length=1000,required=True)
    customer_id=forms.IntegerField(required=True)

class AddOrderInWareHouseForm(forms.Form):
    direction=forms.CharField(max_length=20,required=True)
    order_id=forms.IntegerField(required=True)
    ware_house_id=forms.IntegerField(required=True)
    description=forms.CharField( max_length=100, required=False)

class DeleteProductCommentForm(forms.Form):
    comment_id=forms.IntegerField(required=True)

class AddProductSpecificationForm(forms.Form):
    product_id=forms.IntegerField(required=True)
    name=forms.CharField( max_length=200, required=True)
    value=forms.CharField( max_length=200, required=True)

class AddProductImageForm(forms.Form):
    product_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100,required=False)
    description=forms.CharField(max_length=100,required=False)

class AddProductCommentForm(forms.Form):
    product_id=forms.IntegerField(required=True)
    comment=forms.CharField( max_length=200, required=True)

class DeleteProductForm(forms.Form):
    product_id=forms.IntegerField(required=True)
    parent_id=forms.IntegerField(required=True)

class EditProductForm(forms.Form):
    name=forms.CharField( max_length=100, required=True)
    unit_name=forms.CharField( max_length=50, required=False)
    image=forms.ImageField(required=False,widget=forms.ClearableFileInput(attrs={'class':'btn btn-warning','v-model':'upload-profile','multiple': False}))
    
    short_description=forms.CharField(max_length=500, required=False)
    description=forms.CharField( max_length=5000, required=False)
    def __init__(self, *args, **kwargs):
        super(EditProductForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'accept': 'image/*'})
    
class AddToMyFavoritesForm(forms.Form):
    product_id=forms.IntegerField(required=False)

class RemoveFromMyFavoritesForm(forms.Form):
    product_id=forms.IntegerField(required=False)

class SearchForm(forms.Form):
    search_for=forms.CharField(max_length=50,required=True)

class RemoveShopForm(forms.Form):
    shop_id=forms.IntegerField(required=True)


class AddProductFeatureForm(forms.Form):
    product_id=forms.IntegerField(required=True)
    product_feature_id=forms.IntegerField(required=True)
    add_or_remove=forms.CharField(max_length=10, required=False)

class EditOrderLineForm(forms.Form):
    order_id=forms.IntegerField(required=True)
    product_id=forms.IntegerField(required=True)
    quantity=forms.IntegerField(required=True)
    unit_price=forms.IntegerField(required=True)
    unit_name=forms.CharField(max_length=50, required=False)
    description=forms.CharField(max_length=50, required=False)

class ConfirmCartForm(forms.Form):
    supplier_id=forms.IntegerField(required=False)
    customer_id=forms.IntegerField(required=False)
    address=forms.CharField( max_length=200, required=True)
    description=forms.CharField( max_length=200, required=False)
    no_ship=forms.BooleanField(required=False)

# class CheckoutForm(forms.Form):
#     address=forms.CharField( max_length=200, required=True)
#     description=forms.CharField( max_length=200, required=False)

class DoDeliverForm(forms.Form):
    order_id=forms.IntegerField(required=True)
    ware_house_id=forms.IntegerField(required=False)
    description=forms.CharField( max_length=100, required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'توضیحات'}))

class DoShipForm(forms.Form):
    order_id=forms.IntegerField(required=True)
    description=forms.CharField( max_length=100, required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'توضیحات'}))

class DoPackForm(forms.Form):
    ware_house_id=forms.IntegerField(required=True)
    order_id=forms.IntegerField(required=True)
    count_of_packs=forms.IntegerField( required=False,widget=forms.TextInput(attrs={'class':'form-control','type':'number','placeholder':'تعداد پاکت'}))
    description=forms.CharField(  max_length=100,required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'توضیحات'}))

class CancelOrderForm(forms.Form):
    order_id=forms.IntegerField(required=True)
    description=forms.CharField(max_length=100,required=False)

class ConfirmOrderForm(forms.Form):
    order_id=forms.IntegerField(required=True)    
    description=forms.CharField(max_length=100,required=False)

class DeleteAddressForm(forms.Form):
    address_id=forms.IntegerField(required=True)

class EditProfileForm(forms.Form):
    first_name=forms.CharField(max_length=50, required=True)
    last_name=forms.CharField(max_length=50, required=True)
    #mobile=forms.CharField(max_length=11, required=True)
    #email=forms.EmailField(required=False)
    bio=forms.CharField( max_length=200, required=False)
    region=forms.CharField(max_length=50, required=False)

class AddProductForCategoryPage(forms.Form):
    product_id=forms.IntegerField(required=True)
    category_id=forms.IntegerField(required=False)

class AddCustomerForm(forms.Form):
    profile_id=forms.IntegerField(required=True)

class AddCategoryForm(forms.Form):
    parent_id=forms.IntegerField(required=False)
    title=forms.CharField(max_length=50, required=True)

class AddProductForm(forms.Form):
    unit_name=forms.CharField(max_length=50, required=False)
    category_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100,required=True)
    specifications=forms.CharField( max_length=500, required=False)
    
class AddProductForShoeForm(forms.Form):
    category_id=forms.IntegerField(required=True)
    barcode=forms.CharField(max_length=50,required=True)
    title=forms.CharField(max_length=100,required=True)
    unit_name=forms.CharField(max_length=50, required=False)
    supplier_id=forms.IntegerField(required=True)
    availables=forms.CharField( max_length=500, required=False)
    unit_price=forms.IntegerField(required=False)
    buy_price=forms.IntegerField(required=False)
    
class AddProductForShopForm(forms.Form):
    unit_name=forms.CharField(max_length=50, required=False)
    supplier_id=forms.IntegerField(required=True)
    unit_price=forms.IntegerField(required=True)
    category_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100,required=True)
    specifications=forms.CharField( max_length=500, required=False)
    
class AddWareHouseForm(forms.Form):
    name=forms.CharField(max_length=100, required=True)
    address=forms.CharField(max_length=2000, required=False)

class AddShopForm(forms.Form):
    supplier_id=forms.IntegerField(required=True)
    product_id=forms.IntegerField( required=True)
    specifications=forms.CharField(max_length=2000, required=False)
    unit_name=forms.CharField(required=True)
    old_price=forms.CharField(required=False)
    buy_price=forms.CharField(required=False)
    level=forms.CharField(required=False)
    unit_price=forms.IntegerField(required=True)
    available=forms.IntegerField(required=False)
    
class SearchOrderForm(forms.Form):
    page=forms.IntegerField(required=False)
    supplier_id=forms.IntegerField(required=False)
    shipper_id=forms.IntegerField(required=False)
    customer_id=forms.IntegerField(required=False)
    start_date=forms.CharField(max_length=20,required=False)
    end_date=forms.CharField(max_length=20,required=False)
    status=forms.CharField(max_length=30,required=False)
    
class AddToCartForm(forms.Form):
    customer_id=forms.IntegerField(required=False)
    shop_id=forms.IntegerField(required=True)
    quantity=forms.IntegerField(required=False)

class RemoveFromCartForm(forms.Form):
    shop_id=forms.IntegerField(required=True)

class AddAddressForm(forms.Form):
    city=forms.CharField(max_length=50, required=True)
    street=forms.CharField(max_length=100, required=True)
    agent=forms.CharField(max_length=50, required=True)
    tel=forms.CharField(max_length=50, required=True)
    title=forms.CharField(max_length=50, required=True)

class AddProductLikeForm(forms.Form):
    product_id=forms.IntegerField(required=True)

class RegisterForm(forms.Form):
    region=forms.CharField(max_length=20,required=True)
    username=forms.CharField(max_length=50, required=True)
    password=forms.CharField(max_length=150, required=True)
    first_name=forms.CharField(max_length=50, required=True)
    last_name=forms.CharField(max_length=50, required=True)