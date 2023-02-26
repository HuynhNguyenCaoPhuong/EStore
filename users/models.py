from django.db import models
from django.contrib.auth.models import User


class KhachHang(models.Model):
    ho = models.CharField(max_length=255, blank= False)
    ten = models.CharField(max_length=255, blank= False)
    email = models.EmailField(unique=True)
    mat_khau = models.CharField(max_length=50, blank=False)
    dien_thoai = models.CharField(max_length=20)
    dia_chi = models.TextField()

    def __str__(self):
        return self.ten

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    # sử dụng model User có thể tự động mã hóa luôn khỏi khai báo mã hóa mật khẩu trong file views.py
    # OnetoOneField là bên model User có field nào là lấy bên Customer field đó, quan hệ parent và child, 1 field name trong User thì chỉ có 1 field name *sử dụng chủ yếu
    # ForeignKey: 1 subcategory thì có nhiều product *sử dụng chủ yếu
    # ManytoManyField chồng 3 lớp field, category -> subcategory -> product tương ứng mối quan hệ giữa category và product
    dien_thoai = models.CharField(max_length=20)
    dia_chi = models.TextField()

    def __str__(self):
        return f'{self.user.username} and {self.dien_thoai}'

    class Meta:
        db_table = u'customers'