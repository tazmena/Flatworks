# Generated by Django 4.0.3 on 2022-03-28 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flatworks', '0018_remove_profile_image_name_remove_property_image_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
    ]