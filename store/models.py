from django.conf import settings
from django.db import models
from django.contrib.sessions.models import Session
from checkout.models import Transaction
from django.utils.translation import gettext as _
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')


class Product(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.TextField(null=True)
    description = models.TextField()
    image = models.ImageField()
    pdf_file = models.FileField(null=True)
    price = models.FloatField()
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    @property
    def pdf_file_url(self):
        return settings.SITE_URL + self.pdf_file.url

class Order(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    @property
    def customer_name(self):
        return f"{self.customer['first_name']} {self.customer['last_name']}"

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class Slider(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.TextField(max_length=500)
    image = models.ImageField(null=True)
    order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Slider')
        verbose_name_plural = _('Sliders')

class Cart(models.Model):
    items = models.JSONField(default=dict)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)