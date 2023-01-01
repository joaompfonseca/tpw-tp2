from app.models import *
from rest_framework import serializers
from django.contrib.auth.models import User


class StatsSerializer(serializers.Serializer):
    total_pilots = serializers.IntegerField()
    total_teams = serializers.IntegerField()
    total_races = serializers.IntegerField()


class LeaderboardSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    points = serializers.IntegerField()


class HomeSerializer(serializers.Serializer):
    stats = StatsSerializer()
    pilots_leaderboard = LeaderboardSerializer(many=True)
    teams_leaderboard = LeaderboardSerializer(many=True)


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
    is_authenticated = serializers.BooleanField()
    is_superuser = serializers.BooleanField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'designation', 'code')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'date', 'championships', 'image')


class PilotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pilot
        fields = (
            'id', 'name', 'date', 'victories', 'pole_positions', 'podiums', 'championships', 'contract', 'entry_year',
            'team',
            'country', 'image')


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('id', 'model', 'engine', 'weight', 'pilot')


class CircuitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circuit
        fields = ('id', 'name', 'length', 'location', 'last_winner', 'country')


class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = ('id', 'name', 'date', 'season', 'fast_lap', 'circuit')


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('id', 'position', 'pilot', 'race', 'points')


class TeamLeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamLeader
        fields = ('id', 'name', 'team', 'image')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'profile_image', 'biography', 'favourit_pilot', 'favourit_team')


class FavSerializer(serializers.Serializer):
    is_fav = serializers.BooleanField()


class HeaderSerializer(serializers.Serializer):
    header = serializers.CharField()


class AuthSerializer(serializers.Serializer):
    is_authenticated = serializers.BooleanField()
    is_superuser = serializers.BooleanField()


class PointsSerializer(serializers.Serializer):
    points = serializers.IntegerField()
