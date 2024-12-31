
from django.contrib import admin
from django.urls import path , include
from . import views
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
   
    path('',views.login_client , name='login_client'),
    path('home/',views.home , name='home'),
    path('thread-control/',views.home2 , name='home2'),





    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   
    path('api/login_client/', views.jwt_login_client, name='jwt_login_client'), # 
    path('api/login/', ClientLoginToken.as_view(), name='token_obtain'),

    path('api/clientdt/', EmployeeDetailView.as_view(), name='grt_client'),
]
