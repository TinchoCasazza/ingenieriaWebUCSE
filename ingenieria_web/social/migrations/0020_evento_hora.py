# Generated by Django 2.1.3 on 2018-11-09 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0019_auto_20181109_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='Hora',
            field=models.TimeField( null=True, blank=True,default=None),
        ),
    ]
