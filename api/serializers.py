from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ["user_hash", "username", "email", "first_name", "last_name", "role", "creation_date", "profile_picture"]