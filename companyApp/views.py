from django.shortcuts import render, get_object_or_404
from . models import *
from . serializers import *
from rest_framework.views import APIView,Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from .utils import send_password_reset  # assume this sends an email
from django.urls import reverse

# Create your views here.

class EmployeeListCreateView(APIView):

    def get(self, request):
        user = request.user
        employees = Employee.objects.filter(company=user)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=user)  # Link employee to the logged-in company
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class EmployeeRetrieveUpdateDeleteView(APIView):

    def get_object(self, pk, user):
        return get_object_or_404(Employee, pk=pk, company=user)

    def get(self, request, pk):
        employee = self.get_object(pk, request.user)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def patch(self, request, pk):
        employee = self.get_object(pk, request.user)
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # company is already set, no need to reset
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        employee = self.get_object(pk, request.user)
        employee.delete()
        return Response(status=204)
    
    
    
# class EmployeeDetailView(APIView):
#     def get(self, request, pk):
#         employee = Employee.objects.get(pk=pk)
#         serializer = EmployeeSerializer(employee)
#         return Response(serializer.data)
    
# class EmployeeUpdateView(APIView):
#     def patch(self, request, pk):
#         employee = Employee.objects.get(pk=pk)
#         serializer = EmployeeSerializer(employee, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class EmployeeDeleteView(APIView):
#     def delete(self, request, pk):
#         employee = Employee.objects.get(pk=pk)
#         employee.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)        
    


# class EmployeeRegistrationView(APIView):
#     permission_classes = [AllowAny] 

#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Registration successfull"}, status=201)
#         return Response(serializer.errors, status=400)
     
# class EmployeeRegistrationView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = (AllowAny, )
#     serializer_class = RegisterSerializer



# class EmployeeLoginView(generics.GenericAPIView):
#         serializer_class = LoginSerializer 
#         permission_classes = (AllowAny, )
        
        
#         def post(self, request, *args, **kwargs):
#             username = request.data.get('username')
#             password = request.data.get('password')
#             user = authenticate(username = username, password = password)
            
#             if user is not None:
#                 refresh = RefreshToken.for_user(user)
#                 user_serializer = UserSerializer(user)
#                 return Response({
#                     'refresh': str(refresh),
#                     'access' : str(refresh.access_token),
#                     'user' : user_serializer.data
#                 })
#             else:
#                 return Response({'message': 'Invalid Credentials'},status=401)

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Registration successful."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user

            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": "Incorrect current password."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data['new_password'])
            user.save()

            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = Company.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = PasswordResetTokenGenerator().make_token(user)

                reset_link = f"{request.scheme}://{request.get_host()}{reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})}"
                
                # Send the link via email or just print for dev purposes
                send_password_reset(user.email, reset_link)
            except Company.DoesNotExist:
                pass  # Don't reveal that the email doesn't exist
            
            return Response(
                {"message": "If your email is registered, you will receive a password reset link."},
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    
    
    def post(self, request, uidb64, token):
        serializer = ResetPasswordSerializer(
            data=request.data,
            uidb64=uidb64,   
            token=token      
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 

# class PasswordResetConfirmView(APIView):
    
    
#     def post(self, request, uidb64, token):
#         serializer = ResetPasswordSerializer(data=request.data, context={
#             'uidb64': uidb64,
#             'token': token
#         })
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)