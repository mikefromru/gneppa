# Generated by Django 4.2.3 on 2023-11-08 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_level_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level',
            name='description',
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
    ]