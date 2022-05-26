# Generated by Django 3.0.3 on 2020-03-11 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=3)),
                ('name', models.CharField(max_length=60)),
                ('year', models.IntegerField()),
                ('semester', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=60, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rate_professors.Module')),
                ('professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rate_professors.Professor')),
            ],
        ),
        migrations.AddField(
            model_name='module',
            name='professor',
            field=models.ManyToManyField(to='rate_professors.Professor'),
        ),
    ]