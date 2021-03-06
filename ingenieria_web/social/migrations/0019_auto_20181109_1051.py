# Generated by Django 2.1.3 on 2018-11-09 13:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0018_auto_20181109_0958'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='idGrupoEvento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='social.Grupo'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='FechaEvento',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
