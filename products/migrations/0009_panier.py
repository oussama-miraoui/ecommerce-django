# Generated by Django 3.1.7 on 2021-05-02 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20210501_1451'),
    ]

    operations = [
        migrations.CreateModel(
            name='Panier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('couleur', models.CharField(max_length=50)),
                ('taille', models.CharField(max_length=40)),
                ('subtotal', models.PositiveIntegerField()),
                ('total', models.PositiveIntegerField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.client')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.produit')),
            ],
        ),
    ]
