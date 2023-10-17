from django.forms import ModelForm
from .models import Property, User, Property_Image, Profile_Image
from django import forms
import datetime
from django.forms.widgets import NumberInput
        
#Creates the add property form using the Property model with the borough and postal code not being required
class AddPropertyForm(ModelForm):
    #This is the information about the form with what the field are, labels for it and what form they are in
    class Meta:
        model = Property        
        fields = ['property_name', 'property_cost', 'property_address','property_borough','property_city', 'property_country','property_postal_code','property_type', 'property_accessibility_wheelchair', 'property_accessibility_lift', 'property_furnished', 'property_number_of_rooms', 'property_animal_allowance', 'property_communal_spaces', 'property_information']
        widgets = {
        'property_type': forms.RadioSelect
        }
        labels = {
        'property_name' : 'Property Name',
        'property_cost' : 'Property Cost' ,
        'property_address' : 'Property Address',
        'property_city' : 'Property City',
        'property_country' : 'Property Country',
        'property_number_of_rooms' : 'Property Number Of Rooms',
        'property_type' : 'Type Of Property',
        'property_accessibility_wheelchair' : 'Wheelchair accessible',
        'property_accessibility_lift' : 'Lift avaliable',
        'property_furnished' : 'Furnished Property',
        'property_animal_allowance' : 'Allowed Pets',
        'property_communal_spaces' : 'Shared Kitchen/Bathroom',
        'property_information' : 'Property Extra Information',
        'property_postal_code':'Property Postal Code',
        'property_borough':'Property Borough/County'
        }
        
#Creates the add property form using the Property model with the borough and postal code not being required
class AddPropertyFormAdmin(ModelForm):
    #This is the information about the form with what the field are, labels for it and what form they are in
    class Meta:
        model = Property        
        fields = ['property_name', 'property_cost', 'property_address','property_borough','property_city', 'property_country','property_postal_code','property_type','property_url', 'property_accessibility_wheelchair', 'property_accessibility_lift', 'property_furnished', 'property_number_of_rooms', 'property_animal_allowance', 'property_communal_spaces', 'property_information']
        widgets = {
        'property_type': forms.RadioSelect
        }
        labels = {
        'property_name' : 'Property Name',
        'property_cost' : 'Property Cost' ,
        'property_address' : 'Property Address',
        'property_city' : 'Property City',
        'property_country' : 'Property Country',
        'property_number_of_rooms' : 'Property Number Of Rooms',
        'property_type' : 'Type Of Property',
        'property_accessibility_wheelchair' : 'Wheelchair accessible',
        'property_accessibility_lift' : 'Lift avaliable',
        'property_furnished' : 'Furnished Property',
        'property_animal_allowance' : 'Allowed Pets',
        'property_communal_spaces' : 'Shared Kitchen/Bathroom',
        'property_information' : 'Property Extra Information',
        'property_postal_code':'Property Postal Code',
        'property_borough':'Property Borough/County',
        'property_url' : 'Property URL'
        }        
        
        
#Creates the edut property form using the Property model 
class EditPropertyForm(ModelForm):
    #This is the information about the form with what the field are, labels for it
    class Meta:
        model = Property        
        fields = ['property_name', 'property_cost', 'property_address','property_city','property_borough', 'property_country', 'property_postal_code','property_type', 'property_accessibility_wheelchair', 'property_accessibility_lift', 'property_furnished', 'property_number_of_rooms', 'property_animal_allowance', 'property_communal_spaces', 'property_information']
        labels = {
        'property_name' : 'Property Name',
        'property_cost' : 'Property Cost' ,
        'property_address' : 'Property Address',
        'property_city' : 'Property City',
        'property_country' : 'Property Country',
        'property_number_of_rooms' : 'Property Number Of Rooms',
        'property_type' : 'Type Of Property',
        'property_accessibility_wheelchair' : 'Wheelchair accessible',
        'property_accessibility_lift' : 'Lift avaliable',
        'property_furnished' : 'Furnished Property',
        'property_animal_allowance' : 'Allowed Pets',
        'property_communal_spaces' : 'Shared Kitchen/Bathroom',
        'property_information' : 'Property Extra Information'
        }
        
#Creates the location form using the Property model
class LocationForm(ModelForm):
    #This is the information about the form with what the field are and their form
    class Meta:
        model = Property
        fields = ['property_latitude','property_longitude']
        
        
#Creates the property image form using the Property model  
class PropertyImageForm(ModelForm):
    #This is the information about the form with what the field are and their form
    class Meta:
        model= Property_Image
        fields= ['image_file']
        
        
        
        
#Creates the user sign up form using the User model        
class UserSignUpForm(ModelForm):
    #This is the information about the form with what the field are, labels for it and their form
    class Meta:
        model = User
        fields = ['full_name', 'username','email','password','date_of_birth','phone_number','user_type','location']
        current_time = datetime.datetime.now()
        widgets = {
        'full_name': forms.TextInput(attrs = {'placeholder': 'Full Name'}),
        'username': forms.TextInput(attrs = {'placeholder': 'Username'}),
        'email' : forms.EmailInput(attrs = {'placeholder': '📧 Email'}),
        'password': forms.PasswordInput(attrs = {'placeholder': '🔒 Password'}),
        'date_of_birth' : forms.NumberInput(attrs={'type': 'date'}),
        'phone_number' : forms.TextInput(attrs = {'placeholder': '📱 Phone number'}),
        'user_type' : forms.RadioSelect,
        'location': forms.TextInput(attrs={'placeholder': '🏠 Location'})
        }
        
        labels = {
        'full_name' : 'Full Name',
        'username' : 'Username' ,
        'email' : 'Email',
        'password' : 'Password',
        'date_of_birth' : 'Date Of Birth',
        'phone_number' : 'Phone Number',
        'user_type' : 'Type Of Account',
        'location' : 'Location'
        }
        
#Creates the user login form using the User model  
class UserLoginForm(ModelForm):
    #This is the information about the form with what the field are and their form
    class Meta:
        model = User
        fields = ['email','password']
        widgets = {
        'email' : forms.TextInput(attrs = {'placeholder': '📧 Email'}),
        'password': forms.PasswordInput(attrs = {'placeholder': '🔒 Password'})
        }
        
#Creates the profile picture form using the Profile Image model 
class ProfileImageForm(ModelForm):
    #This is the information about the form with what the field are
    class Meta:
        model= Profile_Image
        fields= ['image_file']


#Creates the user form using the User model         
class UserForm(ModelForm):
    #This is the information about the form with what the field are
    class Meta:
        model = User
        fields = ['full_name', 'username','email','password','date_of_birth','location','phone_number','user_type']


#Creates the edit user form using the User model 
class editUser(ModelForm):
    #This is the information about the form with what the field are and their form
    class Meta:
        model = User
        fields = ['full_name','email','phone_number','location']
        widgets = {
        'email' : forms.EmailInput(attrs = {'placeholder': 'Email'}),
        'location': forms.TextInput(attrs = {'placeholder': 'Location'}),
        'phone_number' : forms.TextInput(attrs = {'placeholder': 'Phone Number'}),
        }
        labels = {
        'email' : 'Email',
        'location' : 'Location',
        'phone_number' : 'Phone Number',
        }
