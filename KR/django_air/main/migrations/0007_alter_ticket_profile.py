# Generated by Django 4.2.7 on 2023-12-16 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_ticket_flights'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profs', to='main.profile', verbose_name='Профиль'),
        ),
    ]
