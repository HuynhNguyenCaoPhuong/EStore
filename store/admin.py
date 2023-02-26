from django.contrib import admin
from . import models

# Register your models here.


# Cách 1
# admin.site.register(models.Category)

# Cách 2 đăng ký model trong admin mặc định theo django
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name', 'slug']
    # ordering (tạo mũi tên sắp xếp trong trang admin), list_display (diễn giải theo nhiều danh mục) là tên biến mặc định của django
    # tên class CategoryAdmin thì tùy dev chọn
    search_fields = ['name']


@admin.register(models.SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
    prepopulated_fields = {
        'slug': ['name']
    }
    # tự tạo slug thông qua utocomplete_fields và prepopulated_fields trong trang admin, sử dụng dictionary với keyword là chuỗi slug và value là list của name
    # lưu ý: tạo slug tự động chỉ giới hạn một số chữ có dấu, đối với các chữ có dấu như "ặ" thì phải nhập tay slug
    list_display = ['name', 'image', 'slug', 'category_name']
    # category_name phải trùng với category_name của def
    search_fields = ['name']

    def category_name(self, subcategory):
        return subcategory.category.name


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['subcategory']
    # để gõ tìm subcategory trong trang admin, lưu ý phải có search_fields = ['name'] trong class subcategory thì django mới tự động tìm kiếm
    list_display = ['name', 'price', 'viewed_status', 'subcategory']
    list_filter = ['public_day', 'subcategory']
    list_editable = ['price']
    # cho phép điều chỉnh field bằng list_editable
    search_fields = ['name__istartswith']
    # istartswith bắt đầu với chữ
    list_per_page = 10
    # 10 tương ứng với 10 product trong 1 trang
    # ordering = ['name', 'price', 'viewed']

    def category_name(self, product):
        return product.subcategory.name

    @admin.display(ordering='viewed')
    # @admin.display(ordering='viewed') dùng gán ordering viewed_status vào viewed do viewed_status là field tự tạo qua def không có sẵn trong model.py nên nếu ordring bằng viewed_status thì code sẽ không chạy dẫn đến lỗi
    def viewed_status(self, product):
        if product.viewed == 0:
            return 'No'
        return 'Yes'
