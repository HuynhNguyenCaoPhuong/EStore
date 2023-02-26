from django import forms
from django.contrib.auth.models import User
from .models import KhachHang, Customer


class FormDangKy(forms.ModelForm):
    ho = forms.CharField(max_length=255, label='Họ', widget=forms.TextInput(attrs={
        "class" : "form-control",
        "placeholder" : "Họ",
        "required" : "required",
    }))
    ten = forms.CharField(max_length=255, label='Tên', widget=forms.TextInput(attrs={
        "class" : "form-control",
        "placeholder" : "Tên",
        "required" : "required",
    }))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        "class" : "form-control",
        "placeholder" : "Email",
        "required" : "required",
    }))
    mat_khau = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput(attrs={
        "class" : "form-control",
        "placeholder" : "Mật Khẩu",
        "required" : "required",
    }))
    xac_nhan_mat_khau = forms.CharField(label='Xác nhận Mật khẩu', widget=forms.PasswordInput(attrs={
        "class" : "form-control",
        "placeholder" : "Xác nhận Mật Khẩu",
        "required" : "required",
    }))
    dien_thoai = forms.CharField(max_length=20, label='Điện thoại', widget=forms.TextInput(attrs={
        "class" : "form-control",
        "placeholder" : "Điện thoại",
        "required" : "required",
    }))
    dia_chi = forms.CharField(label='Địa chỉ', widget=forms.Textarea(attrs={
        "class" : "form-control",
        "placeholder" : "Địa chỉ",
        "rows" : "3",
    }))

    class Meta:
        model = KhachHang
        fields = '__all__'
    # khai báo các field tương ứng vào model Contact, all là tương ứng với tất cả field
    # trường hợp khai báo tương ứng một số field, khai báo tupple hoặc list-> fields = ('name', 'email') or fields = ['name', 'email']

class FormUser(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Username", widget=forms.TextInput(attrs={
        "class" : "form-control",
        "placeholder" : "Username",
        "required" : "required",
    }))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        "class" : "form-control",
        "placeholder" : "Email",
        "required" : "required",
    }))
    last_name = forms.CharField(max_length=255, label="Họ", widget=forms.TextInput(attrs={
        "class" : "form-control",
        "placeholder" : "Họ",
        "required" : "required",
    }))
    first_name = forms.CharField(max_length=255, label="Tên", widget=forms.TextInput(attrs={
        "class" : "form-control",
        "placeholder" : "Tên",
        "required" : "required",
    }))
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput(attrs={
        "class" : "form-control",
        "placeholder" : "Mật Khẩu",
        "required" : "required",
    }))
    confirm_password = forms.CharField(label='Xác nhận Mật khẩu', widget=forms.PasswordInput(attrs={
        "class" : "form-control",
        "placeholder" : "Xác nhận Mật Khẩu",
        "required" : "required",
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')
        # lấy field ('username', 'email', 'first_name', 'last_name', 'password') trong model User

class FormCustomer(forms.ModelForm):
    dien_thoai = forms.CharField(max_length=20, label='Điện thoại', widget=forms.TextInput(attrs={
        "class" : "form-control",
        "placeholder" : "Điện thoại",
        "required" : "required",
    }))
    dia_chi = forms.CharField(label='Địa chỉ', widget=forms.Textarea(attrs={
        "class" : "form-control",
        "placeholder" : "Địa chỉ",
        "rows" : "3",
    }))

    class Meta:
        model = Customer
        exclude = ('user',)
        # lấy tất cả các field trừ (exclude) trong model Customer