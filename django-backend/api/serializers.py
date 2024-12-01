from rest_framework import serializers
from django.contrib.auth.models import AbstractUser
from .models import Game, Ranking, Item

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractUser
        fields = ['id', 'username', 'email']

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'user', 'result', 'earned_points', 'created_at']

class RankingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')  # Add username field from user model
    class Meta:
        model = Ranking
        fields = ['id', 'username', 'points']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'base_price', 'description']