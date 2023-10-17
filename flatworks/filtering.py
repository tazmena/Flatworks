from django_filters import FilterSet
from .models import Property

class PropertyFilter(FilterSet):
    
    class Meta:
        model = Property
        fields = ['property_cost','property_type','property_accessibility_wheelchair','property_accessibility_lift', 'property_furnished', 'property_number_of_rooms', 'property_communal_spaces', 'property_latitude','property_longitude']
        