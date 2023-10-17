from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

#This creates the url pattern of where the site goes to, in the format of the name of the url after domain name/ip address, then what the code is in views then the name of the url 
urlpatterns = [
    path('', views.LogIn, name = 'log-in'),
    path('signup/', views.signUp, name = 'sign-up'),
    path('logout/', views.LogOut, name ='log-out'),
    path('filter/', views.filtering, name='filter'),
    path('add-property/', views.addProperty, name="add-prop"),
    path('see-properties/', views.seeProperties, name="see-prop"),
    path('edit-property/<int:pk>',views.editProperty , name="edit-prop"),
    path('see-profile/', views.seeProfile, name="see-prof"),
    path('edit-profile/<int:pk>', views.editProfile, name="edit-prof"),
    path('see-others-profile/<int:pk>', views.seeOthersProfile, name="see-oth-prof")
    ] 
    
#This allows images to be addded
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  

    
