from django.db import models
from .db_connection import db
product_collection = db['Product']

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name
