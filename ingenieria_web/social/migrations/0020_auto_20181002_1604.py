# Generated by Django 2.1.1 on 2018-10-02 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0019_auto_20181002_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicacion',
            name='Estado_id',
        ),
        migrations.AddField(
            model_name='publicacion',
            name='Estado',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='social.EstadoPublicacion'),
        ),
        migrations.AlterField(
            model_name='estadopublicacion',
            name='NombreEstado',
            field=models.CharField(default=None, max_length=30),
        ),
    ]
