from django.shortcuts import render , HttpResponse

# Create your views here.
def login_subadmin(request):
    return render(request , 'SubAdmin/Login.html')