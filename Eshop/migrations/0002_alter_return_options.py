# Generated by Django 4.1.3 on 2022-11-29 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Eshop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='return',
            options={'ordering': ['date_return'], 'verbose_name': 'return', 'verbose_name_plural': 'returns'},
        ),
    ]
