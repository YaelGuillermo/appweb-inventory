# Generated by Django 5.0.2 on 2024-10-05 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_alter_categorymodel_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorymodel',
            name='name',
            field=models.CharField(max_length=64, unique=True, verbose_name='nombre'),
        ),
    ]
