# Generated by Django 3.2 on 2022-04-05 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0016_auto_20220401_2046'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrudUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=30)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('age', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]