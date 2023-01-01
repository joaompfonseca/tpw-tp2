from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.http import FileResponse, HttpResponse
from django.shortcuts import render, redirect
from rest_framework import status, authentication, permissions, views, generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from app.models import *
from app.forms import *
from app.serializers import *


# Create your views here.

# Home

@api_view(['GET'])
def home(req):
    # Stats
    stats_s = StatsSerializer({
        'total_pilots': Pilot.objects.count(),
        'total_teams': Team.objects.count(),
        'total_races': Race.objects.count()
    })

    # Pilots Leaderboard
    pilots_lb = []
    for pilot in Pilot.objects.all():
        pilots_lb.append({'id': pilot.id,
                          'name': pilot.name,
                          'points': pilot.total_points})
    pilots_lb.sort(key=lambda x: x['points'], reverse=True)
    pilots_lb_s = LeaderboardSerializer(pilots_lb, many=True)

    # Teams Leaderboard
    teams_lb = []
    for team in Team.objects.all():
        teams_lb.append({'id': team.id,
                         'name': team.name,
                         'points': sum([pilot.total_points for pilot in Pilot.objects.filter(team=team)])})
    teams_lb.sort(key=lambda x: x['points'], reverse=True)
    teams_lb_s = LeaderboardSerializer(teams_lb, many=True)

    home_s = HomeSerializer({
        'stats': stats_s.data,
        'pilots_leaderboard': pilots_lb_s.data,
        'teams_leaderboard': teams_lb_s.data
    })

    return Response(home_s.data)


# Auth

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user1 = authenticate(username=user.username, password=request.data['password'])
        Profile.objects.create(user=user1, profile_image='/images/profiles/profile.jpg')
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        temp = serializer.validated_data
        user = authenticate(username=temp['username'], password=temp['password'])
        login(request, user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
        })


class LogoutAPI(generics.GenericAPIView):
    def get(self, request, format=None):
        logout(request)
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def user_get(req):
    user = req.user
    if user.is_authenticated:
        t = UserSerializer(user)
        return Response(t.data)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


# Car

@api_view(['GET'])
def car_get(req):
    _id = int(req.GET['id'])
    try:
        car = Car.objects.get(id=_id)
        pilot = Pilot.objects.get(car=car)
        pa = PilotSerializer(pilot)
        team = pilot.team
        ta = TeamSerializer(team)
        header = HeaderSerializer({'header': 'Car Details'})
        is_authenticated = IsAuthenticated()
        is_superuser = IsAdminUser()
        auth = AuthSerializer({'is_authenticated': is_authenticated, 'is_superuser': is_superuser})
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CarSerializer(car)
    return Response(
        {'car': serializer.data, 'pilot': pa.data, 'team': ta.data, 'header': header.data, 'auth': auth.data})


@api_view(['GET'])
def cars_get(req):
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def car_search(req):
    model = str(req.GET['model'])
    pilot = str(req.GET['pilot'])
    query = f'Car.model={model};Car.pilot={pilot}'
    if 'searched' in req.session:
        if query in req.session['searched'].keys():
            pass
        else:
            cars = Car.objects.filter(Q(model__icontains=model)
                                      & Q(pilot__name__icontains=pilot))
            if len(req.session['searched']) >= 10:
                (k := next(iter(req.session['searched'])), req.session['searched'].pop(k))
            serializer = CarSerializer(cars, many=True)
            req.session['searched'][query] = serializer.data
            req.session.save()
    else:
        req.session['searched'] = dict()
        # make query
        cars = Car.objects.filter(Q(model__icontains=model)
                                  & Q(pilot__name__icontains=pilot))
        serializer = CarSerializer(cars, many=True)
        req.session['searched'][query] = serializer.data
    return Response(req.session['searched'][query])


@api_view(['POST'])
@permission_classes([IsAdminUser])
def car_create(req):
    serializer = CarSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def car_update(req):
    _id = int(req.GET['id'])
    try:
        car = Car.objects.get(id=_id)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CarSerializer(car, data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Circuit

@api_view(['GET'])
def circuit_get(req):
    _id = int(req.GET['id'])
    try:
        circuit = Circuit.objects.get(id=_id)
        races = Race.objects.filter(circuit=circuit)
        is_authenticated = IsAuthenticated()
        is_superuser = IsAdminUser()
        country = circuit.country
        last_winner = circuit.last_winner
    except Circuit.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CircuitSerializer(circuit)
    serializer1 = RaceSerializer(races, many=True)
    auth = AuthSerializer({'is_authenticated': is_authenticated, 'is_superuser': is_superuser})
    header = HeaderSerializer({'header': 'Circuit Details'})
    country = CountrySerializer(country)
    pilot = PilotSerializer(last_winner)
    return Response(
        {'circuit': serializer.data, 'races': serializer1.data, 'country': country.data, 'last_winner': pilot.data,
         'auth': auth.data, 'header': header.data})


@api_view(['GET'])
def circuits_get(req):
    circuits = Circuit.objects.all()
    serializer = CircuitSerializer(circuits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def circuit_search(req):
    name = str(req.GET['name'])
    query = f'Circuit.name={name}'
    if 'searched' in req.session:
        if query in req.session['searched'].keys():
            pass
        else:
            circuits = Circuit.objects.filter(name__icontains=name)
            if len(req.session['searched']) >= 10:
                (k := next(iter(req.session['searched'])), req.session['searched'].pop(k))
            serializer = CircuitSerializer(circuits, many=True)
            req.session['searched'][query] = serializer.data
            req.session.save()
    else:
        req.session['searched'] = dict()
        # make query
        circuits = Circuit.objects.filter(name__icontains=name)
        serializer = CircuitSerializer(circuits, many=True)
        req.session['searched'][query] = serializer.data
    return Response(req.session['searched'][query])


@api_view(['POST'])
@permission_classes([IsAdminUser])
def circuit_create(req):
    serializer = CircuitSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def circuit_update(req):
    _id = int(req.GET['id'])
    try:
        circuit = Circuit.objects.get(id=_id)
    except Circuit.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CircuitSerializer(circuit, data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Country

@api_view(['GET'])
def country_get(req):
    _id = int(req.GET['id'])
    try:
        country = Country.objects.get(id=_id)
        pilots = Pilot.objects.filter(country=country)
        circuits = Circuit.objects.filter(country=country)
        is_authenticated = IsAuthenticated()
        is_superuser = IsAdminUser()
    except Country.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CountrySerializer(country)
    serializer1 = PilotSerializer(pilots, many=True)
    circuits = CircuitSerializer(circuits, many=True)
    header = HeaderSerializer({'header': 'Country Details'})
    auth = AuthSerializer({'is_authenticated': is_authenticated, 'is_superuser': is_superuser})
    return Response(
        {'country': serializer.data, 'pilots': serializer1.data, 'circuits': circuits.data, 'auth': auth.data,
         'header': header.data})


@api_view(['GET'])
def countries_get(req):
    countries = Country.objects.all()
    serializer = CountrySerializer(countries, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def country_search(req):
    designation = str(req.GET['designation'])
    query = f'Country.designation={designation}'
    if 'searched' in req.session:
        if query in req.session['searched'].keys():
            pass
        else:
            countries = Country.objects.filter(designation__icontains=designation)
            if len(req.session['searched']) >= 10:
                (k := next(iter(req.session['searched'])), req.session['searched'].pop(k))
            serializer = CountrySerializer(countries, many=True)
            req.session['searched'][query] = serializer.data
            req.session.save()
    else:
        req.session['searched'] = dict()
        # make query
        countries = Country.objects.filter(designation__icontains=designation)
        serializer = CountrySerializer(countries, many=True)
        req.session['searched'][query] = serializer.data
    return Response(req.session['searched'][query])


@api_view(['POST'])
@permission_classes([IsAdminUser])
def country_create(req):
    serializer = CountrySerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def country_update(req):
    _id = int(req.GET['id'])
    try:
        country = Country.objects.get(id=_id)
    except Country.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CountrySerializer(country, data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Pilot

@api_view(['GET'])
def pilot_get(req):
    _id = int(req.GET['id'])
    try:
        serializer2 = None
        pilot = Pilot.objects.get(id=_id)
        if not isinstance(req.user, AnonymousUser):
            if pilot in Profile.objects.get(user=req.user).favourite_pilot.all():
                is_fav = True
            else:
                is_fav = False
            serializer2 = FavSerializer({'is_fav': is_fav})
        results = Result.objects.filter(pilot=pilot).order_by('-race__date')
        team = pilot.team
        is_authenticated = IsAuthenticated()
        is_superuser = IsAdminUser()
        countries = pilot.country
        races = []
        for result in results:
            races.append(result.race)

    except Pilot.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    points = 0
    for result in results:
        points += result.points

    serializer = PilotSerializer(pilot)
    serializer1 = ResultSerializer(results, many=True)
    serializer3 = TeamSerializer(team)
    serializer4 = CountrySerializer(countries, many=True)
    serializer5 = RaceSerializer(races, many=True)
    header = HeaderSerializer({'header': 'Pilot Details'})
    auth = AuthSerializer({'is_authenticated': is_authenticated, 'is_superuser': is_superuser})
    points = PointsSerializer({'points': points})
    if serializer2:
        return Response(
            {'pilot': serializer.data, 'results': serializer1.data, 'is_fav': serializer2.data, 'header': header.data,
             'auth': auth.data, 'team': serializer3.data, 'country': serializer4.data, 'points': points.data,
             'races': serializer5.data})
    else:
        return Response(
            {'pilot': serializer.data, 'results': serializer1.data, 'header': header.data, 'auth': auth.data,
             'team': serializer3.data, 'country': serializer4.data, 'points': points.data, 'races': serializer5.data})


def pilot_points(id):
    pilot = Pilot.objects.get(id=id)
    results = Result.objects.filter(pilot=pilot)
    points = 0
    for result in results:
        points += result.points
    return points


@api_view(['GET'])
def pilots_get(req):
    pilots = Pilot.objects.all()
    serializer = PilotSerializer(pilots, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def pilot_search(req):
    name = str(req.GET['name'])
    query = f'Pilot.name={name}'
    if 'searched' in req.session:
        if query in req.session['searched'].keys():
            pass
        else:
            pilots = Pilot.objects.filter(name__icontains=name)
            if len(req.session['searched']) >= 10:
                (k := next(iter(req.session['searched'])), req.session['searched'].pop(k))
            serializer = PilotSerializer(pilots, many=True)
            req.session['searched'][query] = serializer.data
            req.session.save()
    else:
        req.session['searched'] = dict()
        # make query
        pilots = Pilot.objects.filter(nameicontains=name)
        serializer = PilotSerializer(pilots, many=True)
        req.session['searched'][query] = serializer.data
    return Response(req.session['searched'][query])


@api_view(['POST'])
@permission_classes([IsAdminUser])
def pilot_create(req):
    serializer = PilotSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def pilot_update(req):
    _id = int(req.GET['id'])
    try:
        pilot = Pilot.objects.get(id=_id)
    except Pilot.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PilotSerializer(pilot, data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Race

@api_view(['GET'])
def race_get(req):
    _id = int(req.GET['id'])
    try:
        race = Race.objects.get(id=_id)
        results = Result.objects.filter(race=race).order_by('position')
        is_authenticated = IsAuthenticated()
        is_superuser = IsAdminUser()
        circuit = race.circuit
        pilots = []
        for result in results:
            pilots.append(result.pilot)
    except Race.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = RaceSerializer(race)
    serializer1 = ResultSerializer(results, many=True)
    serializer2 = CircuitSerializer(circuit)
    serializer3 = PilotSerializer(pilots, many=True)
    header = HeaderSerializer({'header': 'Race Details'})
    auth = AuthSerializer({'is_authenticated': is_authenticated, 'is_superuser': is_superuser})
    return Response({'race': serializer.data, 'results': serializer1.data, 'header': header.data, 'auth': auth.data,
                     'circuit': serializer2.data, 'pilots': serializer3.data})


@api_view(['GET'])
def races_get(req):
    races = Race.objects.all()
    serializer = RaceSerializer(races, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def race_search(req):
    name = str(req.GET['name'])
    query = f'Race.name={name}'
    if 'searched' in req.session:
        if query in req.session['searched'].keys():
            pass
        else:
            races = Race.objects.filter(name__icontains=name)
            if len(req.session['searched']) >= 10:
                (k := next(iter(req.session['searched'])), req.session['searched'].pop(k))
            serializer = RaceSerializer(races, many=True)
            req.session['searched'][query] = serializer.data
            req.session.save()
    else:
        req.session['searched'] = dict()
        # make query
        races = Race.objects.filter(name__icontains=name)
        serializer = RaceSerializer(races, many=True)
        req.session['searched'][query] = serializer.data
    return Response(req.session['searched'][query])


@api_view(['POST'])
@permission_classes([IsAdminUser])
def race_create(req):
    serializer = RaceSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def race_update(req):
    _id = int(req.GET['id'])
    try:
        race = Race.objects.get(id=_id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = RaceSerializer(race, data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Result

@api_view(['GET'])
def result_get(req):
    _id = int(req.GET['id'])
    try:
        result = Result.objects.get(id=_id)
    except Result.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ResultSerializer(result)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def result_create(req):
    serializer = ResultSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def result_update(req):
    _id = int(req.GET['id'])
    try:
        result = Result.objects.get(id=_id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ResultSerializer(result, data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Team

@api_view(['GET'])
def team_get(req):
    _id = int(req.GET['id'])
    serializer2 = None
    try:
        team = Team.objects.get(id=_id)
        if not isinstance(req.user, AnonymousUser):
            if team in Profile.objects.get(user=req.user).favourite_team.all():
                faved = True
            else:
                faved = False
            serializer2 = FavSerializer({'is_fav': faved})
        pilots = Pilot.objects.filter(team=team)
        is_authenticated = IsAuthenticated()
        is_superuser = IsAdminUser()
        teamleader = team.teamleader

        points = 0
        for pilot in pilots:
            points += pilot_points(pilot.id)


    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = TeamSerializer(team)
    serializer1 = PilotSerializer(pilots, many=True)
    serializer3 = TeamLeaderSerializer(teamleader)
    points = PointsSerializer({'points': points})
    header = HeaderSerializer({'header': 'Team Details'})
    auth = AuthSerializer({'is_authenticated': is_authenticated, 'is_superuser': is_superuser})
    if serializer2:
        return Response(
            {'team': serializer.data, 'pilots': serializer1.data, 'fav': serializer2.data, 'header': header.data,
             'auth': auth.data, 'teamleader': serializer3.data, 'points': points.data})
    else:
        return Response({'team': serializer.data, 'pilots': serializer1.data, 'header': header.data, 'auth': auth.data,
                         'teamleader': serializer3.data, 'points': points.data})


@api_view(['GET'])
def teams_get(req):
    teams = Team.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def team_search(req):
    name = str(req.GET['name'])
    query = f'Team.name={name}'
    if 'searched' in req.session:
        if query in req.session['searched'].keys():
            pass
        else:
            teams = Team.objects.filter(name__icontains=name)
            if len(req.session['searched']) >= 10:
                (k := next(iter(req.session['searched'])), req.session['searched'].pop(k))
            serializer = TeamSerializer(teams, many=True)
            req.session['searched'][query] = serializer.data
            req.session.save()
    else:
        req.session['searched'] = dict()
        # make query
        teams = Team.objects.filter(name__icontains=name)
        serializer = TeamSerializer(teams, many=True)
        req.session['searched'][query] = serializer.data
    return Response(req.session['searched'][query])


@api_view(['POST'])
@permission_classes([IsAdminUser])
def team_create(req):
    serializer = TeamSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def team_update(req):
    _id = int(req.GET['id'])
    try:
        team = Team.objects.get(id=_id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = TeamSerializer(team, data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TeamLeader

@api_view(['GET'])
def teamleader_get(req):
    _id = int(req.GET['id'])
    try:
        teamleader = TeamLeader.objects.get(id=_id)
        is_authenticated = IsAuthenticated()
        is_superuser = IsAdminUser()
        team = teamleader.team
    except TeamLeader.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = TeamLeaderSerializer(teamleader)
    serializer1 = TeamSerializer(team)
    header = HeaderSerializer({'header': 'Team Leader Details'})
    auth = AuthSerializer({'is_authenticated': is_authenticated, 'is_superuser': is_superuser})
    return Response({'teamleader': serializer.data, 'team': serializer1.data, 'header': header.data, 'auth': auth.data})


@api_view(['GET'])
def teamleaders_get(req):
    teamleaders = TeamLeader.objects.all()
    serializer = TeamLeaderSerializer(teamleaders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def teamleader_search(req):
    name = str(req.GET['name'])
    query = f'TeamLeader.name={name}'
    if 'searched' in req.session:
        if query in req.session['searched'].keys():
            pass
        else:
            teamleaders = TeamLeader.objects.filter(name__icontains=name)
            if len(req.session['searched']) >= 10:
                (k := next(iter(req.session['searched'])), req.session['searched'].pop(k))
            serializer = TeamLeaderSerializer(teamleaders, many=True)
            req.session['searched'][query] = serializer.data
            req.session.save()
    else:
        req.session['searched'] = dict()
        # make query
        teamleaders = TeamLeader.objects.filter(name__icontains=name)
        serializer = TeamLeaderSerializer(teamleaders, many=True)
        req.session['searched'][query] = serializer.data
    return Response(req.session['searched'][query])


@api_view(['POST'])
@permission_classes([IsAdminUser])
def teamleader_create(req):
    serializer = TeamLeaderSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def teamleader_update(req):
    _id = int(req.GET['id'])
    try:
        teamleader = TeamLeader.objects.get(id=_id)
    except TeamLeader.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = TeamLeaderSerializer(teamleader, data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Profile

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_get(req):
    profile = Profile.objects.get(user=req.user)
    t = ProfileSerializer(profile)
    return Response(t.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def profile_update(req):
    profile = Profile.objects.get(user=req.user)
    serializer = ProfileSerializer(profile, data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Pilot Favourites

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pilot_fav_add(req):
    _id = int(req.GET['id'])
    user_profile = Profile.objects.get(user=req.user)
    pilot = Pilot.objects.get(id=_id)
    user_profile.favourite_pilot.add(pilot)
    user_profile.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pilot_fav_rem(req):
    _id = int(req.GET['id'])
    user_profile = Profile.objects.get(user=req.user)
    pilot = Pilot.objects.get(id=_id)
    user_profile.favourite_pilot.remove(pilot)
    user_profile.save()
    return Response(status=status.HTTP_200_OK)


# Team Favourites

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def team_fav_add(req):
    _id = int(req.GET['id'])
    user_profile = Profile.objects.get(user=req.user)
    team = Team.objects.get(id=_id)
    user_profile.favourite_team.add(team)
    user_profile.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def team_fav_rem(req):
    _id = int(req.GET['id'])
    user_profile = Profile.objects.get(user=req.user)
    team = Team.objects.get(id=_id)
    user_profile.favourite_team.remove(team)
    user_profile.save()
    return Response(status=status.HTTP_200_OK)


def get_image(req, type, _id):
    if type == 'pilot':
        image = Pilot.objects.get(id=_id).image
    elif type == 'team':
        image = Team.objects.get(id=_id).image
    elif type == 'teamleader':
        image = TeamLeader.objects.get(id=_id).image
    elif type == 'profile':
        image = Profile.objects.get(user=req.user).profile_image
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return HttpResponse(image, content_type='image/png')
