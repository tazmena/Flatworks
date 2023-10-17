# Generated by Django 4.0.3 on 2022-03-27 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatworks', '0016_alter_profile_image_image_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile_image',
            name='image_file',
            field=models.FileField(blank=True, null=True, upload_to='images/user_imgs/', verbose_name=''),
        ),
        migrations.AlterField(
            model_name='property_image',
            name='image_file',
            field=models.FileField(blank=True, null=True, upload_to='images/properties_imgs/', verbose_name=''),
        ),
    ]
