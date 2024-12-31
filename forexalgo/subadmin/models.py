from django.db import models

# Create your models here.
from django.utils import timezone
import uuid
from django.core.validators import MinValueValidator

class Subadmin_client_limit(models.Model):
    Subadmin_limit = models.CharField(max_length=20)
    max_quantity = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.Subadmin_limit
    

# subadmin_logo
# class subadmin_logo(models.Model):
#     subadmin_keyword = models.CharField(max_length=1000,blank=True,null=True)
#     subadmin_logo = models.ImageField(upload_to='photos/subadmin_logo',blank=True,null=True)
#     # timestamp
#     created_at = models.DateTimeField(auto_now_add=True)
#     last_modified = models.DateTimeField(auto_now=True)

#     def _str_(self):
#         return self.subadmin_keyword

from datetime import timedelta    
class SubAdminDT(models.Model):
  #  subadmin_id = models.CharField(max_length=8, unique=True, default=uuid.uuid4().hex[:8])
    subadmin_id = models.CharField(max_length=8, unique=True, blank=True, default=uuid.uuid4().hex[:8])
  #   user_id = models.IntegerField(verbose_name="user_id",  unique=True, primary_key=True)
    subadmin_name_first = models.CharField(max_length=50, blank=True, null=True)
    subadmin_name_last = models.CharField(max_length=50, blank=True, null=True)
    subadmin_email = models.EmailField(blank=True, null=True)
    subadmin_password = models.CharField(max_length=50,blank=True, null=True)
    subadmin_phone_number = models.CharField(max_length=15,blank=True, null=True)
    subadmin_verify_code = models.CharField(max_length=15,blank=True, null=True)

    subadmin_keyword = models.CharField(max_length=1000,blank=True,null=True)
    subadmin_logo = models.ImageField(upload_to='photos/subadmin_logo',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True,blank=True, null=True)

    subadmin_client_limit = models.ForeignKey(Subadmin_client_limit, on_delete=models.SET_NULL, blank=True, null=True)
    subadmin_status= models.BooleanField(default=False,blank=True, null=True)  

    subadmin_date_joined = models.DateTimeField(verbose_name='date joined', default=timezone.now)
    subadmin_last_login = models.DateTimeField(verbose_name='last login', default=timezone.now() + timedelta(days=1))

    def save(self, *args, **kwargs):
          # If subadmin_id is not set, generate a new unique ID
          if not self.subadmin_id:
              self.subadmin_id = self.generate_unique_id()
          super(SubAdminDT, self).save(*args, **kwargs)
      
    def generate_unique_id(self): 
          while True:
              # Generate a new ID
              new_id = uuid.uuid4().hex[:8]
              # Check if this ID already exists
              if not SubAdminDT.objects.filter(subadmin_id=new_id).exists():
                  return new_id  
      
      
    def _str_(self):
          return self.subadmin_name_first
    