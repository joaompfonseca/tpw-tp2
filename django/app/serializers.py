from app.models import *
from rest_framework import serializers


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('designation', 'code')


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('name', 'date', 'championships', 'image')


class PilotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pilot
        fields = ('name', 'date', 'victories', 'pole_positions', 'podiums', 'championships', 'contract', 'entry_year', 'team', 'country', 'image')


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('model', 'engine', 'weight', 'pilot')


class CircuitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circuit
        fields = ('name', 'length', 'location', 'last_winner', 'country')


class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = ('name', 'date', 'season', 'fast_lap', 'circuit')


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('position', 'pilot', 'race', 'points')


class TeamLeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamLeader
        fields = ('name', 'team', 'image')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'profile_image', 'biography', 'favourit_pilot', 'favourit_team')
