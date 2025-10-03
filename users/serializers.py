from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
MAIN_FLOW_ID = os.getenv("MAIN_FLOW_ID")
UPLOAD_DOCS_FLOW_ID = os.getenv("UPLOAD_DOCS_FLOW_ID")

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        data = super().validate(attrs)

        # expires_at_utc = datetime.fromtimestamp(data["exp"], tz=timezone.utc)
        # expires_at_gmt1 = expires_at_utc + timedelta(hours=1)  # Convertir a GMT+1

        # data["expires_at"] = expires_at_gmt1.isoformat()
        

        return data
        

        
class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = RefreshToken(attrs['refresh'])

        data['access'] = str(refresh.access_token)

        return data
    
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        
        return user