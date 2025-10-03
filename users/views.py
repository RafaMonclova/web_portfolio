from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from users.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from users.filters import UserFilter
from users.permission import IsSelfOrSuperUser
from drf_spectacular.utils import extend_schema
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect

# Create your views here.

class CustomLoginView(APIView):
    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(request=CustomTokenObtainPairSerializer)
    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSelfOrSuperUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    
class WebLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    next_page = '/' 

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['username'].widget.attrs.update({
            'placeholder': 'Nombre de usuario',
            'class': 'w-full p-3 rounded-lg bg-gray-700 text-gray-100 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
        form.fields['password'].widget.attrs.update({
            'placeholder': 'Contraseña',
            'class': 'w-full p-3 rounded-lg bg-gray-700 text-gray-100 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
        return form

def web_logout(request):
    logout(request)
    return redirect('home')