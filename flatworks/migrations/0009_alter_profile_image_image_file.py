# Generated by Django 4.0.3 on 2022-03-25 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatworks', '0008_alter_profile_image_image_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile_image',
            name='image_file',
            field=models.FileField(null=True, upload_to='images/user_imgs/', verbose_name=''),
        ),
    ]