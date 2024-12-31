
from django.contrib import admin
from django.urls import path , include
from . import views
urlpatterns = [
   
    path('',views.login_subadmin , name='login_subadmin'),

]
