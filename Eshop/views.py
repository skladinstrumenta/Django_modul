from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from Eshop.forms import UserCreateForm, PurchaseCreateForm, ProductCreateForm, ReturnCreateForm
from Eshop.models import Product, Purchase, MyUser, Return


class SuperUserRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('home')


class UserCreateView(CreateView):
    form_class = UserCreateForm
    template_name = 'registration.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        valid = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return valid


class ProductListView(ListView):
    model = Product
    template_name = 'index.html'
    extra_context = {'form': PurchaseCreateForm, 'create_form': ProductCreateForm()}
    paginate_by = 3


class Login(LoginView):
    success_url = '/'
    template_name = 'login.html'

    def get_success_url(self):
        return self.success_url


class Logout(LoginRequiredMixin, LogoutView):
    next_page = 'home'
    login_url = 'login/'
    success_url = reverse_lazy("purchaselist")


class BuyProductCreateView(CreateView):
    form_class = PurchaseCreateForm
    template_name = "index.html"
    success_url = "/purchaselist"

    def form_valid(self, form):
        obj = form.save(commit=False)
        product_id = self.kwargs.get('pk')
        product = Product.objects.get(id=product_id)
        customer = MyUser.objects.get(id=self.request.user.id)
        order_amount = int(self.request.POST['amount'])
        if order_amount > product.amount:
            messages.error(self.request, '???? ?????????????? ?????????????? ????????????')
            return HttpResponseRedirect('/')
        purchase_sum = product.price * order_amount
        if purchase_sum > customer.deposit:
            messages.error(self.request, '?? ?????? ???????????????????????? ?????????????? ?????? ?????????? ??????????????')
            return HttpResponseRedirect('/')
        customer.deposit -= purchase_sum
        product.amount -= order_amount
        obj.product = product
        obj.user = customer

        with transaction.atomic():
            obj.save()
            product.save()
            customer.save()

        return super().form_valid(form)


class PurchaseListView(LoginRequiredMixin, ListView):
    login_url = 'login/'
    model = Purchase
    template_name = 'purchaselist.html'

    def get_queryset(self):
        if not self.request.user.is_superuser:
            queryset = Purchase.objects.filter(user=self.request.user)
            return queryset
        queryset = Purchase.objects.all()
        return queryset


class ProductCreateView(SuperUserRequiredMixin, CreateView):
    template_name = 'createproduct.html'
    http_method_names = ['get', 'post']
    extra_context = {'create_form': ProductCreateForm()}
    form_class = ProductCreateForm
    success_url = '/'


class ProductUpdate(SuperUserRequiredMixin, UpdateView):
    model = Product
    fields = ['title', 'text', 'price', 'image', 'amount']
    template_name = 'updateproduct.html'
    success_url = '/'


class ReturnPurchaseCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    form_class = ReturnCreateForm
    template_name = "purchaselist.html"
    success_url = "/purchaselist"

    def form_valid(self, form):
        obj = form.save(commit=False)
        purchase_id = self.kwargs.get('pk')
        purchase = Purchase.objects.get(id=purchase_id)
        purchase_time_on = timezone.now() - purchase.date_of_purchase
        time_button_return = 180
        if purchase_time_on.seconds > time_button_return:
            messages.error(self.request, '?????????? ???????????? ???????????? ???? ?????????????? ??????????????')
            return HttpResponseRedirect('/purchaselist')
        obj.purchase = purchase
        obj.save()
        return super().form_valid(form)


class ReturnListView(LoginRequiredMixin, ListView):
    login_url = 'login/'
    model = Return
    template_name = 'returnpurchaselist.html'
    extra_context = {'form': ReturnCreateForm}

    def get_queryset(self):
        if not self.request.user.is_superuser:
            queryset = Return.objects.filter(purchase__user=self.request.user)
            return queryset
        queryset = Return.objects.all()
        return queryset


class DeletePurchaseView(SuperUserRequiredMixin, DeleteView):
    model = Purchase
    success_url = '/returnpurchaselist'

    def form_valid(self, form):
        purc = self.get_object()
        customer = purc.user
        product = purc.product
        customer.deposit += purc.total()
        product.amount += purc.amount

        with transaction.atomic():
            customer.save()
            product.save()
            purc.delete()

        return HttpResponseRedirect(self.success_url)


class DeleteReturnView(SuperUserRequiredMixin, DeleteView):
    model = Return
    success_url = '/returnpurchaselist'

