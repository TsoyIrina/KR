# Generated by Django 4.2.7 on 2023-12-16 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_ticket_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, null=True, verbose_name='Цена'),
        ),
    ]
