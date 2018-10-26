# Generated by Django 2.1.2 on 2018-10-26 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0014_auto_20181026_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicacion',
            name='Destacar',
            field=models.CharField(choices=[('Destacado', 'Destacado'), ('NoDestacado', 'No destacado')], default='Publicado', max_length=15),
        ),
        migrations.AlterField(
            model_name='publicacion',
            name='Estado',
            field=models.CharField(choices=[('Publicado', 'Publicado'), ('Eliminado', 'Eliminado'), ('Borrador', 'Borrador')], default='Publicado', max_length=15),
        ),
    ]
