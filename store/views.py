import requests
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import response, viewsets, permissions
from django.core.paginator import Paginator
from . models import Category, SubCategory, Product, Contact
from cart.cart import Cart

from . forms import FormContact
# class FormContact trong file forms.py
from . serializers import ProductSerializer

# Create your views here.


def index(request):
    cart = Cart(request)
    tbgd_subcategory = SubCategory.objects.filter(
        category__slug='thiet-bi-gia-dinh').values_list('slug')
    # values_list chuyển dữ liệu Queryset (bên trong có tuple) về dạng list của Queryset, nhập slug để tạo list các slug của subcategory
    # Queryset là một định dạng của Django khi lấy table ra từ SQL, cần chuyển đổi về dạng list để thao tác
    # Ví dụ:
    # tbgd subcategory = <QuerySet[("ban-ui",),("cay-nuoc-nong lanh',), ('may-hut-bui",), ('quat dien',), ("may-loc-nuoc',)]>
    # for sub in tbgd_subcategory: tbgd_list_sub.append(sub[0])
    # sub[0] để lấy giá trị bên trong tuple trong Queryset trong list tbgd_subcategory

    ddnb_subcategory = SubCategory.objects.filter(
        category__slug='do-dung-nha-bep').values_list('slug')

    tbgd_list_sub = []
    ddnb_list_sub = []

    for sub in tbgd_subcategory:
        tbgd_list_sub.append(sub[0])
    # sub[0] để lấy giá trị bên trong tuple trong Queryset trong list tbgd_subcategory

    for sub in ddnb_subcategory:
        ddnb_list_sub.append(sub[0])

    tbgd_products = Product.objects.filter(subcategory__slug__in=tbgd_list_sub)
    ddnb_products = Product.objects.filter(subcategory__slug__in=ddnb_list_sub)

    return render(request, 'store/index.html', {
        'tbgd_products': tbgd_products,
        'ddnb_products': ddnb_products,
        'cart': cart
    })


def productlist(request, slug):
    cart = Cart(request)
    sub_cats = SubCategory.objects.all()

    if slug == 'tat-ca-san-pham':
        products = Product.objects.all()
        sub_name = 'Tất cả sản phẩm (' + str(len(products)) + ')'
    else:
        products = Product.objects.filter(subcategory__slug=slug)
        select_sub = SubCategory.objects.get(slug=slug)
        # slug đầu tiên là filed trong model, slug thứ 2 là slug trên hàm def
        sub_name = select_sub.name + ' (' + str(len(products)) + ')'

    # Lọc giá
    from_price = 0
    to_price = 0
    product_name = ''
    if request.GET.get('from_price'):
        # nếu nhấn và btn Lọc thì sẽ lấy 'from_price'
        from_price = int(request.GET.get('from_price'))
        to_price = int(request.GET.get('to_price'))
        product_name = request.GET.get('product_name')

        if product_name != '':
            # if produce_name:
            products = Product.objects.filter(name__contains=product_name)
        products = [product for product in products if from_price <=
                    product.price <= to_price]
        # list comprehensiom
        sub_name = f'Số sản phẩm có giá từ "{from_price}" đến "{to_price}": ' + '(' + str(
            len(products)) + ')'

    page = request.GET.get('page', 1)
    paginator = Paginator(products, 20)
    products_pager = paginator.page(page)

    return render(request, 'store/product-list.html', {
        'sub_cats': sub_cats,
        'products': products_pager,
        'sub_name': sub_name,
        'from_price': from_price,
        'to_price': to_price,
        'cart': cart,
    })


def productdetail(request, pk):
    cart = Cart(request)
    product = Product.objects.get(id=pk)
    sub_category_id = Product.objects.filter(pk=pk).values_list('subcategory')
    # values_list('subcategory') dùng để lọc trích ra id sub category của product, nếu để values_list('') thì sẽ cho ra 1 list với toàn bộ thông tin của product

    same_products = Product.objects.filter(
        subcategory__in=sub_category_id).exclude(pk=pk)

    sub_cats = SubCategory.objects.all()

    all_products = Product.objects.all()

    return render(request, 'store/product-detail.html', {
        'pk': pk,
        'product': product,
        'same_product': same_products,
        'sub_cats': sub_cats,
        'all_products': all_products,
        'cart': cart,
    })


def search(request):
    cart = Cart(request)
    product_name = ''
    if request.GET.get('product_name'):
        # GET là method get trong html
        sub_cats = SubCategory.objects.all()
        # kế thừa từ productlist
        product_name = request.GET.get('product_name')
        search_products = Product.objects.filter(name__contains=product_name)
        sub_name = f'Số sản phẩm có từ khóa "{product_name}": ' + \
            '(' + str(len(search_products)) + ')'
        # kế thừa từ productlist

    page = request.GET.get('page', 1)
    paginator = Paginator(search_products, 20)
    products_pager = paginator.page(page)

    return render(request, 'store/product-list.html', {
        'products': products_pager,
        'all_products': search_products,
        # all_products khai báo để phòng hờ, bỏ cũng được
        'product_name': product_name,
        'sub_cats': sub_cats,
        'sub_name': sub_name,
        'cart': cart,
    })


def contact(request):
    cart = Cart(request)
    form = FormContact()
    result = ''
    if request.POST.get('btnSubmit'):
        form = FormContact(request.POST, Contact)
        if form.is_valid():
            # if form.is_valid(): nếu dữ liệu nhập đúng
            post = form.save(commit=False)
            # save(commit=False): khoan save, để check đúng field chưa
            post.name = form.cleaned_data['name']
            # cleaned_data là để xóa attrs={'class' : 'form-control','placeholder' : 'Your Name','required' : 'required'
            post.email = form.cleaned_data['email']
            post.subject = form.cleaned_data['subject']
            post.message = form.cleaned_data['message']
            post.save()

            result = '''
                <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                    <symbol id="check-circle-fill" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                    </symbol>
                </svg>
                <div class="alert alert-success d-flex align-items-center" role="alert">
                    <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:"><use xlink:href="#check-circle-fill"/></svg>
                    <div>
                        Submit Successfully!
                    </div>
                </div>
            '''

    return render(request, 'store/contact.html', {
        'form': form,
        'result': result,
        'cart': cart
    })


# def demo_api(request):
#     url_api = "https://fakestoreapi.com/products/"
#     data = requests.get(url_api)

#     return HttpResponse(data.text, content_type='application/json')
#     # data.content dủng để lấy nguyên mẫu, data.text dủng để điều chỉnh sử dụng trên model


def api_update_product(request):
    url = requests.get("https://fakestoreapi.com/products/")
    items = url.json()
    if request.POST.get("btnSubmit"):
        for item in items:
            product = Product()
            product.subcategory = SubCategory.objects.get(pk=1)
            product.name = item.get("title")
            product.price = item.get("price")
            product.price_origin = item.get("price")
            product.content = item.get("description")
            product.image = item.get("image")
            product.viewed = item.get("rating").get("count")
            product.save

    return render(request, 'store/api_update.html')


def products_service(request):
    product = Product.objects.all()
    result_list = list(product.values('name', 'price', 'content', 'image'))

    return JsonResponse(result_list, safe=False)


def product_service_detail(request, pk):
    product = Product.objects.filter(pk=pk)
    result_list = list(product.values())[0]

    return JsonResponse(result_list, safe=False)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # permissions_classes = [permissions.IsAdminUser]
    # permission_classes là mặc định
    # Ai là admin user mới được access vào api
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # IsAuthenticated miễn có tài khoản của trang web là được cập nhật API
    # IsAuthenticatedOrReadOnly có tài khoản của trang web nhưng chỉ được xem API
