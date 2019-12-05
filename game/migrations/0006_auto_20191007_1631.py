# Generated by Django 2.2.6 on 2019-10-07 16:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('game', '0005_auto_20191006_0056'),
    ]

    operations = [
        migrations.CreateModel(
            name='RewardCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('points', models.IntegerField()),
                ('is_used', models.BooleanField()),
            ],
            options={
                'verbose_name': 'کد جایزه',
                'verbose_name_plural': 'کدهای جایزه',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='hint_point',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='team',
            name='hint',
            field=models.BooleanField(default=False),
        ),
    ]