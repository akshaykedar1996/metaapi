
from django.contrib import admin
from django.urls import path , include
from . import views
urlpatterns = [
   
    path('',views.login_admin , name='admin_login'),
    path('logout/',views.logout_admin, name='logout_admin'),
    path('deshboard/',views.deshboard_admin, name='deshboard_admin'),
    path('admin_message/',views.admin_message, name='admin_message'),

]
