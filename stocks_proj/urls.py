from django.urls import path
from . import views
from . import importdata

app_name = 'quandl'


urlpatterns = [

    path('stock',views.stock, name='stock' ),


    ]