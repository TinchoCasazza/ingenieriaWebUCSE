# Generated by Django 2.1.1 on 2018-09-28 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0014_carrera'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoPublicacion',
            fields=[
                ('idEstadoPublicacion', models.AutoField(primary_key=True, serialize=False)),
                ('Estado', models.CharField(max_length=30)),
            ],
        ),
        migrations.DeleteModel(
            name='Carrera',
        ),
        migrations.AddField(
            model_name='publicacion',
            name='Estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social.EstadoPublicacion'),
            preserve_default=False,
        ),
    ]
