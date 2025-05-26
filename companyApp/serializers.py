# from rest_framework import serializers
# from .models import Employee
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate

# class EmployeeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Employee
#         fields = '__all__'
        
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username','email')
  
# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only = True)
    
#     class Meta:
#         Model = User
#         fields = ('username','email', 'password')

#     def create(self, validated_data):
 
#         user = User.objects.create_user(**validated_data)
#         return user

        
# class LoginSerializer(serializers.Serializer): #Serializer because we're not using Model field
#     username = serializers.CharField(required = True)
#     password = serializers.CharField(required = True, write_only = True)

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import Company, Employee

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

#Create your serializers here

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Company
        fields = ['email', 'password', 'confirm_password', 'company_name', 'address']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = Company.objects.create_user(**validated_data)
        return user


    
class CompanyLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        return user



class EmployeeSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.company_name', read_only=True)
    
    class Meta:
        model = Employee
        fields = '__all__'

        
   
        
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "New passwords do not match."})

        if len(attrs['new_password']) < 8:
            raise serializers.ValidationError({"new_password": "Password must be at least 8 characters long."})

        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        self.uidb64 = kwargs.pop('uidb64')
        self.token = kwargs.pop('token')
        super().__init__(*args, **kwargs)

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(self.uidb64))
            self.user = Company.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Company.DoesNotExist):
            raise serializers.ValidationError("Invalid user or UID.")
        
        if not PasswordResetTokenGenerator().check_token(self.user, self.token):
            raise serializers.ValidationError("Invalid or expired token.")

        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        
        if len(data['new_password']) < 8:
            raise serializers.ValidationError({"new_password": "Password must be at least 8 characters long."})

        return data

    def save(self):
        self.user.set_password(self.validated_data['new_password'])
        self.user.save()



class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
 
    class Meta:
        fields = ['email']