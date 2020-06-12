from django.urls import  path

from property.views import *

app_name = 'property'


urlpatterns = [
    path('cards/', PropertyCardList.as_view(), name='card-list'),
    path('list/', PropertyList.as_view(), name='list'),
    path('details/<id>/', PropertyDetail.as_view(), name='detail'),
    path('requests/<id>/', ClientRequest.as_view(), name='client-request')
]