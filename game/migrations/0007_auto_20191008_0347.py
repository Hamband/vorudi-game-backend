# Generated by Django 2.2.6 on 2019-10-08 03:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('game', '0006_auto_20191007_1631'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='hint',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='team',
            name='current_problem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='game.Problem'),
        ),
    ]
