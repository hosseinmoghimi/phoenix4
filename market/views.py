from core.constants import CURRENCY
from utility.persian2 import PersianCalendar
from django.http.response import Http404
from market.serializers import CartLineSerializer, CartSerializer, OrderLineSerializer, ProductSpecificationSerializer, ShopSerializer
import json
from .enums import OrderStatusEnum, ParameterEnum, PictureEnum, ShopLevelEnum
from core.repo import NavLinkRepo, ParameterRepo, PictureRepo
from core.views import CoreContext, MessageView, PageContext
from django.views import View
from market.forms import *
from .repo import BlogRepo, EmployeeRepo, FinancialReportRepo, ProductFeatureRepo, ShipperRepo, BrandRepo, CartRepo, CategoryRepo, CustomerRepo, GuaranteeRepo, OfferRepo, OrderRepo, ProductRepo, ShopRepo, SupplierRepo, WareHouseRepo
from .apps import APP_NAME
from authentication.views import ProfileContext
from django.shortcuts import render, redirect, reverse
TEMPLATE_ROOT = "market/"
LAYOUT_PARENT = "Adminlte/layout.html"
LAYOUT_PARENT = "Adminlte/layout.html"
LAYOUT_PARENT = "phoenix/layout.html"
LAYOUT_PARENT = "material-kit-pro/layout.html"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    context['title'] = "Market"
    context['market_title']=ParameterRepo(request=request,app_name=APP_NAME).parameter(name=ParameterEnum.SHOP_HEADER_TITLE)
    context['market_link']=ParameterRepo(request=request,app_name=APP_NAME).parameter(name=ParameterEnum.SHOP_HEADER_LINK)
    context['me_supplier'] = SupplierRepo(request=request).me
    me_customer=CustomerRepo(request=request).me
    context['me_customer'] = me_customer
    vertical_navs=NavLinkRepo(request=request,app_name=APP_NAME).list()
    context['vertical_navs']=vertical_navs
    if me_customer is not None:
        context['profile_button']={
            'url':me_customer.get_absolute_url(),
            'title':me_customer.title,
            'icon':"shopping_cart",
            'color':"primary",
        }
    
    context['ware_houses'] = WareHouseRepo(request=request).list()
    context['suppliers'] = SupplierRepo(request=request).list()
    context['brands'] = BrandRepo(request=request).list()
    context['navbar'] = APP_NAME+"/includes/nav-bar.html"
    context['layout_parent'] = LAYOUT_PARENT
    context['root_categories'] = CategoryRepo(
        request=request).list(for_home=True)
    context['search_form']=SearchForm()
    return context
# Create your views here.


class BasicViews(View):
    def home(self, request, *args, **kwargs):
        context = getContext(request)
        context['body_class'] = "ecommerce-page"
        parameter_repo = ParameterRepo(request=request, app_name=APP_NAME)
        context['shop_header_title'] = parameter_repo.parameter(
            name=ParameterEnum.SHOP_HEADER_TITLE)
        context['shop_header_slogan'] = parameter_repo.parameter(
            name=ParameterEnum.SHOP_HEADER_SLOGAN)
        context['shop_header_image'] = PictureRepo(
            request=request, app_name=APP_NAME).picture(name=ParameterEnum.SHOP_HEADER_IMAGE)
        categories = CategoryRepo(request=request).list(for_home=True)
        context['categories'] = categories
        context['offers'] = OfferRepo(request=request).list(for_home=True)
        context['blogs'] = BlogRepo(request=request).list(for_home=True)
        products = ProductRepo(request=request).list(for_home=True)
        context['products'] = products
        context['top_products'] = products.order_by('-priority')[:3]
        if request.user.has_perm(APP_NAME+".add_product") and len(categories) == 0:
            context['add_product_form'] = AddProductForm()
        if request.user.has_perm(APP_NAME+".add_category") and len(products) == 0:
            context['add_category_form'] = AddCategoryForm()
        return render(request, TEMPLATE_ROOT+"index.html", context)

    def search(self, request, *args, **kwargs):
        context = getContext(request)
        log = 1
        if request.method == 'POST':
            log += 1
            search_form = SearchForm(request.POST)
            if search_form.is_valid():
                log += 1
                search_for = search_form.cleaned_data['search_for']
                context['search_for'] = search_for
                context['products'] = ProductRepo(
                    request=request).list(search_for=search_for)
                context['categories'] = CategoryRepo(
                    request=request).list(search_for=search_for)
                context['customers'] = CustomerRepo(
                    request=request).list(search_for=search_for)
                context['suppliers'] = SupplierRepo(
                    request=request).list(search_for=search_for)
                context['shippers'] = ShipperRepo(
                    request=request).list(search_for=search_for)
                
                context['log'] = log
                context['header_image'] = PictureRepo(request=request, app_name=APP_NAME).picture(name=PictureEnum.SEARCH_HEADER)
        
                return render(request, TEMPLATE_ROOT+"search.html", context)
        return BasicViews().home(request=request)
 

class ShopViews(View):
    def shop(self, request, *args, **kwargs):
        shop=ShopRepo(request=request).shop(*args, **kwargs)
        return redirect(shop.product.get_absolute_url())

    def shops(self, request, *args, **kwargs):
        supplier=SupplierRepo(request=request).supplier(*args, **kwargs)
        if supplier is None:
            raise Http404
        context=getContext(request=request)

        context['body_class'] = "product-page"
        
        shops=ShopRepo(request=request).list(supplier=supplier)
        context['shops']=shops
        context['supplier']=supplier
        return render(request,TEMPLATE_ROOT+"shops.html",context)


class EmployeeViews(View):
    def employee(self, request, *args, **kwargs):
        
        context = getContext(request)
        employee=EmployeeRepo(request=request).employee(*args, **kwargs)
        context['employee']=employee
        context['body_class'] = "product-page"
        return render(request, TEMPLATE_ROOT+"employee.html", context)


class WareHouseViews(View):
    def ware_house(self, request, *args, **kwargs):
        
        context = getContext(request)
        ware_house=WareHouseRepo(request=request).ware_house(*args, **kwargs)
        context['ware_house']=ware_house
        context['body_class'] = "product-page"
        return render(request, TEMPLATE_ROOT+"ware-house.html", context)

    def ware_houses(self, request, *args, **kwargs):
        
        context = getContext(request)
        ware_houses=WareHouseRepo(request=request).list(*args, **kwargs)
        context['ware_houses']=ware_houses
        context['body_class'] = "product-page"
        if request.user.has_perm(APP_NAME+".add_warehouse"):
            context['add_ware_house_form']=AddWareHouseForm()
        return render(request, TEMPLATE_ROOT+"ware-houses.html", context)


class CartViews(View):
    def create_cart(self,request,*args, **kwargs):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+"create-cart.html",context)
    def cart(self, request, *args, **kwargs):
        if 'customer_id' in kwargs:
            customer_id = kwargs['customer_id']
            customer = CustomerRepo(request=request).customer(
                customer_id=kwargs['customer_id'])
        else:
            customer = CustomerRepo(request=request).me
        if customer is None:
            raise Http404
        context = getContext(request)
        cart_repo=CartRepo(request=request)
        cart = cart_repo.cart(customer=customer)
        context['cart'] = cart
        context['profit']=cart_repo.get_cart_profit(customer=customer)
        context['is_empty'] = len(cart.lines) == 0
        context['cart_lines_s'] = json.dumps(
            CartLineSerializer(cart.lines, many=True).data)
        context['customer'] = customer
        context['header_image'] = PictureRepo(
            request=request, app_name=APP_NAME).picture(name=PictureEnum.CART_HEADER)
        context['body_class'] = "shopping-cart"
        if request.user.has_perm(APP_NAME+".add_product"):
            context['add_product_form'] = AddProductForm()
        return render(request, TEMPLATE_ROOT+"cart.html", context)

    def confirm(self, request):
        if request.method == 'POST':
            confirm_cart_form = ConfirmCartForm(request.POST)
            if confirm_cart_form.is_valid():
                customer_id = confirm_cart_form.cleaned_data['customer_id']
                no_ship = confirm_cart_form.cleaned_data['no_ship']
                supplier_id = confirm_cart_form.cleaned_data['supplier_id']
                address = confirm_cart_form.cleaned_data['address']
                description = confirm_cart_form.cleaned_data['description']
                no_ship = confirm_cart_form.cleaned_data['no_ship']
                orders = CartRepo(request=request).confirm(
                    no_ship=no_ship,
                    customer_id=customer_id,
                    address=address,
                    description=description,
                    supplier_id=supplier_id
                    )
                if orders is not None and len(orders) == 1:
                    return redirect(orders[0].get_absolute_url())


class ProductViews(View):
    def product_sold(self,request,*args, **kwargs):

        product = ProductRepo(request=request).product(*args, **kwargs)
        page = product
        context = getContext(request=request)
        context.update(PageContext(request=request, page=page))
        if request.user.has_perm(APP_NAME+".add_productspecification"):
            context['add_product_specification_form']=AddProductSpecificationForm()
        context['product'] = product
        if request.user.has_perm(APP_NAME+".view_orderline"):
            order_lines=product.orderline_set.all().order_by("order__date_ordered")
            context['order_lines'] = order_lines
        context['body_class'] = "product-page"
        return render(request, TEMPLATE_ROOT+"product-sold.html.html", context)
    def add_product_for_category_page(self,request,*args, **kwargs):

        log=1
        if request.method=='POST':
            log=2
            add_product_for_category_page_form=AddProductForCategoryPage(request.POST)
            if add_product_for_category_page_form.is_valid():
                log=3
                category_id=add_product_for_category_page_form.cleaned_data['category_id']
                product_id=add_product_for_category_page_form.cleaned_data['product_id']
                category=ProductRepo(request=request).add_product_for_category_page(
                    product_id=product_id,
                    category_id=category_id)
                if category is not None:
                    return redirect(category.get_absolute_url())
       
        raise Http404

    def product_feature(self, request, *args, **kwargs):

        product_feature = ProductFeatureRepo(request=request).product_feature(*args, **kwargs)
        page = product_feature
        context = getContext(request)
        context.update(PageContext(request=request, page=product_feature))
        context['body_class'] = "product-page"
        context['product_feature']=product_feature
        return render(request, TEMPLATE_ROOT+"product-feature.html", context)

    def product(self, request, *args, **kwargs):

        product = ProductRepo(request=request).product(*args, **kwargs)
        page = product
        context = getContext(request=request)
        context.update(PageContext(request=request, page=page))
        if request.user.has_perm(APP_NAME+".add_productspecification"):
            context['add_product_specification_form']=AddProductSpecificationForm()
        context['product'] = product
        if request.user.has_perm(APP_NAME+".view_orderline"):
            order_lines=product.orderline_set.all().order_by("-order__date_ordered")
            context['order_lines'] = order_lines
        vertical_navs=[]
        vertical_navs.append({'url':"#product-main",'title':'مشخصات محصول','priority':1})
        vertical_navs.append({'url':"#product-features",'title':'خدمات برای این محصول','priority':2})
        vertical_navs.append({'url':"#related-products-div",'title':'محصولات مشابه','priority':3})
        vertical_navs.append({'url':"#product-orders",'title':'سفارشات این محصول','priority':4})
        context['vertical_navs']=vertical_navs
        context['related_products']=product.related_products()
        context['level']=ShopLevelEnum.REGULAR
        context['shop_levels'] = (i[0] for i in ShopLevelEnum.choices)
        if context['me_supplier'] is not None:
            context['supplier_shops'] = ShopRepo(request=request).list(
                product=product).order_by('unit_name', 'unit_price')
            context['add_shop_form']=AddShopForm()
        if context['me_customer'] is not None:
            
            context['in_cart']="ناموجود در سبد خرید شما"
            me_customer=context['me_customer']
            shops = ShopRepo(request=request).list(
                product=product, region=me_customer.region, level=me_customer.level)
            context['shops'] = shops
            context['shops_s'] = json.dumps(
                ShopSerializer(shops, many=True).data)
            cart=CartRepo(request=request).cart(customer_id=me_customer.id)
            context['cart']=cart
            line=cart.lines.filter(shop__product=product).first()
            if line is not None:
                in_cart=str(int(line.quantity))+" "+str(line.shop.unit_name)+" در سبد خرید "
                context['in_cart']=in_cart

            context['cart_s']=json.dumps(CartSerializer(cart).data)
        context['specifications_s']=json.dumps(ProductSpecificationSerializer(product.specifications(),many=True).data)
        if request.user.has_perm(APP_NAME+".change_product"):
            context['add_product_feature_form']=AddProductFeatureForm()
        context['body_class'] = "product-page"
        return render(request, TEMPLATE_ROOT+"product.html", context)

    def brand(self, request, *args, **kwargs):

        brand = BrandRepo(request=request).brand(*args, **kwargs)
        page = brand
        context = getContext(request)
        context['brand'] = brand

        context['products'] = brand.product_set.all()
        return render(request, TEMPLATE_ROOT+"brand.html", context)

    def brands(self, request, *args, **kwargs):

        brands = BrandRepo(request=request).list(*args, **kwargs)
        context = getContext(request)
        context['brands'] = brands
        context['image_header']=PictureRepo(request=request).picture(name=PictureEnum.BRANDS_IMAGE_HEADER)
        context['brands_slogan']=ParameterRepo(request=request).parameter(name=ParameterEnum.BRANDS_SLOGAN)
        return render(request, TEMPLATE_ROOT+"brands.html", context)

    def add_product(self,request,*args, **kwargs):
        context=getContext(request=request)
        category=CategoryRepo(request=request).category(*args, **kwargs)
        context['category']=category
        
        context['body_class'] = "product-page"
        return render(request,TEMPLATE_ROOT+"add-product.html",context)
    
    def add_product_for_shoe(self,request,*args, **kwargs):
        context=getContext(request=request)
        category=CategoryRepo(request=request).category(*args, **kwargs)
        context['category']=category
        
        
        context['body_class'] = "product-page"
        return render(request,TEMPLATE_ROOT+"add-product-for-shoe.html",context)


class CustomerViews(View):
    def customer(self, request, *args, **kwargs):

        customer = CustomerRepo(request=request).customer(*args, **kwargs)
        profile = customer.profile
        context = getContext(request)
        context.update(ProfileContext(request=request, profile=profile))
        context['customer'] = customer
        context['orders'] = OrderRepo(request=request).list(customer_id=customer.id)
        context['products'] = customer.favorites.all()

        context['body_class'] = "shopping-cart"
        return render(request, TEMPLATE_ROOT+"customer.html", context)


class GuaranteeView(View):
    def guarantee_qrcode(self, request, *args, **kwargs):
        context = getContext(request)
        guarantee = GuaranteeRepo(request=request).guarantee(*args, **kwargs)
        return guarantee.get_qrcode_response(context=context)

    def guarantee(self, request, *args, **kwargs):
        context = getContext(request)
        context['header_image'] = PictureRepo(
            request=request, app_name=APP_NAME).picture(name=PictureEnum.GUARANTEE_HEADER)
        guarantee = GuaranteeRepo(request=request).guarantee(*args, **kwargs)
        context['guarantee'] = guarantee
        return render(request, TEMPLATE_ROOT+'guarantee.html', context)


class SupplierViews(View):
    def supplier(self, request, *args, **kwargs):

        supplier = SupplierRepo(request=request).supplier(*args, **kwargs)
        page = supplier
        context = getContext(request)
        context.update(PageContext(request=request, page=page))
        context['supplier'] = supplier
        context['body_class'] = "product-page"
        context['orders'] = OrderRepo(request=request).list(supplier_id=supplier.id)
        return render(request, TEMPLATE_ROOT+"supplier.html", context)


class ShipperViews(View):
    def shipper(self, request, *args, **kwargs):
        shipper = SupplierRepo(request=request).shipper(*args, **kwargs)
        page = shipper
        context = getContext(request)
        context.update(PageContext(request=request, page=page))
        context['shipper'] = shipper
        context['body_class'] = "product-page"
        return render(request, TEMPLATE_ROOT+"shipper.html", context)


class OrderViews(View):
    def financial_report(self,request,*args, **kwargs):
        context = getContext(request)
        financial_report=FinancialReportRepo(request=request).financial_report(*args, **kwargs)
        context['financial_report']=financial_report
        context['order']=financial_report.order
        return render(request, TEMPLATE_ROOT+"financial-report.html", context)

    def order(self, request, *args, **kwargs):
        user = request.user
        order = OrderRepo(request=request).order(*args, **kwargs)
        if order is None:
            raise Http404
            # message= MessageView(request=request)
            # message.title="همچنین "
            # return message.show(request=request)
        context = getContext(request)
        context['header_image'] = PictureRepo(
            request=request, app_name=APP_NAME).picture(name=PictureEnum.ORDER_HEADER)
        context['order'] = order
        context['order_lines_s'] = json.dumps(
            OrderLineSerializer(order.orderline_set.all(), many=True).data)
        context['body_class'] = "shopping-cart"
        
        context['add_order_in_ware_house_form']=AddOrderInWareHouseForm()
        
        ware_houses=WareHouseRepo(request=request).list()
        context['ware_houses']=ware_houses
        
        me_supplier = SupplierRepo(request=request).me
        if me_supplier is not None and order.supplier == me_supplier and order.status == OrderStatusEnum.ACCEPTED:
            do_pack_form = DoPackForm()
            context['do_pack_form'] = do_pack_form

         # do ship form
        me_shipper = ShipperRepo(request=request).me

        if me_shipper is not None and order.status == OrderStatusEnum.PACKED and not order.no_ship:
            do_ship_form = DoShipForm()
            context['do_ship_form'] = do_ship_form
        # do deiver form
        customer = CustomerRepo(user=user).me
        if customer is not None and (order.status == OrderStatusEnum.SHIPPED or (order.status == OrderStatusEnum.PACKED and order.no_ship == True)) and order.customer == customer:
            do_deliver_form = DoDeliverForm()
            context['do_deliver_form'] = do_deliver_form
        if customer is not None and order.status == OrderStatusEnum.CONFIRMED and order.customer == customer:
            do_cancel_form = CancelOrderForm()
            context['do_cancel_form'] = do_cancel_form

        return render(request, TEMPLATE_ROOT+"order.html", context)

    def edit_order(self,request,*args, **kwargs):
        user = request.user
        order = OrderRepo(request=request).order(*args, **kwargs)
        if order is None:
            raise Http404
            # message= MessageView(request=request)
            # message.title="همچنین "
            # return message.show(request=request)
        context = getContext(request)
        context['header_image'] = PictureRepo(
            request=request, app_name=APP_NAME).picture(name=PictureEnum.ORDER_HEADER)
        context['order'] = order
        context['order_lines_s'] = json.dumps(
            OrderLineSerializer(order.orderline_set.all(), many=True).data)
        context['body_class'] = "shopping-cart"
        
        context['add_order_in_ware_house_form']=AddOrderInWareHouseForm()
        
        ware_houses=WareHouseRepo(request=request).list()
        context['ware_houses']=ware_houses
        
        me_supplier = SupplierRepo(request=request).me
        if me_supplier is not None and order.supplier == me_supplier and order.status == OrderStatusEnum.ACCEPTED:
            do_pack_form = DoPackForm()
            context['do_pack_form'] = do_pack_form

         # do ship form
        me_shipper = ShipperRepo(request=request).me

        if me_shipper is not None and order.status == OrderStatusEnum.PACKED and not order.no_ship:
            do_ship_form = DoShipForm()
            context['do_ship_form'] = do_ship_form
        # do deiver form
        customer = CustomerRepo(user=user).me
        if customer is not None and (order.status == OrderStatusEnum.SHIPPED or (order.status == OrderStatusEnum.PACKED and order.no_ship == True)) and order.customer == customer:
            do_deliver_form = DoDeliverForm()
            context['do_deliver_form'] = do_deliver_form
        if customer is not None and order.status == OrderStatusEnum.CONFIRMED and order.customer == customer:
            do_cancel_form = CancelOrderForm()
            context['do_cancel_form'] = do_cancel_form

        return render(request, TEMPLATE_ROOT+"order-edit.html", context)

    def orders(self, request, *args, **kwargs):
        
        orders = OrderRepo(request=request).orders(*args, **kwargs)
        context = getContext(request)
        customer=CustomerRepo(request=request).customer(*args, **kwargs)
        shipper=ShipperRepo(request=request).shipper(*args, **kwargs)
        supplier=SupplierRepo(request=request).supplier(*args, **kwargs)
        if supplier is not None:
            context['orders_title']="لیست سفارشات "+supplier.title
            orders=orders.filter(supplier=supplier)
            context['supplier']=supplier

        if customer is not None:
            context['orders_title']="لیست سفارشات "+customer.title
            orders=orders.filter(customer=customer)
            context['customer']=customer

        if shipper is not None:
            context['orders_title']="لیست سفارشات "+shipper.title
            orders=orders.filter(shipper=shipper)
            context['shipper']=shipper


        context['header_image'] = PictureRepo(request=request, app_name=APP_NAME).picture(name=PictureEnum.ORDER_HEADER)

        context['orders'] = orders
        # print(orders)
        context['body_class'] = "shopping-cart"
        return render(request, TEMPLATE_ROOT+"orders.html", context)

    def do_deliver_order(self, request):
        if request.method == 'POST':
            do_deliver_form = DoDeliverForm(request.POST)
            if do_deliver_form.is_valid():
                ware_house_id = do_deliver_form.cleaned_data['ware_house_id']
                order_id = do_deliver_form.cleaned_data['order_id']
                description = do_deliver_form.cleaned_data['description']
                order = OrderRepo(request=request).do_deliver(
                    order_id=order_id, description=description,ware_house_id=ware_house_id)
                
                if order is not None:
                    return redirect(order.get_absolute_url())
        return redirect(reverse('market:orders', kwargs={'profile_id': 0}))

    def do_pack_order(self, request):
        if request.method == 'POST':
            do_pack_form = DoPackForm(request.POST)
            if do_pack_form.is_valid():
                order_id = do_pack_form.cleaned_data['order_id']
                count_of_packs = do_pack_form.cleaned_data['count_of_packs']
                description = do_pack_form.cleaned_data['description']
                ware_house_id = do_pack_form.cleaned_data['ware_house_id']
                if count_of_packs is None:
                    count_of_packs = 1
                order = OrderRepo(request=request).do_pack(
                    order_id=order_id, count_of_packs=count_of_packs, description=description)
                # WareHouseRepo(request=request).add_order_in_ware_house(
                #     order_id=order.id, ware_house_id=ware_house_id, direction=False, description=description)
                if order is not None:
                    return redirect(order.get_absolute_url())
        # return redirect(reverse('market:orders_supplier',kwargs={'supplier_id':0}))
        return redirect(order.get_absolute_url())

    def do_ship_order(self, request):
        if request.method == 'POST':
            do_ship_form = DoShipForm(request.POST)
            if do_ship_form.is_valid():
                order_id = do_ship_form.cleaned_data['order_id']
                description = do_ship_form.cleaned_data['description']
                order = OrderRepo(request=request).do_ship(
                    order_id=order_id, description=description)

                if order is not None:
                    return redirect(order.get_absolute_url())
        return redirect(reverse('market:orders_shipper', kwargs={'shipper_id': 0}))

    def do_cancel_order(self, request):
        if request.method == 'POST':
            cancel_order_form = CancelOrderForm(request.POST)
            if cancel_order_form.is_valid():
                order_id = cancel_order_form.cleaned_data['order_id']
                description = cancel_order_form.cleaned_data['description']
                order = OrderRepo(request=request).do_cancel(
                    order_id=order_id, description=description)

                if order is not None:
                    return redirect(order.get_absolute_url())
        return redirect(reverse('market:orders', kwargs={'customer_id': 0}))

    def order_invoice(self, request, *args, **kwargs):
        context = getContext(request)
        TAX_PERCENT = 0
        order = OrderRepo(request=request).order(*args, **kwargs)
        order_lines = []
        lines_total = 0
        for order_line in order.orderline_set.all():
            quantity = order_line.quantity
            unit_name = order_line.unit_name
            unit_price = order_line.unit_price
            lines_total += (quantity*unit_price)
            order_lines.append({
                'quantity': quantity,
                'unit_name': unit_name,
                'unit_price': unit_price,
                'line_total': quantity*unit_price,
                'product_title': order_line.product.title,
                'description': f""" <small>{order_line.description}</small>""",
            })

        tax = int(TAX_PERCENT*(lines_total)/100)
        ship_fee = 0
        descriptions = [
            f""" سفارش شماره {order.pk} <span class="bg-dark text-light px-2 rounded">{order.status}</span>""",
            f"""<small>تعداد بسته قابل تحویل </small>: {order.count_of_packs} بسته""",
            f"""<small>آدرس تحویل :</small> {order.address}""",
            f"""واحد مبلغ ها {CURRENCY} می باشد.""",
            ]
        total_for_pay = tax+lines_total
        print_date = PersianCalendar().date
        order = {
            'customer': order.customer.profile.name,
            'supplier': order.supplier,
            'tax': tax,
            'lines_total': lines_total,
            'ship_fee': ship_fee,
            'total_for_pay': total_for_pay,
            'print_date': print_date,
            'descriptions': descriptions,
        }
        context['order_lines'] = order_lines
        context['order'] = order
        context['project'] = {}
        return render(request, TEMPLATE_ROOT+"order-invoice.html", context)


class OfferViews(View):
    def offer(self, request, *args, **kwargs):

        offer = OfferRepo(request=request).offer(*args, **kwargs)
        page = offer
        context = getContext(request)
        context.update(PageContext(request=request, page=page))
        context['offer'] = offer
        if request.user.has_perm(APP_NAME+".add_offer"):
            context['add_offer_form'] = AddProductForm()
        return render(request, TEMPLATE_ROOT+"offer.html", context)


class BlogViews(View):
    def blog(self, request, *args, **kwargs):

        blog = BlogRepo(request=request).blog(*args, **kwargs)
        page = blog
        context = getContext(request)
        context.update(PageContext(request=request, page=page))
        context['blog'] = blog
        if request.user.has_perm(APP_NAME+".add_blog"):
            context['add_blog_form'] = AddProductForm()
        return render(request, TEMPLATE_ROOT+"blog.html", context)


class CategoryViews(View):
    def category(self, request, *args, **kwargs):
        
        category = CategoryRepo(request=request).category(*args, **kwargs)
        page = category
        context = getContext(request)
        context.update(PageContext(request=request, page=page))
        context['category'] = category
        categories = category.childs().order_by('priority')
        context['categories'] = categories
        products = category.products.all().order_by('priority')
        context['products'] = products
        context['top_products'] = category.top_products(3)
        if request.user.has_perm(APP_NAME+".add_product") and len(categories) == 0:
            context['add_product_form'] = AddProductForm()
        if request.user.has_perm(APP_NAME+".add_category") and len(products) == 0:
            context['add_category_form'] = AddCategoryForm()
        return render(request, TEMPLATE_ROOT+"category.html", context)
