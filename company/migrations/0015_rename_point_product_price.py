# Generated by Django 3.2 on 2022-04-01 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0014_auto_20220331_2134'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='point',
            new_name='price',
        ),
    ]