from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):   
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=150, null=False)
    date_created = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.name
        
class Tag(models.Model):
    name = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.name

class Product(models.Model): 
    CATEGORY = (('In Door', 'In Door'), ('Out Door', 'Out Door'))  
    name = models.CharField(max_length=150, null=False)
    price = models.FloatField( null=False)
    category = models.CharField(max_length=150, null=False, choices=CATEGORY)
    description = models.CharField(max_length=150, null=False)
    tags = models.ManyToManyField(Tag)
    date_created = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.name


class Order(models.Model):   
    STATUS = (('Pending', 'Pending'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered'))
    
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=False)
    status = models.CharField(max_length=150, null=False, choices=STATUS)
    note = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.product.name # To change instace name, like when we type only one order instace, It will return this string. Ex. order = Order.objects.get(id=1) => when we print(order) => ball (product name)
