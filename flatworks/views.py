from .models import *
from django.contrib.auth import get_user_model as um
from django.contrib.auth.models import User as u
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import *
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, CreateView,DetailView
from django.db.models import Q
from django.conf import settings
import geopy.geocoders
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib import messages
from django.db import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError
from django.forms import formset_factory
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import datetime
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.decorators import user_passes_test,login_required
from .filtering import PropertyFilter
import logging
from django.core.exceptions import ValidationError

    
#Allows user to sign up to the site and adds what their information is to the database
def signUp(request):
    form = UserSignUpForm#Creates empty form for the client to fill in
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)#Creates the form with the data sent from client
        if form.is_valid(): #Checks if the form is filled in propertly
            prop_dic = form.cleaned_data
            #Checks if location inputted is valid or if not entered
            geolocator = Nominatim(user_agent="MyApp")
            location_exists = geolocator.geocode(prop_dic['location'])
            if (location_exists != None)|(prop_dic['location'] == "0")|(prop_dic['location']==None) |(prop_dic['location']==""):
                form.save() #Saves the form using the information inputted if it's valid
                um().objects._create_user(request.POST['username'], 
                request.POST['email'],            
                request.POST['password']) #Creates the user and add it to the django inbuild user database too
                iding = User.user_objects.last()
                iding.password = u.objects.last().password #Adds the hashed password to the User model
                iding.link_to_django_user_id=u.objects.last().id #Adds the link to the inbuilt user id to the User model database of that user
                iding.save() #Saves the User model
                messages.success(request, 'Account created, Login')#Sends message to user on login page
                return redirect('log-in')#Goes to login
            else:
                messages.error(request, "Location is not valid, it doesn't exist") #If location doesn't exists then outputs message location not valid
    context = {'form':form} #assigns the form to the form being used for sign up
    return render(request, 'flatworks/signupPage.html', context) #Renders the html page to that url with that form 
       
       
#Allows the user to login with their email and password
def LogIn(request):
    form = UserLoginForm #Assigns empty login form to form
    mod = User #Assigns model user to mod
    if request.method == 'POST': #Checks if the form method is post and if it is does the following
        email = request.POST.get('email') #Gets the email from the client request
        password = request.POST.get('password') #Gets the password from the client request
        try:
            user_check = mod.user_objects.get(email=email) #Checks if the email exists in the User database
            username = user_check.username #Assigns the username gotten from that data if the email exists
            user_authe = authenticate(username=username, password=password) #Then authenticates the account to see if the username and password exists
            password_inputted = check_password(password, user_check.password) #This checks if the hashed password is the same as the password inputted
            if (user_check is not None)&(user_authe is not None)&(password_inputted == True): #If all of these are true then the user gets logged in
                login(request, user_authe)
                find_user_type = int(User.user_objects.get(link_to_django_user_id=request.user.id).user_type) #This checks the user type since landlords can see different html pages than the fdmers and developers
                if (find_user_type == 1) | (find_user_type == 3): 
                    return redirect('filter') #Goes to the url.py filter if consultant or developer
                elif find_user_type == 2:
                    return redirect('see-prop') #Goes to the url.py see-prop if landlord
            else:
                messages.error(request, "Either password wrong or account doesn't exist") #If it doesn't then returns wrong password or account doesn't exist
        except Exception as identifier:
            messages.error(request, "Either password wrong or account doesn't exist") #If there isn't an email or password or username that exists then returns wrong password or account doesn't exist
    context = {'form':form} #This is the variables passed to the html page to use and call
    return render(request, 'flatworks/loginPage.html', context) #Renders the page with the form given and html page
    
    
    
#Allows user to log out
@login_required(login_url='log-in')
def LogOut(request):
    logout(request) #Log out the user
    messages.success(request, "Logged out") #Messages the user they are logged out
    return redirect('log-in') #Redirects them to login 


#This is for filter and results
@login_required(login_url='log-in')
def filtering(request):
    find_user_type = int(User.user_objects.get(link_to_django_user_id=request.user.id).user_type) #Finds the user type
    if (find_user_type == 1) | (find_user_type == 3): #If consultant or developer
        filtered_properties = results(request) #Uses the function results to output the properties filtered
        images = Property_Image.objects.all() #This is all the data in property image table
        
        picture_files = []
        
        #This adds the first photo of each property displayed if it exists to a list
        for each_item in filtered_properties:
            try:  
                picture_files +=[images.filter(property_id__exact = each_item.id)[0]]
            except:
                picture_files = picture_files
        #If post is see profile redirects them to that profile
        if (request.method=="POST") & (request.POST.get('see-profile') != None):
            return redirect('see-oth-prof', pk = request.POST.get('see-profile') )
        #Else if it's just a post request then renders that form with the filters staying the same
        elif request.method == "POST": 
            given_filter = request.POST
            if picture_files==[]:
                context = {'object_list':filtered_properties, 'given_filter':given_filter}#If there are no picture files then only the filtered_properties are given
            else:
                context = {'object_list':filtered_properties, 'given_filter':given_filter,'image':picture_files}
            return render(request, 'flatworks/whole-filter.html', context)#Renders the whole filter html if the user filtered
        if picture_files==[]:
            context = {'object_list':filtered_properties}#If there are no picture files then only the filtered_properties are given
        else:
            context = {'object_list':filtered_properties,'image':picture_files}
        return render(request, 'flatworks/partial-filter.html', context)#Renders the partial filter html if the user hasn't filtered yet
    else:
        return redirect('see-prop') #Can't access filter + results if landlord
        
        
    
#This is for results filtering
@login_required(login_url='log-in')
def results(request):
    find_user_type = int(User.user_objects.get(link_to_django_user_id=request.user.id).user_type)#Finds the user_type
    if (find_user_type == 1) | (find_user_type == 3): #If consultant or developer then does the following
        geolocator = Nominatim(user_agent="MyApp")
        
        #Gets the cost minimum of the filter if it exist otherwise it assign a 0 to it
        try:
            cost_minimum = float(request.POST.get('cost_min'))
        except:
            cost_minimum = 0
        if cost_minimum == None:
            cost_minimum = 0
        
        #Gets the cost maximum of the filter if it exist otherwise it assign a 5000 to it
        try:
            cost_maximum = float(request.POST.get('cost_max'))
        except:
            cost_maximum = 5000
        if cost_minimum == None:
            cost_maximum = 5000
        
        #Gets the location of the filter and True for location given if it exist otherwise it assign a False for location given
        location = request.POST.get('location')
        if (location == None):
            location_given = False
        else:
            try:
                location = request.POST.get('location')
                geolocator = Nominatim(user_agent="MyApp")
                latitude = geolocator.geocode(location).latitude
                longitude = geolocator.geocode(location).longitude
                location = (latitude,longitude)
                location_given = True
            except: 
                location_given = False
                    
        #Gets the distance of the filter otherwise it assigns 5 to the distance            
        try:
            distance = int(request.POST.get('distance'))
        except: 
            distance = 5
        if distance == None:
            distance = 5
            

        #Gets if the property is wheelchair accessible otherwise it assigns [None,0,1] to it        
        try:
            wheelchair = [int(request.POST.get('wheelchair'))]
        except :
            wheelchair = [None, 0,1]
        if wheelchair == [None]:
            wheelchair = [None, 0,1]
            
        #Gets if the property has a lift otherwise it assigns [None,0,1] to it 
        try:
            lift = [int(request.POST.get('lift'))]
        except :
            lift = [None, 0,1]
        if lift == [None]:
            lift = [None, 0,1]
          
        #Gets if it is a house otherwise it assigns 1 to it 
        try:
            type_house = int(request.POST.get('house'))
        except :
            type_house = 1
        if type_house == None:
            type_house = 1
           
        #Gets if it is a flat otherwise it assigns 2 to it 
        try:
            type_flat = int(request.POST.get('flat'))
        except :
            type_flat = 2
        if type_flat == None:
            type_flat = 2
            
        #Gets if it is a studio otherwise it assigns 3 to it 
        try:
            type_studio = int(request.POST.get('studio'))
        except :
            type_studio = 3
        if type_studio == None:
            type_studio = 3

        #Gets if the property is furnished otherwise it assigns [None,0,1] to it
        try :
            furnished = [int(request.POST.get('furnished'))]
        except:
            furnished = [None,0,1]
        if furnished == [None]:
            furnished = [None,0,1]
            
        #Gets the minimum amount of rooms otherwise it assigns 0 to it
        try:
            min_num_rooms = int(request.POST.get('min_noofrooms'))
        except:
            min_num_rooms = 0
        if cost_minimum == None:
            min_num_rooms = 0
            
        #Gets the maximum amount of rooms otherwise it assigns 100 to it
        try:
            max_num_rooms = int(request.POST.get('max_noofrooms'))
        except:
            max_num_rooms = 100
        if cost_minimum == None:
            max_num_rooms = 100
            
        #Gets if the property allows animals otherwise it assigns [None,0,1] to it    
        try:
            animal_allowance = [int(request.POST.get('animalallowance'))]
        except:
            animal_allowance = [None,0,1]
        if animal_allowance == [None]:
            animal_allowance = [None,0,1]
           
        #Gets if the property shares bathrooms/kitchens otherwise it assigns [None,0,1] to it
        try:
            communal_spaces = [int(request.POST.get('communalspaces'))] 
        except:
            communal_spaces = [None,0,1]
        if communal_spaces == [None]:
            communal_spaces = [None,0,1]
        
        #Filters the Property based on the variables previously assigned and checks them against what the property data already has
        mostly_filtered = Property.objects.filter(
            Q(property_type__exact = type_studio)|Q(property_type__exact = type_house)|Q(property_type__exact = type_flat),
            property_cost__gte = cost_minimum,
            property_cost__lte = cost_maximum,
            property_accessibility_wheelchair__in = wheelchair,
            property_accessibility_lift__in = lift,
            property_furnished__in = furnished,
            property_number_of_rooms__gte = min_num_rooms,
            property_number_of_rooms__lte = max_num_rooms,
            property_animal_allowance__in = animal_allowance,
            property_communal_spaces__in= communal_spaces,
            )
        
        #If there is a location given then for each Property in mostly_filtered checks where that location is then measures the distance between the location and the one in property and if it's less or equal to the distance given then adds it to the filtered list, once it's finished returns the filtered list
        if location_given == True:    
            filtered = []
            amount = len(mostly_filtered)
            for each_data in range(amount):
                if (geodesic(location,(mostly_filtered[each_data].property_latitude,mostly_filtered[each_data].property_longitude)).km<= distance):
                    filtered.append(mostly_filtered[each_data])
            return filtered  
                
        #If location is not given returns the mostly filtered list
        else:
            return mostly_filtered
    else:
        return redirect('see-prop') #Redirects it to see prop if a landlord
        
#This adds a property to that user 
@login_required(login_url='log-in')
def addProperty(request):
    find_user_type = int(User.user_objects.get(link_to_django_user_id=request.user.id).user_type) #Checks user type
    if (find_user_type == 1) | (find_user_type == 2): #This is for if it's a landlord or consultant
        form = AddPropertyForm
    elif find_user_type == 3: #This is for developer so they can add a url
        form = AddPropertyFormAdmin
        
    image_form = PropertyImageForm() #This is for image form creation
    if request.method == 'POST':
        if (find_user_type == 1) | (find_user_type == 2):
            form = AddPropertyForm(request.POST)#This inputs the property post information based on the fields for landlords and users
        elif find_user_type == 3:
            form = AddPropertyFormAdmin(request.POST)#This inputs the property post information admin based on the fields for developers
            
        image_form = PropertyImageForm(request.POST,request.FILES)#This inputs the property post and file information in the image form based on the fields
        
        if form.is_valid(): #If the information is valid then 
            prop_dic = form.cleaned_data
            geolocator = Nominatim(user_agent="MyApp")
            location_exists = geolocator.geocode(prop_dic['property_address']+', '+ prop_dic['property_borough']+', '+ prop_dic['property_city']+', '+ prop_dic['property_country']) #This checks if the location exists by inputting it into the geolocator and checking if it exist
            
            #If location does exist then saves the form with the property_user_id being what the current user's id is
            if (location_exists != None):
                form = form.save(commit=False)
                form.property_user_id = User.user_objects.get(link_to_django_user_id=request.user.id).id
                form.save()
                #If there is files uploaded the saves the image
                if request.FILES != {}:
                    if image_form.is_valid():
                        image_form = image_form.save(commit=False)
                        image_form.property_id = form.id #Adds the image's property id to the id of the property
                        image_form.save()#This saves the new image if it exists
                #This assigns the property latitude and longitude of the property
                prop = Property.objects.latest('id')
                geolocator = Nominatim(user_agent="MyApp")
                prop.property_latitude = geolocator.geocode(prop.property_address +', '+ prop.property_city +', '+ prop.property_country).latitude
                prop.property_longitude = geolocator.geocode(prop.property_address +', '+ prop.property_city +', '+ prop.property_borough +', '+ prop.property_country).longitude
                prop.save()
                return redirect('filter')
            else: 
                messages.error(request, "Location is not valid, it doesn't exist")#If the location doesn't exist then output location is not valid
    
    
    if (find_user_type == 1) | (find_user_type == 3):
        context = {'form':form,'image_form':image_form}
        return render(request, 'flatworks/add-property.html', context)#This renders the add property html page with the form and image_form and request for consultants and developers
    elif find_user_type == 2:
        context = {'form':form,'image_form':image_form}
        return render(request, 'flatworks/landlord-add-property.html', context)#This renders the add property html page with the form and image_form and request for landlords
    
    
    
    
#This is for seeing the properties owned by that user
@login_required(login_url='log-in')    
def seeProperties(request):
    user_id = User.user_objects.get(link_to_django_user_id=request.user.id) #This find the user id
    form = Property.objects.filter(property_user_id__exact =user_id) #This finds the property objects owned by that user
    picture_files = []
    images = Property_Image.objects.all() #This is all the data from property image table
    #This filters the images based on the property ids and if they exist takes the first one 
    for each_item in form:
        try:
            picture_files += [images.filter(property_id__exact =each_item.id)[0]]
        except: 
            picture_files = picture_files
    #If the client submits something then this happens
    if request.method == 'POST':
        try:
            if request.POST['delete'] != None:
                pk = int(request.POST['delete'])
                try:
                    #If property image exists and there is an id based on the post delete value and deletes the property image
                    property_data_image_data = Property_Image.objects.get(property_id=pk) #This gets the property image data
                    property_data_image_data.image_file.delete() #This deletes the image file on the server
                    property_data_image_data.delete() #This deletes the property image data in the table
                except:
                    None
                deleteProperty(request) #This deletes the property if they picked delete property
                return redirect('see-prop') #This reloads the page without the request
        except: 
            edit_val = request.POST['edit'] #This edits the property if they picked edit property
            if edit_val != None:
                return redirect(editProperty, pk = edit_val) #This redirects the page with the second argument being the id of the property
            return redirect('see-prop') #This reloads the page without the request
    if picture_files==[]:
        context = {'form':form} #Passes just form onto html if there are no picture files
    else:
        context = {'form':form, 'image':picture_files } #Passes both picture_files and form if there are picture files
    find_user_type = int(User.user_objects.get(link_to_django_user_id=request.user.id).user_type)
    if (find_user_type == 1) | (find_user_type == 3):
        return render(request, 'flatworks/see-properties.html', context)#This renders the see properties html page for developers and consultants 
    elif find_user_type == 2:
        return render(request, 'flatworks/landlord-see-properties.html', context)#This renders the see properties html page for landlords
        
    
#This deletes the property    
@login_required(login_url='log-in')
def deleteProperty(request):
    #If property exists and there is an id based on the post delete value and deletes the property 
    try:
        pk = int(request.POST['delete']) #Gets the property id
        property_data = Property.objects.get(id=pk) #Finds the property data with that id
        property_data.delete() #Deletes property data
    except:
        return redirect('see-prop') 
    return
        
 
#The edit the property based on the given request and id 
@login_required(login_url='log-in')
def editProperty(request,pk):
    try:
        property_id = Property.objects.get(id=pk)#Gets the property id from the argument
        form = EditPropertyForm(instance=property_id) #Uses the form to output the values from the data
        try:
            image_file = Property_Image.objects.get(property_id=pk) #If there is a property image then passes it into the html
            context = {'form':form, 'image': image_file}
        except:
            image_file = PropertyImageForm #If there isn't already an image then allows a user to upload one
            context = {'form':form, 'image_form': image_file}     
            
        if (request.method == "POST")& (request.POST.get('delete') != None):
            deletePropertyImage(request) #If the user want to delete the image this goes to that function to delete it
            return redirect('edit-prop',pk=pk) #This directs it to the edit page again once deleted
        elif request.method == "POST":
            form = EditPropertyForm(request.POST, instance=property_id)#This changes the form based on the new values
            image_form = PropertyImageForm(request.POST,request.FILES)#This changes the form based on the new values too
            #Checks if the form and location is valid then saves the form
            if form.is_valid():
                prop_dic = form.cleaned_data
                geolocator = Nominatim(user_agent="MyApp")
                #This checks if the location exists
                location_exists = geolocator.geocode(prop_dic['property_address']+', '+ prop_dic['property_borough']+', '+ prop_dic['property_city']+', '+ prop_dic['property_country'])
                if (location_exists != None):
                    form.save() #Saves the form onto the table for property
                    #Saves the image if there is one 
                    if (image_form.is_valid())&(request.FILES != {}):
                        image_form = image_form.save(commit=False)
                        image_form.property_id = property_id.id #Adds the image's property id to the id of the property
                        image_form.save()#This saves the new image if it exists
                    #Adds the new latitude and longitude to the data from the location updated
                    prop = Property.objects.last()
                    prop.property_latitude = geolocator.geocode(prop.property_address +', '+ prop.property_borough  +', '+ prop.property_city+', '+ prop.property_country).latitude
                    prop.property_longitude = geolocator.geocode(prop.property_address +', '+ prop.property_borough +', '+ prop.property_city +', '+ prop.property_country).longitude
                    prop.save()
                    return redirect('see-prop') #Redirects it to the see properties page once finished
                else:
                    messages.error(request, "Location is not valid, it doesn't exist") #If location doesn't exists then outputs message location not valid
                return redirect('edit-prop',pk=pk) #This reloads the page without the request
        
        find_user_type = int(User.user_objects.get(link_to_django_user_id=request.user.id).user_type)
        if (find_user_type == 1) | (find_user_type == 3):
            return render(request, 'flatworks/edit-property.html', context) #Renders the edit properties page with the form and image files if the user is a developer or consultant
        elif find_user_type == 2:
            return render(request, 'flatworks/landlord-edit-property.html', context) #Renders the edit properties page with the form and image files if the user is a landlord
    except ObjectDoesNotExist:
        return redirect('see-prop') #If the edit doesn't exist then redirects it to the see properties page
    
#This deletes the property image with 
@login_required(login_url='log-in')     
def deletePropertyImage(request):
    try:
        #If property image exists and there is an id based on the post delete value and deletes the property image
        pk = request.POST['delete'] #This get's the id of the image from client side
        property_data = Property_Image.objects.get(id=pk) #This gets the property image data
        property_data.image_file.delete() #This deletes the image file on the server
        property_data.delete() #This deletes the property image data in the table
    except:
        return redirect('see-prop') #Redirect to see properties in url 
 
 
 
 
#This sees the user's own profile
@login_required(login_url='log-in')
def seeProfile(request):
    form = User.user_objects.get(link_to_django_user_id=request.user.id) #This gets the user's data
    try: 
        other = Profile_Image.objects.get(user_id=form.id) #This sets other to the profile image if it exists
    except:
        other = None
    if request.method == 'POST':
        try:
            if request.POST['delete'] != None: 
                pk = int(request.POST['delete']) #Get the id of the profile picture
                try:
                    profile_data = Profile_Image.objects.get(user_id=pk) #Find the profile picture by id
                    profile_data.image_file.delete() #Deletes the image file from the media 
                    profile_data.delete() #Deletes the image from profile picture table
                except:
                    None
                deleteProfile(request) #This deletes the profile if they picked delete profile
                return redirect('log-in') #Redirects to login
        except:
            None
        try:
            edit_val = request.POST['edit'] #This edits the profile if they picked edit profile
            if edit_val != None:
                return redirect(editProfile, pk = edit_val) #This redirects the page with the second argument being the id of the profile
            return redirect('see-prof') #Redirects to see profile
        except:
            None
        return redirect('see-prof') #Redirects to see profile
    context = {'form':form, 'image':other } #This passes the user's data and image to the client
    find_user_type = int(User.user_objects.get(link_to_django_user_id=request.user.id).user_type) #This get's the user type
    if (find_user_type == 1) | (find_user_type == 3):
        return render(request, 'flatworks/see-profile.html', context) #Renders see profile html if the user is a developer or consultant
    elif find_user_type == 2:
        return render(request, 'flatworks/landlord-see-profile.html', context) #Renders landlord see profile html if user is a landlord
        
        
#This allows user to see other's profile     
@login_required(login_url='log-in')
def seeOthersProfile(request, pk):
    find_user_type = int(User.user_objects.get(link_to_django_user_id=request.user.id).user_type) #This checks user type
    if (find_user_type == 1) | (find_user_type == 3): #If the user is a developer or consultant they can do the following
        check = User.user_objects.get(link_to_django_user_id=request.user.id) #This gets the user's id
        form = User.user_objects.get(id=pk) #This get's the user of the argument
        if (check == form): 
            return redirect('see-prof') #If they are the same user, the client get's redirected to see their own profile
        print(check.id)
        blocked_users = Blocked_Users.objects.filter(user_id__exact=check.id) #This checks if the client is blocked by that user, if they are can't get to the user's profile
        for each_blocked_user in blocked_users:
            print(each_blocked_user)
            if(form.id==each_blocked_user.blocked_user_id):
                return redirect('filter')
        try: 
            other = Profile_Image.objects.get(user_id=form.id) #If an image exists then assigns it to other
        except:
            other = None
        try:
            #If the user blocked the profile then the blocked user data is created to the table of blocked users
            if (request.method == "POST")&(request.POST['block'] != None):
                new_user = Blocked_Users.objects.create(user_id = request.POST['block'],blocked_user_id = check.id)
                return redirect('filter') #Redirected to filter
                
        except:
            None
        
        try:
            #If the user is reported then send an email to the developers of the app
            if (request.method == "POST")&(request.POST['report'] != None):
                send_mail(subject='User reported', message = 'The user blocked is '+str(form),from_email = settings.EMAIL_HOST_USER, recipient_list=['ec20323@qmul.ac.uk']) 
                return redirect('filter') #Redirected to filter
        except:
            None
            
        context = {'form':form, 'image':other } #This passes the other and form onto the client
        return render(request, 'flatworks/see-others-profile.html', context)

@login_required(login_url='log-in')
def deleteProfile(request):
    try:
        pk = request.POST['delete'] #Get the id of the profile
        profile_data = User.user_objects.get(id=pk) #Find the profile by id
        dj_profile_data = u.objects.get(id = profile_data.link_to_django_user_id) #Find the user in the django inbuilt database 
        profile_data.delete() #Deletes the user from User table
        dj_profile_data.delete() #Deletes the user from Django user database
    except:
        return redirect('see-prof') #Redirects to see profile
    return

@login_required(login_url='log-in')
def deleteProfileImage(request):
    try:
        pk = request.POST['delete'] #Get the id of the profile picture
        profile_data = Profile_Image.objects.get(id=pk) #Find the profile picture by id
        profile_data.image_file.delete() #Deletes the image file from the media 
        profile_data.delete() #Deletes the image from profile picture table
    except:
        return redirect('see-prof') #Redirects to see profile

@login_required(login_url='log-in')
def editProfile(request,pk):
    try:
        use_id = User.user_objects.get(id=pk) #Get the user data from id
        form = editUser(instance=use_id) #Get the form with that user data inputted
        try:
            image_file = Profile_Image.objects.get(user_id=pk) #Get profile image if it exists
            context = {'form':form, 'image': image_file}
        except:
            image_file = ProfileImageForm #Get profile image form if profile doesn't exist
            context = {'form':form, 'image_form': image_file}
        
        if (request.method == "POST")& (request.POST.get('delete') != None):
            deleteProfileImage(request) #Delete profile image
            return redirect('edit-prof',pk=pk) #Redirect to edit profile
        elif request.method == "POST":
            form = editUser(request.POST, instance=use_id) #Make a form with the new user data inputted
            image_form = ProfileImageForm(request.POST,request.FILES) #Make a image form with the files uploaded
            if form.is_valid():
                prop_dic = form.cleaned_data
                geolocator = Nominatim(user_agent="MyApp")
                #Checks if new location exists and if it does or there is no location inputted then saves the form and image_form 
                location_exists = geolocator.geocode(prop_dic['location'])
                if (location_exists != None)|(prop_dic['location'] == "0")|(prop_dic['location']==None) |(prop_dic['location']==""):
                    form.save()
                    #This saves the new image if it exists to the table
                    if (image_form.is_valid())&(request.FILES != {}):
                        image_form = image_form.save(commit=False)
                        image_form.user_id = use_id.id
                        image_form.save()
                    #This saves the email to the django inbuilt database
                    saving = u.objects.get(id=use_id.link_to_django_user_id)
                    saving.email = prop_dic['email']
                    saving.save()
                    return redirect('see-prof') #The user gets redirected to see profile
                else:
                    messages.error(request, "Location is not valid, it doesn't exist") #If location doesn't exists then outputs message location not valid
        find_user_type = int(User.user_objects.get(link_to_django_user_id=request.user.id).user_type)
        if (find_user_type == 1) | (find_user_type == 3):
            return render(request, 'flatworks/edit-profile.html', context) #Renders the edit profile html if developer or consultant
        elif find_user_type == 2:
            return render(request, 'flatworks/landlord-edit-profile.html', context) #Renders the landlord edit profile html if landlord
    except ObjectDoesNotExist:
        return redirect('see-prof')
