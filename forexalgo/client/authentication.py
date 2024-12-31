from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import ClientDetail

# Custom JWT Authentication Class for Employee
class ClientJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        # Extract the 'user_id' from the validated token
        user_id = validated_token.get("user_id")
        
        try:
            # Try to fetch the Employee object using the 'user_id' from the token
            return ClientDetail.objects.get(id=user_id)
        except ClientDetail.DoesNotExist:
            # If no Employee with the given 'user_id' is found, return None
            return None

# Custom Permission Class to check if the user is an Employee
from rest_framework.permissions import BasePermission

class IsClientAuthenticated(BasePermission):
    def has_permission(self, request, view):
        # This method checks whether the authenticated user is an instance of the Employee model.
        # If the request.user is an instance of Employee, return True, meaning the user has permission.
        # If the request.user is not an instance of Employee, return False, meaning the user does not have permission.
        return isinstance(request.user, ClientDetail)
