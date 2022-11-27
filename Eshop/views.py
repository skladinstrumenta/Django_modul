from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from Eshop.forms import UserCreateForm, PurchaseCreateForm, ProductCreateForm
from Eshop.models import Product, Purchase, MyUser


def index(request):
    return render(request, "index.html")


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


class ProductListView(LoginRequiredMixin, ListView):
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
    next_page = 'index'
    login_url = 'login/'
    success_url = reverse_lazy("purchaselist")

class ByeProductCreateView(CreateView):
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
            messages.error(self.request, 'Не хватает наличия товара')
            return HttpResponseRedirect('/')
        purchase_sum = product.price * order_amount
        if purchase_sum > customer.deposit:
            messages.error(self.request, 'У вас недостаточно средств для такой покупки')
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

    def purchase_sum(self, *args, **kwargs):
        object = Purchase.objects.get(id=self.request.id)
        purchase_sum = int(object.price) * int(object.amount)
        return purchase_sum



class ProductCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    template_name = 'createproduct.html'
    http_method_names = ['get', 'post']
    extra_context = {'create_form': ProductCreateForm()}
    form_class = ProductCreateForm
    success_url = '/'


class ProductUpdate(LoginRequiredMixin, UpdateView):
    login_url = 'login/'
    model = Product
    fields = ['title', 'text', 'price', 'image', 'amount']
    template_name = 'updateproduct.html'
    success_url = reverse_lazy('home')

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = '/'




