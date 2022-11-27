from django.contrib.auth import views
from django.urls import path
from .views import index, UserCreateView, Login, ProductListView, ByeProductCreateView, PurchaseListView, Logout, \
    ProductCreateView, ProductDeleteView, ProductUpdate

urlpatterns = [
    path('homepage', index, name='index'),
    path('', ProductListView.as_view(), name="home"),
    path('logout/', Logout.as_view(), name='logout'),
    path('byers/<int:pk>', ByeProductCreateView.as_view(), name="byers"),
    path('purchaselist', PurchaseListView.as_view(), name="purchaselist"),
    path('login/', Login.as_view(), name='login'),
    path('registration', UserCreateView.as_view(), name="registration"),
    path('product/create/', ProductCreateView.as_view(), name='product-create'),
    path('product/update/<int:pk>', ProductUpdate.as_view(), name='product-update'),
    path('product/delete/<int:pk>', ProductDeleteView.as_view(), name='product-delete'),


]
