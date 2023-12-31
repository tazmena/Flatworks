# Generated by Django 4.0.3 on 2022-03-24 06:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import flatworks.validators
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_name', models.CharField(max_length=100)),
                ('property_cost', models.DecimalField(decimal_places=2, max_digits=8)),
                ('property_address', models.CharField(max_length=200, unique=True)),
                ('property_city', models.CharField(max_length=40)),
                ('property_borough', models.CharField(max_length=40, null=True)),
                ('property_country', models.CharField(max_length=40)),
                ('property_postal_code', models.CharField(max_length=15)),
                ('property_url', models.URLField(null=True, unique=True)),
                ('property_type', models.IntegerField(choices=[(1, 'House'), (2, 'Flat'), (3, 'Studio')])),
                ('property_accessibility_wheelchair', models.BooleanField(null=True)),
                ('property_accessibility_lift', models.BooleanField(null=True)),
                ('property_furnished', models.BooleanField(null=True)),
                ('property_number_of_rooms', models.IntegerField(null=True)),
                ('property_animal_allowance', models.BooleanField(null=True)),
                ('property_communal_spaces', models.BooleanField(null=True)),
                ('property_latitude', models.FloatField(default=0)),
                ('property_longitude', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=15, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('user_type', models.IntegerField(choices=[(1, 'Consultant'), (2, 'Landlord')])),
                ('full_name', models.CharField(max_length=30)),
                ('date_of_birth', models.DateField(validators=[flatworks.validators.validate_birth])),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, unique=True, verbose_name='INTERNATIONAL')),
                ('link_to_django_user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            managers=[
                ('user_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Property_Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('image_file', models.ImageField(null=True, upload_to='images/properties_imgs/', verbose_name='')),
                ('property', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='flatworks.property')),
            ],
        ),
        migrations.AddField(
            model_name='property',
            name='property_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='flatworks.user'),
        ),
        migrations.CreateModel(
            name='Profile_Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('image_file', models.ImageField(null=True, upload_to='images/user_imgs/', verbose_name='')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='flatworks.user')),
            ],
        ),
    ]
