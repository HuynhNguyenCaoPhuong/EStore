from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.index, name='index'),
    path('subcategory/<slug:slug>/', views.productlist, name='product-list'),
    # đường link sẽ là subcategory ánh xạ từ productlist
    path('product/<int:pk>/', views.productdetail, name='product-detail'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
    # path('call_api/', views.demo_api),
    path('product_api/', views.api_update_product),
    path('api/product/', views.products_service),
    path('api/product/<int:pk>/', views.product_service_detail),
]
