# Generated by Django 2.1.1 on 2018-10-02 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0020_auto_20181002_1604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicacion',
            name='Estado',
        ),
        migrations.AddField(
            model_name='publicacion',
            name='Borrador',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='publicacion',
            name='Eliminado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='publicacion',
            name='Publicado',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='EstadoPublicacion',
        ),
    ]
