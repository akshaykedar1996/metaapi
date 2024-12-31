from django.shortcuts import render , HttpResponse , redirect
from .models import *
# Create your views here.
# def login_client(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         print(f'email: {email} \npassword: {password}')
#         return redirect('home')
#     return render(request , 'Client/Login.html')
#  #   return HttpResponse('login client')

from .authentication import *
from .serializers import *
from django.utils import timezone

def login_client(request):

    if 'msg' in request.GET:
        msg = request.GET['msg']
    else:
        msg = None 
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = ClientDetail.objects.get(email=email)
            if password == user.password:
                user_id = ClientDetail.objects.get(email=user.email)
                # Check if last login date is today or later
                if user_id.Expire_date.date() >= timezone.now().date():
                    request.session['user_id'] = user_id.user_id
                    print('login')
                    alls = SYMBOL.objects.all()
                    
                    for s in alls:
                        try:
                            signals = Client_SYMBOL_QTY.objects.get(client_id = user_id.user_id , SYMBOL = s.SYMBOL)
                            q = signals.QUANTITY
                            d = signals.client_id
                        except:    
                            q = 0
                            d = "my"
                        if user_id.user_id != d:
                            creat = Client_SYMBOL_QTY.objects.create(
                                client_id = user_id.user_id,
                                SYMBOL = s.SYMBOL,
                                QUANTITY = q
                            )
                            

                    return redirect('home')
                else:
                    return redirect('/?msg=Your lane is expire')  
                
            else:
                return redirect('/?msg=wrong password') 
        except Exception as e:
            print(e)
         #   return HttpResponse('email no register')
            return redirect('/?msg=Email no register') 
     
    return render(request,'Client/Login.html', {'msg':msg})


def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('/')
    

def home(request):
    if 'user_id' not in request.session:
        redirect('login_client')
    return render(request , 'Client/home.html')


def home2(request):
    if 'user_id' not in request.session:
        redirect('login_client')
    if 'msg' in request.GET:
        msg = request.GET['msg']
    else:
        msg = None     
    user_id = request.session.get('user_id')    
    client = ClientDetail.objects.get(user_id = user_id) 
    try:
        group = GROUP.objects.get(GROUP=client.client_Group)
        filtered_signals = Client_SYMBOL_QTY.objects.filter(client_id=user_id)
            # Retrieve all symbols from the group
        symbols = group.symbols.all()
     
    except GROUP.DoesNotExist:
        symbols = []
    if request.method == "POST":
        # Fetch the signals filtered by client ID
        filtered_signals = Client_SYMBOL_QTY.objects.filter(client_id=user_id)

        # Get the user's group for max quantity check
        try:
            group = GROUP.objects.get(GROUP=client.client_Group) # Assuming a single group per user
        except GROUP.DoesNotExist:
            return redirect('/dashboard/?msg=Group not found for user')

        # Process each signal in the form
        for i in range(1, len(filtered_signals) + 1):
            symbol = request.POST.get(f'symbol_{i}')
            quantity = request.POST.get(f'quantity_{i}')
            trading = 'on' if request.POST.get(f'trading_{i}') else 'off'
            print(symbol ,'\n',quantity ,'\n',trading)
            # Default handling for quantity
            if not quantity:
                quantity = 0
            else:
                quantity = float(quantity)

            # Check if quantity exceeds the max_quantity for the group
            if quantity <= float(group.max_quantity):
                try:
                    # Update the signal
                    signal = filtered_signals.get(SYMBOL=symbol)
                    signal.QUANTITY = float(quantity)
                    signal.trade = trading
                    signal.save()

                except Client_SYMBOL_QTY.DoesNotExist:
                    print(f"Signal with symbol '{symbol}' does not exist.")
            else:
                print(f"Symbol '{symbol}' exceeds group max_quantity {group.max_quantity}.")
                error_msg = f"Symbol '{symbol}' exceeds allowed quantity ({group.max_quantity})."
                return redirect(f'/thread-control/?msg={error_msg}')
        return redirect('/thread-control/?msg=Updated successfully')    
    dt = {'msg':msg,
            'signals':filtered_signals,
            'symbols':symbols,    
      }
    return render(request , 'Client/home2.html',dt)






'''

=============================================================================================================================

---------------------------------------------  API create -----------------------------------------------------

=============================================================================================================================


'''


from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.shortcuts import redirect
from .models import ClientDetail, SYMBOL, Client_SYMBOL_QTY

@api_view(['POST'])
def jwt_login_client(request):
    email = request.data.get('email')
    password = request.data.get('password')
    print(f'email : {email}')
    print(f'password ; {password}')

    try:
        # Check if user exists
        user = ClientDetail.objects.get(email=email)
        if password == user.password:
            # Check if the subscription is still valid
            if user.Expire_date.date() >= timezone.now().date():
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                # Handle SYMBOL logic
                alls = SYMBOL.objects.all()
                for s in alls:
                    try:
                        signals = Client_SYMBOL_QTY.objects.get(client_id=user.user_id, SYMBOL=s.SYMBOL)
                        q = signals.QUANTITY
                        d = signals.client_id
                    except Client_SYMBOL_QTY.DoesNotExist:
                        q = 0
                        d = "my"

                    if user.user_id != d:
                        Client_SYMBOL_QTY.objects.create(
                            client_id=user.user_id,
                            SYMBOL=s.SYMBOL,
                            QUANTITY=q
                        )

                # Return JWT tokens and user info
                return Response({
                    'message': 'Login successful',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user_id': user.user_id,
                })
            else:
                return Response({'error': 'Your plan has expired'}, status=400)
        else:
            return Response({'error': 'Invalid password'}, status=400)
    except ClientDetail.DoesNotExist:
        return Response({'error': 'Email not registered'}, status=400)

from rest_framework.views import APIView
from rest_framework import status
# Custom view to handle token generation for Employee login
class ClientLoginToken(APIView):
    def post(self, request):
        # Fetching email and password from the request body
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = ClientDetail.objects.get(email=email)
            if password == user.password:
                if user.Expire_date.date() >= timezone.now().date():
                    # Generate JWT tokens
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    refresh_token = str(refresh)

                    return Response({
                        'message': 'Login successful',
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        'user_id': user.user_id,
                    }, status=status.HTTP_200_OK)
             
                   
            else:
                # If password doesn't match, return Unauthorized response
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except ClientDetail.DoesNotExist:
            # If no employee is found with the given email, return a "User not found" response
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

'''============================================================================================================================================================'''        
        
# This Code Login API JWT and Session baesed login APA methods         
        
'''
from django.utils.timezone import now
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import ClientDetail

@api_view(['POST'])
def jwt_login_client(request):
    """
    JWT Login API: User ko login karne par JWT tokens return karta hai.
    """
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        # Check user existence
        user = ClientDetail.objects.get(email=email)
        
        # Password check karo
        if user.password == password:
            # Subscription check
            if user.Expire_date.date() >= now().date():
                # JWT tokens generate karo
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                return Response({
                    'message': 'Login successful',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user_id': user.user_id,
                })
            else:
                return Response({'error': 'Your plan has expired'}, status=400)
        else:
            return Response({'error': 'Invalid password'}, status=400)

    except ClientDetail.DoesNotExist:
        return Response({'error': 'Email not registered'}, status=400)


from django.utils.timezone import now
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import ClientDetail

@csrf_exempt  # CSRF token ki zarurat nahi API ke liye
def session_login_api(request):
    """
    Session-Based Login API:
    User credentials verify karta hai aur session create karta hai.
    """
    if request.method == 'POST':
        try:
            # Parse incoming JSON request
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            # Authenticate user
            try:
                user = ClientDetail.objects.get(email=email)
                if user.password == password:
                    # Check subscription validity
                    if user.Expire_date.date() >= now().date():
                        # Create session
                        request.session['user_id'] = user.user_id

                        return JsonResponse({
                            'status': 'success',
                            'message': 'Login successful',
                            'user_id': user.user_id
                        }, status=200)
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Your plan has expired'}, status=400)
                else:
                    return JsonResponse({'status': 'error', 'message': 'Invalid password'}, status=400)

            except ClientDetail.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Email not registered'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON payload'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)




@csrf_exempt
def get_user_details(request):
    """
    Session-Based API to Retrieve Logged-In User Details.
    """
    if request.method == 'GET':
        # Check if session has 'user_id'
        user_id = request.session.get('user_id')
        if user_id:
            try:
                # Retrieve user from ClientDetail model
                user = ClientDetail.objects.get(user_id=user_id)
                
                # Return user details as JSON
                return JsonResponse({
                    'status': 'success',
                    'user_id': user.user_id,
                    'email': user.email,
                    'plan_expiry': user.Expire_date.strftime('%Y-%m-%d'),
                }, status=200)
            except ClientDetail.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
        else:
            return JsonResponse({'status': 'error', 'message': 'User not logged in'}, status=401)
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
'''


# View to fetch and return employee details after successful authentication
class EmployeeDetailView(APIView):
    # Setting the custom permission class to ensure the user is an authenticated Employee
    permission_classes = [IsClientAuthenticated]

    # Using custom JWT authentication class for authenticating the employee using the token
    authentication_classes = [ClientJWTAuthentication]

    def get(self, request):
        # Getting the user from the request after authentication (this will be the authenticated employee)
        user = request.user

        # Checking if the authenticated user is indeed an instance of Employee
        if not isinstance(user, ClientDetail):
            # If the user is not an Employee (perhaps it's a superuser or a different model), return Unauthorized response
            return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        # If the user is an Employee, serialize the employee data
        serializer = ClientDetailSerializer(user)
    
        # Returning the serialized employee data in the response with HTTP 200 OK status
        return Response(serializer.data, status=status.HTTP_200_OK)