from django.core.exceptions import ValidationError
import datetime
from geopy.geocoders import Nominatim
import logging

#This is for validating an email if it goes to production to check if a consultant works for FDM by checking if they have a valid email
def validate_flatworks_email(value):
    if not "flatworks.ac.uk" in value:
        raise ValidationError("A valid flatworks email must be entered in")
    else:
        return value
        
#This is for checking if the user has a valid birthday between 1940 to today
def validate_birth(date):
    d1 = datetime.date.today()
    d2 = datetime.date(1940,1,1)
    if date >= d2 and date <= d1:
        return date
    else: 
        raise ValidationError("Not valid date of birth")

#This is for checking if the property is between 0 to 5000 cost 
def validate_cost(cost):
    if cost>=5000:
        raise ValidationError("Too high cost")
    elif cost<=0:
        raise ValidationError("Too little cost")
    else:
        return cost

#This for checking if a location is valid
def validate_location(location):
    try:
        geolocator = Nominatim(user_agent="MyApp")
        location_exists = geolocator.geocode(location)
    except:
        return ValidationError("Not found")
    if location_exists == None:
        return ValidationError("Not found")
    else:
        return location
