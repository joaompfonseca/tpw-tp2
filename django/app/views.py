from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
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

# def home(req):
#    pilots_leaderboard = []
#    teams_leaderboard = []
#
#    stats = {'total_races': Race.objects.count(),
#             'total_pilots': Pilot.objects.count(), 'total_teams': Team.objects.count()}
#    for pilot in Pilot.objects.all():
#        pilots_leaderboard.append({'pilot': pilot, 'points': pilot.total_points})
#    pilots_leaderboard.sort(key=lambda x: x['points'], reverse=True)
#
#    for team in Team.objects.all():
#        teams_leaderboard.append({'team': team,
#                                  'points': sum([pilot.total_points for pilot in Pilot.objects.filter(team=team)])})
#    teams_leaderboard.sort(key=lambda x: x['points'], reverse=True)
#    ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
#        -1] if req.user.is_authenticated else None,
#           'pilots_leaderboard': pilots_leaderboard, 'stats': stats, 'teams_leaderboard': teams_leaderboard}
#    return render(req, 'home.html', ctx)


# AUTH


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


# Profile


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(req):
    profile = Profile.objects.get(user=req.user)
    t = ProfileSerializer(profile)
    return Response(t.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(req):
    profile = Profile.objects.get(user=req.user)
    serializer = ProfileSerializer(profile, data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Pilot Favourites


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pilot_add_to_favourite(req):
    user_profile = Profile.objects.get(user=req.user)
    pilot = Pilot.objects.get(id=req.data['id'])
    user_profile.favourite_pilot.add(pilot)
    user_profile.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pilot_remove_from_favourites(req):
    user_profile = Profile.objects.get(user=req.user)
    pilot = Pilot.objects.get(id=req.data['id'])
    user_profile.favourite_pilot.remove(pilot)
    user_profile.save()
    return Response(status=status.HTTP_200_OK)


# Team Favourites


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def team_add_to_favourite(req):
    user_profile = Profile.objects.get(user=req.user)
    team = Team.objects.get(id=req.data['id'])
    user_profile.favourite_team.add(team)
    user_profile.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def team_remove_from_favourites(req):
    user_profile = Profile.objects.get(user=req.user)
    team = Team.objects.get(id=req.data['id'])
    user_profile.favourite_team.remove(team)
    user_profile.save()
    return Response(status=status.HTTP_200_OK)


# Car


@api_view(['GET'])
def get_cars(req):
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def car_create(req):
    serializer = CarSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


@api_view(['GET'])
def get_car(req):
    id = str(req.GET['id'])
    try:
        car = Car.objects.get(id=id)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CarSerializer(car)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_car(req):
    id = str(req.GET['id'])
    try:
        car = Car.objects.get(id=id)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CarSerializer(car, data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Circuit

@api_view(['GET'])
def get_circuits(req):
    circuits = Circuit.objects.all()
    print(circuits[0].id)
    serializer = CircuitSerializer(circuits, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def search_circuits(req):
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


@api_view(['GET'])
def get_circuit(req):
    id = str(req.GET['id'])
    try:
        circuit = Circuit.objects.get(id=id)
        races = Race.objects.filter(circuit=circuit)
    except Circuit.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CircuitSerializer(circuit)
    serializer1 = RaceSerializer(races, many=True)
    return Response({'circuit': serializer.data, 'races': serializer1.data})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def new_circuit(req):
    serializer = CircuitSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_circuit(req):
    id = str(req.GET['id'])
    try:
        circuit = Circuit.objects.get(id=id)
    except Circuit.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CircuitSerializer(circuit, data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Country

@api_view(['GET'])
def get_countries(req):
    countries = Country.objects.all()
    serializer = CountrySerializer(countries, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_country(req):
    id = str(req.GET['id'])
    try:
        country = Country.objects.get(id=id)
        pilots = Pilot.objects.filter(country=country)
    except Country.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CountrySerializer(country)
    serializer1 = PilotSerializer(pilots, many=True)
    return Response({'country': serializer.data, 'pilots': serializer1.data})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def new_country(req):
    serializer = CountrySerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search_countries(req):
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


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_country(req):
    id = str(req.GET['id'])
    try:
        country = Country.objects.get(id=id)
    except Country.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CountrySerializer(country, data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Pilot


@api_view(['GET'])
def get_pilots(req):
    pilots = Pilot.objects.all()
    serializer = PilotSerializer(pilots, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def search_pilots(req):
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


@api_view(['GET'])
def get_pilot(req):
    id = str(req.GET['id'])
    try:
        serializer2 = None
        pilot = Pilot.objects.get(id=id)
        if not isinstance(req.user, AnonymousUser):
            if pilot in Profile.objects.get(user=req.user).favourite_pilot.all():
                is_fav = True
            else:
                is_fav = False
            serializer2 = FavSerializer({'is_fav': is_fav})
        results = Result.objects.filter(pilot=pilot).order_by('-race__date')
    except Pilot.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PilotSerializer(pilot)
    serializer1 = ResultSerializer(results, many=True)
    if serializer2:
        return Response({'pilot': serializer.data, 'results': serializer1.data, 'is_fav': serializer2.data})
    else:
        return Response({'pilot': serializer.data, 'results': serializer1.data})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_pilot(req):
    serializer = PilotSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_pilot(req):
    id = str(req.GET['id'])
    try:
        pilot = Pilot.objects.get(id=id)
    except Pilot.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PilotSerializer(pilot, data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Race

@api_view(['GET'])
def get_races(req):
    races = Race.objects.all()
    serializer = RaceSerializer(races, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def search_races(req):
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


@api_view(['GET'])
def get_race(req):
    id = str(req.GET['id'])
    try:
        race = Race.objects.get(id=id)
        results = Result.objects.filter(race=race).order_by('position')
    except Race.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = RaceSerializer(race)
    serializer1 = ResultSerializer(results, many=True)
    return Response({'race': serializer.data, 'results': serializer1.data})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def new_race(req):
    serializer = RaceSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_race(req):
    id = str(req.GET['id'])
    try:
        race = Race.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = RaceSerializer(race, data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Result

"""
def results_list(req):
    results = Result.objects.all()
    actions = [{'str': 'Search Result', 'url': '/results/search'}]
    if req.user.is_authenticated and req.user.username == 'admin':
        actions += [{'str': 'New Result', 'url': '/results/new'}]
    lst = [[{'str': r.pilot, 'url': f'/results/{r.id}'}] for r in results]

    ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[-1] if req.user.is_authenticated else None,'header': 'List of Results', 'actions': actions, 'list': lst}
    return render(req, 'list.html', ctx)


def results_search(req):
    # If POST request, process form data
    if req.method == 'POST':
        # Create a form instance and pass data to it
        form = ResultSearchForm(req.POST)
        if form.is_valid():
            pilot = form.cleaned_data['pilot']
            race = form.cleaned_data['race']

            query = f'Result.pilot={pilot};Result.race={race}'
            # if 'searched' in req.session and req.session['searched'] == query:
            #     return HttpResponse('You have searched for the same thing before. Please try again.')
            # req.session['searched'] = query

            result = Result.objects.filter(Q(pilot=pilot) & Q(race=race))

            return redirect('results_get', _id=result[0].id)
    else:
        # If GET (or any other method), create blank form
        form = ResultSearchForm()
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[-1] if req.user.is_authenticated else None,'header': 'Search Result', 'form': form}
        return render(req, 'search.html', ctx)
"""


@api_view(['GET'])
def get_result(req):
    id = str(req.GET['id'])
    try:
        result = Result.objects.get(id=id)
    except Result.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ResultSerializer(result)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def new_result(req):
    serializer = ResultSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_result(req):
    id = str(req.GET['id'])
    try:
        result = Result.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ResultSerializer(result, data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Team


@api_view(['GET'])
def get_team(req):
    id = str(req.GET['id'])
    serializer2 = None
    try:
        team = Team.objects.get(id=id)
        if not isinstance(req.user, AnonymousUser):
            if team in Profile.objects.get(user=req.user).favourite_team.all():
                faved = True
            else:
                faved = False
            serializer2 = FavSerializer({'is_fav': faved})
        pilots = Pilot.objects.filter(team=team)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = TeamSerializer(team)
    serializer1 = PilotSerializer(pilots, many=True)
    if serializer2:
        return Response({'team': serializer.data, 'pilots': serializer1.data, 'fav': serializer2.data})
    else:
        return Response({'team': serializer.data, 'pilots': serializer1.data})


@api_view(['GET'])
def search_team(req):
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


@api_view(['GET'])
def get_teams(req):
    teams = Team.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def new_team(req):
    serializer = TeamSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_team(req):
    id = str(req.GET['id'])
    try:
        team = Team.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = TeamSerializer(team, data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TeamLeader

@api_view(['GET'])
def get_teamleaders(req):
    teamleaders = TeamLeader.objects.all()
    serializer = TeamLeaderSerializer(teamleaders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def search_teamleader(req):
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


@api_view(['GET'])
def get_teamleader(req):
    id = str(req.GET['id'])
    try:
        teamleader = TeamLeader.objects.get(id=id)
    except TeamLeader.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = TeamLeaderSerializer(teamleader)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def new_teamleader(req):
    serializer = TeamLeaderSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_teamleader(req):
    id = str(req.GET['id'])
    try:
        teamleader = TeamLeader.objects.get(id=id)
    except TeamLeader.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = TeamLeaderSerializer(teamleader, data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def template_index(req):
    return render(req, 'template_index.html')
