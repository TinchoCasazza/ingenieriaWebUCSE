# Generated by Django 2.1.3 on 2018-11-13 01:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0025_auto_20181112_2035'),
    ]

    operations = [
        migrations.CreateModel(
            name='DenunciaGrupos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Contenido', models.TextField(max_length=150)),
                ('idGrupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social.Grupo')),
                ('idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
