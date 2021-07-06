from django.db import models
from django.contrib.postgres.indexes import GinIndex
from .managers import ProductManager
from authentication.models import User

# Valid product categories
product_categories = (
    (0, 'Clothes'),
    (1, 'Accessories'),
    (2, 'Cooking Utilities'),
    (3, 'Electronics'),
    (4, 'Gaming'),
    (5, 'Sports')
)


class ProductInterface(models.Model):
    name = models.CharField(max_length=100)
    category = models.IntegerField(choices=product_categories)
    original_price = models.FloatField(verbose_name='original')
    price = models.FloatField()
    image = models.ImageField(upload_to='products')
    description = models.TextField(null=True, blank=True)
    on_sale = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)

    manager = ProductManager()

    class Meta:
        abstract = True
        indexes = [
            GinIndex(fields=('name', ))
        ]
        ordering = ('-created', )

    def __str__(self):
        return self.name


class Product(ProductInterface):
    pass


class PurchasedProduct(ProductInterface):
    qty = models.IntegerField()


# Valid order statuses
order_status = (
    (0, 'awaiting'),
    (1, 'delivered')
)


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    intent_id = models.CharField(max_length=500)
    products = models.ManyToManyField(PurchasedProduct, related_name='orders')
    total_price = models.FloatField()
    status = models.IntegerField(choices=order_status, default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ('-created', )
