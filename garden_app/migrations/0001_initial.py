# Generated by Django 4.1.2 on 2022-10-20 07:29

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlanOfWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateField(auto_now=True)),
                ('date', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('species', models.CharField(blank=True, max_length=60, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('amount', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='PlantType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('description', models.TextField(blank=True, null=True)),
                ('plan', models.ManyToManyField(blank=True, to='garden_app.planofwork')),
                ('plant', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='garden_app.plant')),
            ],
        ),
        migrations.AddField(
            model_name='plant',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garden_app.planttype'),
        ),
        migrations.AddField(
            model_name='plant',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garden_app.unit'),
        ),
    ]
