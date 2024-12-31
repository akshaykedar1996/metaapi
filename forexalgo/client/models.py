from django.db import models
import uuid
from django.core.validators import *


class SYMBOL(models.Model):
    #   user = models.ForeignKey(ClientDetail, on_delete=models.CASCADE , blank=True, null=True) 
      SYMBOL = models.CharField(max_length=10)
      created_at = models.DateTimeField(auto_now_add=True)
      
      def __str__(self):
        return self.SYMBOL

class GROUP(models.Model):
    GROUP = models.CharField(max_length=20)
    symbols = models.ManyToManyField(SYMBOL, related_name='groups')
    min_quantity = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    max_quantity = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.GROUP
    
# Create your models here.
class ClientDetail(models.Model):
    user_id = models.CharField(max_length=8, unique=True, default=uuid.uuid4().hex[:8])
    # user_id = models.IntegerField(verbose_name="user_id",  unique=True, primary_key=True)
    name_first = models.CharField(max_length=50, blank=True, null=True)
    name_last = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=50,blank=True, null=True)
    phone_number = models.CharField(max_length=15,blank=True, null=True)
    verify_code = models.CharField(max_length=15,blank=True, null=True)
    date_joined	= models.DateTimeField(verbose_name='date joined', default=None)
    Expire_date= models.DateTimeField(verbose_name='Expire login',default=None)
    status= models.BooleanField(default=False)    
    clint_status = models.CharField(max_length=15,blank=True, null=True)
    client_Group = models.ForeignKey(GROUP, on_delete=models.SET_NULL, blank=True, null=True)

    mt5_login = models.CharField(max_length=100, blank=True, null=True)
    mt5_password = models.CharField(max_length=100, blank=True, null=True)
    mt5_server = models.CharField(max_length=100, blank=True, null=True)
    api_key = models.CharField(max_length=10000, blank=True, null=True) 
    

    
      

class Client_SYMBOL_QTY(models.Model):
    client_id = models.CharField(max_length=50, blank=True, null=True)    
    SYMBOL = models.CharField(max_length=50, blank=True, null=True)
    QUANTITY = models.FloatField(null=True, blank=True)
    trade = models.CharField(max_length=50, blank=True, null=True)    
    created_at = models.DateTimeField(auto_now_add=True)


class ClientSignal(models.Model):
    admin = models.CharField(max_length=50, blank=True, null=True)
    client_id = models.CharField(max_length=50, blank=True, null=True)
    message_id = models.CharField(max_length=50, blank=True, null=True)
    ids = models.CharField(max_length=50, blank=True, null=True)
    
    SYMBOL = models.ForeignKey(SYMBOL, on_delete=models.CASCADE, related_name='client_signals')
    TYPE_CHOICES = (
        ('BUY_ENTRY', 'BUY_ENTRY'),
        ('BUY_EXIT', 'BUY_EXIT'),
        ('SELL_ENTRY', 'SELL_ENTRY'),
        ('SELL_EXIT', 'SELL_EXIT'),
    )
    TYPE = models.CharField(max_length=10, choices=TYPE_CHOICES)
    QUANTITY = models.FloatField(null=True, blank=True)
    ENTRY_PRICE = models.DecimalField(max_digits=12, decimal_places=5,null=True,blank=True)
    EXIT_PRICE = models.DecimalField(max_digits=12, decimal_places=5,null=True,blank=True)
    profit_loss =  models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    cumulative_pl =  models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
     