import django
from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone = models.IntegerField(max_length=20)
    address = models.CharField(max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}, {self.email}, {self.phone}, {self.address}'


class Goods(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    amount = models.IntegerField()
    create_at = models.DateField(auto_now_add=True)

    def total_price(self):
        return self.price * self.amount

    def __str__(self):
        return f'{self.name} {self.description} {self.price} {self.amount} {self.create_at}'


class Order(models.Model):
    price = models.IntegerField()
    create_at = models.DateField(auto_now_add=True)
    client_id = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_app.Client')
    goods_id = models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_app.Goods')

    def __str__(self):
        return f'{self.price}, {self.client_id}, {self.goods_id}'
