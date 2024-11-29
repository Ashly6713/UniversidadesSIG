# Generated by Django 5.1.1 on 2024-11-12 00:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0005_carrera_duracion'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='carrera',
            name='calificacion_promedio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='facultad',
            name='calificacion_promedio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='point',
            name='calificacion_promedio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.AddField(
            model_name='universidad',
            name='calificacion_promedio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True),
        ),
        migrations.CreateModel(
            name='Calificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calificacion', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=1)),
                ('carrera', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='geodata.carrera')),
                ('facultad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='geodata.facultad')),
                ('universidad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='geodata.universidad')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('usuario', 'universidad', 'facultad', 'carrera')},
            },
        ),
    ]
