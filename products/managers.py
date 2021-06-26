from django.db.models import Manager


class ProductManager(Manager):

    def hot_items(self, limit=10):
        queryset = self.order_by('on_sale', 'created')[:limit]
        return queryset
