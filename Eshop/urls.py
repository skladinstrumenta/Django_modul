from django.urls import path
from .views import UserCreateView, Login, ProductListView, BuyProductCreateView, PurchaseListView, Logout, \
    ProductCreateView, ProductUpdate, ReturnPurchaseCreateView, ReturnListView, DeletePurchaseView, DeleteReturnView

urlpatterns = [
    path('', ProductListView.as_view(), name="home"),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('buy/<int:pk>', BuyProductCreateView.as_view(), name="buy"),
    path('purchaselist', PurchaseListView.as_view(), name="purchaselist"),
    path('registration', UserCreateView.as_view(), name="registration"),
    path('product/create/', ProductCreateView.as_view(), name='product-create'),
    path('product/update/<int:pk>', ProductUpdate.as_view(), name='product-update'),
    path('purchase/delete/<int:pk>', DeletePurchaseView.as_view(), name='purchase-delete'),
    path('delete/return/<int:pk>', DeleteReturnView.as_view(), name='delete-return'),
    path('return/purchase/<int:pk>', ReturnPurchaseCreateView.as_view(), name='return-purchase'),
    path('returnpurchaselist', ReturnListView.as_view(), name='returnpurchaselist')

]
