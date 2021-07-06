# Generated by Django 3.2.2 on 2021-07-06 15:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0008_alter_order_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.IntegerField(choices=[(0, 'Clothes'), (1, 'Accessories'), (2, 'Cooking Utilities'), (3, 'Electronics'), (4, 'Gaming'), (5, 'Sports')]),
        ),
        migrations.AlterField(
            model_name='purchasedproduct',
            name='category',
            field=models.IntegerField(choices=[(0, 'Clothes'), (1, 'Accessories'), (2, 'Cooking Utilities'), (3, 'Electronics'), (4, 'Gaming'), (5, 'Sports')]),
        ),
    ]