from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Country(models.Model):
    designation = models.CharField(max_length=50)
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.designation


class Team(models.Model):
    name = models.CharField(max_length=70)
    date = models.DateField()
    championships = models.IntegerField()

    def __str__(self):
        return self.name


class Pilot(models.Model):
    name = models.CharField(max_length=70)
    date = models.DateField()
    victories = models.IntegerField()
    pole_positions = models.IntegerField()
    podiums = models.IntegerField()
    championships = models.IntegerField()
    contract = models.IntegerField()
    entry_year = models.IntegerField()
    team = models.ForeignKey(Team, on_delete=models.RESTRICT)
    country = models.ManyToManyField(Country)

    def __str__(self):
        return self.name

    @property
    def total_points(self):
        return sum([r.points for r in self.result_set.all()])


class Car(models.Model):
    model = models.CharField(max_length=70)
    engine = models.CharField(max_length=70)
    weight = models.IntegerField()
    pilot = models.OneToOneField(Pilot, on_delete=models.RESTRICT)

    def __str__(self):
        return self.model


class Circuit(models.Model):
    name = models.CharField(max_length=70)
    length = models.FloatField()
    location = models.CharField(max_length=70)
    last_winner = models.ForeignKey(Pilot, on_delete=models.RESTRICT)
    country = models.ForeignKey(Country, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class Race(models.Model):
    name = models.CharField(max_length=70)
    date = models.DateField()
    season = models.IntegerField()
    fast_lap = models.TimeField()
    circuit = models.ForeignKey(Circuit, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class Result(models.Model):
    position = models.IntegerField()
    pilot = models.ForeignKey(Pilot, on_delete=models.RESTRICT)
    race = models.ForeignKey(Race, on_delete=models.RESTRICT)
    points = models.IntegerField()

    def __str__(self):
        return str(self.position)


class TeamLeader(models.Model):
    name = models.CharField(max_length=70)
    team = models.OneToOneField(Team, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='app/static/images/profiles/')
    biography = models.CharField(max_length=150)
    favourite_pilot = models.ManyToManyField(Pilot)
    favourite_team = models.ManyToManyField(Team)

