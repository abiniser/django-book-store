# Generated by Django 5.1.3 on 2024-11-22 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='pdf_file',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
