import os
import random
import string
import secrets
import urllib.parse
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from datetime import datetime as dt
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from apps.users.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.users.serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer, RegisterSerializer, UserSerializer, UserUpdateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from apps.users.filters import UserFilter
from apps.users.permission import IsSelfOrSuperUser
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.renderers import JSONRenderer
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken
import requests
from rest_framework.parsers import JSONParser
from apps.users.throttles import LoginThrottle
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout


import jwt
import json
from jwt.algorithms import RSAAlgorithm
from django.conf import settings


# Create your views here.

class CustomLoginView(APIView):
    serializer_class = CustomTokenObtainPairSerializer
    throttle_classes = [LoginThrottle]

    @extend_schema(request=CustomTokenObtainPairSerializer)
    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomTokenRefreshView(APIView):
    serializer_class = CustomTokenRefreshSerializer

    @extend_schema(request=CustomTokenRefreshSerializer)
    def post(self, request, *args, **kwargs):
        serializer = CustomTokenRefreshSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSelfOrSuperUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    parser_classes = (MultiPartParser, FormParser)
    
   
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    # override delete to disable it
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False if user.is_active else True
        user.save()
        return Response(status=status.HTTP_200_OK)
    

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