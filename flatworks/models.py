from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from .validators import validate_birth,validate_cost
from django.contrib.auth.models import User

#This creates a model called user to create a table on the database for users
#max_length means the maximum amount of characters that can be entered
#unique means the characters entered can't be the same as the previous data
#choices means those choices are only allowed and those choices are assigned to the value in the inside brackets
#blank means it is not required
#validators call upon the validator.py file to check if the value inputted in valid
#null means it can be no value
#on_delete cascade allows the child data to be deleted when the parent data so what is connected to that foreign key is deleted then the data itself is deleted
class User(models.Model):
    username = models.CharField(max_length = 15,unique=True) #Username
    password = models.CharField(max_length = 20) #Password
    user_type = models.IntegerField(choices=((1,'Consultant'),(2,'Landlord'))) #User type, 1 for consultant, 2 for landlord, 3 for developer
    full_name = models.CharField(max_length=30) #Full name
    date_of_birth = models.DateField(validators=[validate_birth]) #Date of birth, has to be between 1940 to today
    email = models.EmailField(unique=True) #Email
    phone_number = PhoneNumberField("INTERNATIONAL",null=True,unique=True,blank=True) #Phone number, different for each user and can be any international number
    link_to_django_user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)#Link to the in-built django user
    location = models.CharField(max_length=30,blank=True) #Location
    #When use str version of the model then returns the id, username, user type, full name and email 
    def __str__(self):
        return str(self.id) + ", " + self.username + ", " + str(self.user_type) + ", " + self.full_name + ", " + self.email
        
    #Makes user_object the manager of the model instead of objects
    user_objects= models.Manager()
    
    #Returns the id of the user
    def user_id(self):
        return self.id
        
#This creates a model called property to create a table on the database for properties  
#max_digits means the maximum amount of digits allowed to be entered including the decimal place
#decimal_places means the amount of decimals a number can have 
#default means that if no value is inputted then it will be 0 by default 
class Property(models.Model):
    property_name = models.CharField(max_length=100) #Name of property
    property_cost = models.DecimalField(max_digits=8, decimal_places=2) #Cost of property
    property_address = models.CharField(max_length=200, unique=True) #Address of property
    property_city = models.CharField(max_length=40) #City of property
    property_borough = models.CharField(max_length=40, blank=True) #Borough of property
    property_country = models.CharField(max_length=40) #Country of property
    property_postal_code = models.CharField(max_length=15, blank=True) #Postal Code of property
    property_url = models.URLField(null=True, unique=True) #URL of property
    property_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)#Properties the user owns, this is many to one so the user can have many properties
    property_type = models.IntegerField(choices=((1,'House'),(2,'Flat'),(3,'Studio'))) #Property type, 1 for house, 2 for flat, 3 for studio, 4 for business room
    property_accessibility_wheelchair = models.BooleanField() #Accessible to wheelchairs
    property_accessibility_lift = models.BooleanField() #Has a lift
    property_furnished = models.BooleanField() #Furnished
    property_number_of_rooms = models.IntegerField() #Number of rooms
    property_animal_allowance = models.BooleanField() #Allowed animals
    property_communal_spaces = models.BooleanField() #Sharing space or not
    property_information = models.TextField(blank=True) #Property information
    property_latitude = models.FloatField(default = 0) #For latitude, of the location
    property_longitude = models.FloatField(default = 0) #For longitude, of the location
    
    #When use str version of the model then returns the property: id, name, cost, address, postal_code and country
    def __str__(self):
        return str(self.id) + ", " + self.property_name + ", " + str(self.property_cost) + ", " + self.property_address + ", " + self.property_postal_code + ", " + self.property_country
    
    #Returns the id of the property
    def property_id(self):
        return self.id

#This creates a model called property_image to create a table on the database for images of the properties
class Property_Image(models.Model):
    property = models.OneToOneField(Property,on_delete=models.CASCADE,null=True) #Picture belongs to a property
    image_file= models.ImageField(upload_to='images/properties_imgs/', null=True, verbose_name="",blank=True) #Image file itself
    
    
    #When use str version of the model then returns the property image: file url
    def __str__(self):
        return str(self.image_file.url)
      

    #Returns property image id
    def property_image_id(self):
        return self.id
    

#This creates a model called profile_Image to create a table on the database for  images for the profile
class Profile_Image(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)#Picture belongs to a user
    image_file= models.ImageField(upload_to='images/user_imgs/', null=True, verbose_name="",blank=True)#Image file itself
    
    #When use str version of the model then returns the profile image: file url
    def __str__(self):
        return str(self.image_file.url)
        
    #Returns profile image id
    def profile_image_id(self):
        return self.id
        
#This creates a model for blocked users so users can blocks others to not be able to see their profile
class Blocked_Users(models.Model):
    user = models.ForeignKey(User, related_name='blocked_by', verbose_name="User Blocked By",on_delete=models.CASCADE)#The user that blocks it
    blocked_user = models.ForeignKey(User, related_name='blocked_user', verbose_name="User Blocked",on_delete=models.CASCADE)#The user blocked
        
