from django.shortcuts import render , HttpResponse , redirect
from django.contrib import messages
from .models import *
from client.models import *

# Create your views here.
def login_admin(request):
    if request.method == 'POST':
    
        email = request.POST.get('Email')
        password = request.POST.get('password')
        try:
            admindt = AdminDT.objects.get(admin_email = email)
            if password == admindt.admin_password:

                request.session['admin_id'] = admindt.admin_id
                return redirect('deshboard_admin')
            else:
                messages.error(request, 'Wrong password.') 
        except:
            messages.error(request, 'Admin not found.') 
    return render(request , 'admin/SLogin.html')


def logout_admin(request):
    if 'admin_id' in request.session:
        del request.session['admin_id']
    return redirect('admin_login')

def deshboard_admin(request):
    if 'admin_id' not in request.session:
        messages.error(request, 'Login Requered.')
        return redirect('admin_login')
    # return HttpResponse('test')
    admin_id = request.session.get('admin_id')
  
    return render(request , 'admin/home.html')


# ====================== admin_message ===========================================

# Django-related imports
from django.shortcuts import render, get_object_or_404, redirect  # View and redirect functions
from django.utils import timezone  # For working with timezone-aware dates and times
from django.views.decorators.csrf import csrf_protect  # For CSRF protection in forms
from django.db.models import Sum  # To sum up query results
from django.http import JsonResponse  # If you use AJAX-based responses (optional)
from django.contrib.auth.decorators import login_required  # To ensure user is authenticated
from django.db import transaction  # For database transaction management

# Python Standard Libraries
from decimal import Decimal  # To ensure precision for decimal calculations
import random  # For generating unique IDs
import string  # For working with string operations
import uuid  # For generating unique IDs if needed


# Forms - If you're using Django forms
from django.forms import Form  # Optional

def generate_unique_id():
    characters = string.ascii_letters + string.digits
    unique_id = ''.join(random.choice(characters) for _ in range(10))
    return unique_id


@csrf_protect
def admin_message(request):
    if 'admin_id' not in request.session:
        return redirect('/admin/?msg=Login')
    
    # Filter for active ENTRY signals
    entry = ClientSignal.objects.filter(TYPE="BUY_ENTRY")  # Fixed the incorrect field
    error = ""
    success_msg = ""
    symbols = SYMBOL.objects.all()  # Fetch all symbols
    current_date = timezone.now().date()
    d = request.session.get('message_id')

    if request.method == "POST":
       
             # Assuming the admin is authenticated

            # Get the symbol and type of action
            symbol_name = request.POST['symbol']
            ty = request.POST['type']
            qty_str = request.POST.get('quantity', '0')  # Quantity input from form
      
            entry_price = request.POST.get('entry_price', '0')
            exit_price = request.POST.get('exit_price', '0')

            # Fetch the SYMBOL object
            sy = get_object_or_404(SYMBOL, SYMBOL=symbol_name)

            # Check if quantity is valid
            try:
                qty = float(qty_str)
            except ValueError:
                qty = 0  # Default to 0 if invalid

            client_signals = ClientSignal.objects.filter(message_id=d, ids='No')

            # ======================== EXIT LOGIC ==================================
            if ty in ['BUY_EXIT', 'SELL_EXIT'] and client_signals:
                print('run buy')
                client_signal = client_signals.first()
                enp = client_signal.ENTRY_PRICE
                exp = float(exit_price) if exit_price.strip() else None

                if exp is None:
                    error = "Exit price is required for EXIT operations."
                else:
                    # Calculate profit/loss based on symbol type
                    if ty == 'BUY_EXIT':
                        prloss = (exp - enp) * qty * 100
                    elif ty == 'SELL_EXIT':
                        prloss = (enp - exp) * qty * 100

                    # Calculate cumulative profit/loss
                    t = ClientSignal.objects.filter(TYPE=ty, client_id=client_signal.client_id, created_at__date=current_date)
                    total = sum(Decimal(p.profit_loss or 0) for p in t)
                    total_pl = total + Decimal(prloss)

                    # Save the EXIT entry
                    ClientSignal.objects.create(
                        SYMBOL=sy, TYPE=ty, QUANTITY=qty,
                        ENTRY_PRICE=enp, EXIT_PRICE=exp, profit_loss=prloss,
                        cumulative_pl=total_pl, created_at=timezone.now(),
                        message_id=client_signal.message_id, client_id=client_signal.client_id
                    )

                    client_signal.TYPE = "none"  # Reset TYPE for EXIT signals
                    client_signal.save()
                    success_msg = f"{ty} operation successful for {symbol_name}."

            # ======================== ENTRY LOGIC ==================================
            elif ty in ['BUY_ENTRY', 'SELL_ENTRY']:
                print('run sell')
                enp = float(entry_price) if entry_price.strip() else 0.0

                if enp == 0:
                    error = "Entry price is required for ENTRY operations."
                else:
                    # Create a new entry for the client signal
                    creat = ClientSignal.objects.create(
                        SYMBOL=sy, admin='admin', TYPE=ty, QUANTITY=qty,
                        ENTRY_PRICE=enp, EXIT_PRICE=None, profit_loss=None,
                        cumulative_pl=None, created_at=timezone.now()
                    )
                    creat.message_id = creat.id
                    creat.ids = generate_unique_id()
                    creat.save()

                    # Update session with the new message ID
                    request.session['message_id'] = creat.id
                    success_msg = f"{ty} operation successful for {symbol_name}."

                    # Update Client_SYMBOL_QTY for the symbol and quantity
                    client_qty, created = Client_SYMBOL_QTY.objects.get_or_create(
                        client_id=request.user.id, SYMBOL=sy
                    )
                    client_qty.QUANTITY = qty
                    client_qty.save()

    return render(request, 'admin/admin_messages.html', {
        'symbols': symbols,
        'error': error,
        'success_msg': success_msg,
        'entry': entry
    })