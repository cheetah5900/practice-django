# Generated by Django 3.2 on 2022-03-26 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0008_auto_20220327_0255'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Contact',
            new_name='ContactList',
        ),
    ]
