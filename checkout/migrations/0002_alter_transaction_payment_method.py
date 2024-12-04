# Generated by Django 5.1.3 on 2024-12-01 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='payment_method',
            field=models.IntegerField(choices=[(1, 'Stripe'), (2, 'Paypal')]),
        ),
    ]
