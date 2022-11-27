from django.contrib.auth.models import AbstractUser
from django.db import models

class MyUser(AbstractUser):
    deposit = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

class Product(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(blank=True, null=True)
    amount = models.IntegerField()

    class Meta:
        ordering = ['title']
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.title

class Purchase(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date_of_purchase = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_of_purchase']
        verbose_name = "purchase"
        verbose_name_plural = "purchases"

    def __str__(self):
        return f"{self.product}"

class Return(models.Model):
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE)
    date_return = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_return']
        verbose_name = "return"
        verbose_name_plural = "returns"

    def __str__(self):
        return self.purchase
