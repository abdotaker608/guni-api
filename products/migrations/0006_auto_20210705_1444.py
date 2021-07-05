# Generated by Django 3.2.2 on 2021-07-05 14:44

from django.conf import settings
import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0005_auto_20210704_1343'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intent_id', models.CharField(max_length=500)),
                ('total_price', models.FloatField()),
                ('created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PurchasedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.IntegerField(choices=[(0, 'Clothes'), (1, 'Accessories'), (2, 'Cooking Utilities'), (3, 'Electric Appliances'), (4, 'Gaming'), (5, 'Sports')])),
                ('original_price', models.FloatField(verbose_name='original')),
                ('price', models.FloatField()),
                ('image', models.ImageField(upload_to='products')),
                ('description', models.TextField(blank=True, null=True)),
                ('on_sale', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now=True)),
                ('qty', models.IntegerField()),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
            },
            managers=[
                ('manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='original_price',
            field=models.FloatField(verbose_name='original'),
        ),
        migrations.AddIndex(
            model_name='purchasedproduct',
            index=django.contrib.postgres.indexes.GinIndex(fields=['name'], name='products_pu_name_2e2396_gin'),
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='orders', to='products.PurchasedProduct'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
    ]