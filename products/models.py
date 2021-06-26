from django.db import models
from django.contrib.postgres.indexes import GinIndex
from .managers import ProductManager

# Valid product categories
product_categories = (
    (0, 'Clothes'),
    (1, 'Accessories'),
    (2, 'Cooking Utilities'),
    (3, 'Electric Appliances'),
    (4, 'Gaming'),
    (5, 'Sports')
)


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.IntegerField(choices=product_categories)
    original_price = models.FloatField()
    price = models.FloatField()
    image = models.ImageField(upload_to='products')
    description = models.TextField(null=True, blank=True)
    on_sale = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)

    manager = ProductManager()

    class Meta:
        indexes = [
            GinIndex(fields=('name', 'category'))
        ]

    def __str__(self):
        return self.name
