# Generated by Django 3.2 on 2022-03-26 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0007_auto_20220327_0254'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='cost',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
