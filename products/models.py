from django.db import models
from django.contrib.postgres.indexes import GinIndex

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
    category = models.CharField(max_length=100, choices=product_categories)
    price = models.FloatField()
    image = models.ImageField(upload_to='products')
    description = models.TextField(null=True, blank=True)
    on_sale = models.BooleanField(default=False)

    class Meta:
        indexes = [
            GinIndex(fields=('name', 'category'))
        ]

    def __str__(self):
        return self.name
