# Generated by Django 4.2.2 on 2023-06-27 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webV', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='topprovincerate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=50)),
                ('province', models.CharField(max_length=50)),
                ('applicants', models.CharField(max_length=50)),
                ('enrollment', models.CharField(max_length=50)),
                ('rate', models.CharField(max_length=50)),
            ],
        ),
    ]
