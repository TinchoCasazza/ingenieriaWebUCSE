# Generated by Django 2.1.1 on 2018-10-02 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0021_auto_20181002_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicacion',
            name='Borrador',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='Eliminado',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='Publicado',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
