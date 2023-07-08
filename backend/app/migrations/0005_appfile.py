# Generated by Django 3.2 on 2022-07-19 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_delete_appfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('file', models.FileField(blank=True, null=True, upload_to='app_files/')),
                ('counter', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
