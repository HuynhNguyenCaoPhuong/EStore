from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import Argon2PasswordHasher
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from . models import KhachHang, Customer
from . forms import FormDangKy, FormCustomer, FormUser
from cart.models import Order, OrderItem
from cart.cart import Cart
from store.models import Product

def login_signup(request):
    form = FormDangKy()
    result_signup = ''
    result_login = ''

    if request.POST.get('btnSignup'):
        # btnSignup là name của button Đăng ký
        form = FormDangKy(request.POST, KhachHang)
        # Lưu vào model KhachHang
        if form.is_valid() and form.cleaned_data['mat_khau'] == form.cleaned_data['xac_nhan_mat_khau']:
            hasher = Argon2PasswordHasher()
            post = form.save(commit=False)
            post.ho = form.cleaned_data['ho']
            post.ten = form.cleaned_data['ten']
            post.email = form.cleaned_data['email']
            post.dien_thoai = form.cleaned_data['dien_thoai']
            post.mat_khau = hasher.encode(form.cleaned_data['mat_khau'], 'abcd^123')
            # encode(hàm cần mã hóa, phương thức mã hóa[ do mình tạo để tự mã hóa, dùng nhiều ký tự])
            post.dia_chi = form.cleaned_data['dia_chi']
            post.save()
            result_signup = '''
                <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                    <symbol id="check-circle-fill" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                    </symbol>
                </svg>
                <div class="alert alert-success d-flex align-items-center" role="alert">
                    <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:"><use xlink:href="#check-circle-fill"/></svg>
                    <div>
                        Bạn đã đăng ký thành công!
                    </div>
                </div>
            '''
        else:
            result_signup = '''
                <div class="alert alert-danger" role="alert">
                    Đăng ký không thành công!
                </div>
            '''
    
    if request.POST.get('btnLogin'):
        email = request.POST.get('email')
        password = request.POST.get('password')
        hasher = Argon2PasswordHasher()
        ma_hoa = hasher.encode(password,'abcd^123')
        # tạo một biến là mã hóa của password
        customer = KhachHang.objects.filter(email=email, mat_khau=ma_hoa)
        # so sánh mật khẩu với mã hóa
        if customer.count() > 0:
            request.session['s_customer'] = customer.values()[0]
            # tạo session
            return redirect('store:index')
            # quay về trang chủ
        else:
            result_login = '''
                <div class="alert alert-danger" role="alert">
                    Sai thông tin đăng nhập!
                </div>
            '''

    return render(request, 'users/login.html', {
        'form' : form,
        'result_signup' : result_signup,
        'result_login' : result_login,
    })

def user_logout (request):
    if 's_customer' in request.session:
        del request.session['s_customer']
    return redirect('users:login')

def login_signup2(request):
    form_user = FormUser()
    form_customer = FormCustomer()
    result_signup = ''
    if request.POST.get('btnSignup'):
        form_user = FormUser(request.POST, User)
        form_customer = FormCustomer(request.POST, Customer)
        if form_user.is_valid() and form_customer.is_valid():
            if form_user.cleaned_data['password'] == form_user.cleaned_data['confirm_password']:
                # User
                user = form_user.save()
                user.set_password(user.password)
                # set_password là hàm đi kèm trong model User, tự động lấy Argon2 trong settting.py
                user.save()

                # Customer
                customer = form_customer.save(commit=False)
                customer.user = user
                customer.dien_thoai = form_customer.cleaned_data['dien_thoai']
                customer.dia_chi = form_customer.cleaned_data['dia_chi']
                customer.save()
                
                result_signup = '''
                    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                        <symbol id="check-circle-fill" fill="currentColor" viewBox="0 0 16 16">
                            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                        </symbol>
                    </svg>
                    <div class="alert alert-success d-flex align-items-center" role="alert">
                        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:"><use xlink:href="#check-circle-fill"/></svg>
                        <div>
                            Bạn đã đăng ký thành công!
                        </div>
                    </div>
                '''
            else:
                result_signup = '''
                    <div class="alert alert-danger" role="alert">
                        Đăng ký không thành công!
                    </div>
                '''

    # Đăng nhập
    if request.POST.get('btnLogin'):
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        # hàm authenticate có sẵn của model User tự động tão session, không cần phải tạo session thủ công

        # if user is not None:
        if user:
            login(request,user)
            return redirect('store:index')


    return render(request, 'users/login2.html', {
        'form_user' : form_user,
        'form_customer' : form_customer,
        'result_signup' : result_signup,
    })


def user_logout2 (request):
    logout(request)
    return redirect('users:login2')


def myaccount(request):
    if not request.user.username:
        messages.warning(request,"Vui lòng đăng nhập lại.")
        return redirect('users:login2')

    result = ''

    if request.POST.get('btnUpdateUser'):
        ho = request.POST.get('last_name')
        ten = request.POST.get('first_name')
        dt = request.POST.get('mobile')
        mail = request.POST.get('email')
        dc = request.POST.get('address')

        s_customer = request.user
        customer = Customer.objects.get(user__id=s_customer.id)
        customer.user.last_name = ho
        customer.user.first_name = ten
        customer.dien_thoai = dt
        customer.email = mail
        customer.dia_chi = dc
        customer.save()

        s_customer.last_name = ho
        s_customer.first_name = ten
        result = '''
                <div class = "col-md-12">
                    <div class="alert alert-success" role="alert">
                        Cập nhật thành công!
                    </div>
                </div>
                '''
    
    # Cách 1 chưa tối ưu, nhập sai matkhauhientai - bug
    # if request.POST.get('btnUpdatePass'):
    #     s_customer = request.user
    #     username = User.objects.get(username=s_customer.username)
    #     matkhauhientai = request.POST.get('current_password')
    #     matkhaucapnhat = request.POST.get('new_password')
    #     matkhaucapnhat_conf = request.POST.get('new_password_conf')

    #     user = authenticate(request, username=username, password=matkhauhientai)

    #     if user and matkhaucapnhat==matkhaucapnhat_conf:
    #         user.set_password(matkhaucapnhat)
    #         user.save()
    #         result = '''
    #                 <div class = "col-md-12">
    #                     <div class="alert alert-success" role="alert">
    #                         Cập nhật thành công!
    #                     </div>
    #                 </div>
    #                 '''
            
    #     else:
    #         result = '''
    #             <div class = "col-md-12">
    #                 <div class="alert alert-danger" role="alert">
    #                     Vui lòng kiểm tra thông tin!
    #                 </div>
    #             </div>
    #             '''
    # return render(request, 'users/my-account.html',{
    #     'result': result
    # })
    # Cách 2
    if request.POST.get('btnUpdatePass'):
        s_customer = request.user
        matkhauhientai = request.POST.get('current_password')
        matkhaucapnhat = request.POST.get('new_password')
        matkhaucapnhat_conf = request.POST.get('new_password_conf')

        if s_customer.check_password(matkhauhientai) and matkhaucapnhat==matkhaucapnhat_conf:
            s_customer.set_password(matkhaucapnhat)
            s_customer.save()
            result = '''
                    <div class = "col-md-12">
                        <div class="alert alert-success" role="alert">
                            Cập nhật thành công!
                        </div>
                    </div>
                    '''
            
        else:
            result = '''
                <div class = "col-md-12">
                    <div class="alert alert-danger" role="alert">
                        Vui lòng kiểm tra thông tin!
                    </div>
                </div>
                '''
            
    cart = Cart(request)
    orders = Order.objects.filter(username=request.user.username)
    dict_orders = {}
    for order in orders:
        items = list(OrderItem.objects.filter(order=order.id).values())
        # Hiện hữu là Querryset cần lấy values và chuyển về list
        for item in items:
            product = Product.objects.get(id=item['product_id'])
            item['product_name'] = product.name
            item['product_image'] = product.image
            item['total_price'] = order.total
        else:
            dict_orders_items = {
                order.id: items
            }
            dict_orders.update(dict_orders_items)


    return render(request, 'users/my-account.html',{
        'result': result,
        'cart': cart,
        'orders': orders,
        'dict_orders': dict_orders,
    })