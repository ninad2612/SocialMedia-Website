# Generated by Django 5.1.2 on 2024-11-02 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='profile_pictures'),
        ),
    ]
