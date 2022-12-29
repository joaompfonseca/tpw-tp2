from django.contrib.auth import authenticate, login, get_user
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from app.models import *
from app.forms import *
from app.serializers import *

# Create your views here.

# Home

def home(req):
    pilots_leaderboard = []
    teams_leaderboard = []

    stats = {'total_races': Race.objects.count(),
             'total_pilots': Pilot.objects.count(), 'total_teams': Team.objects.count()}
    for pilot in Pilot.objects.all():
        pilots_leaderboard.append({'pilot': pilot, 'points': pilot.total_points})
    pilots_leaderboard.sort(key=lambda x: x['points'], reverse=True)

    for team in Team.objects.all():
        teams_leaderboard.append({'team': team,
                                  'points': sum([pilot.total_points for pilot in Pilot.objects.filter(team=team)])})
    teams_leaderboard.sort(key=lambda x: x['points'], reverse=True)
    ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
        -1] if req.user.is_authenticated else None,
           'pilots_leaderboard': pilots_leaderboard, 'stats': stats, 'teams_leaderboard': teams_leaderboard}
    return render(req, 'home.html', ctx)


# Auth
def signup(req):
    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            Profile.objects.create(user=user,
                                   profile_image='/images/profiles/profile.jpg')

            login(req, user)
            return redirect('home')
        else:
            ctx = {
                'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
                    -1] if req.user.is_authenticated else None,
                'form': form}
            return render(req, 'signup.html', ctx)
    else:
        form = UserCreationForm()
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'form': form}
        return render(req, 'signup.html', ctx)


# Profile
def profile(req):
    user_profile = Profile.objects.get(user=get_user(req))
    ctx = {'image': 'images/profiles/' + user_profile.profile_image.url.split('/')[
        -1] if req.user.is_authenticated else None,
           'biography': user_profile.biography,
           'pilots': user_profile.favourite_pilot,
           'teams': user_profile.favourite_team,
           'user_id': user_profile.id}
    return render(req, 'profile.html', ctx)


def profile_edit(req):
    if not req.user.is_authenticated:
        return redirect('login')
    user_profile = Profile.objects.get(user=get_user(req))
    if req.method == 'POST':
        form = ProfileForm(req.POST, req.FILES)
        if form.is_valid() or req.POST.get('profile_image') == '':
            user_profile.user.first_name = form.cleaned_data['first_name']
            user_profile.user.last_name = form.cleaned_data['last_name']
            user_profile.user.email = form.cleaned_data['email']
            user_profile.user.save()
            if req.POST.get('profile_image') != '':
                user_profile.profile_image = form.cleaned_data['profile_image']
            user_profile.biography = form.cleaned_data['biography']
            user_profile.save()

            return redirect('profile')
    else:
        form = ProfileForm(initial={
            'first_name': user_profile.user.first_name,
            'last_name': user_profile.user.last_name,
            'email': user_profile.user.email,
            'profile_image': user_profile.profile_image,
            'biography': user_profile.biography
        })
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'Edit Profile', 'form': form}
        return render(req, 'edit.html', ctx)


# Pilot Favourites
def pilot_add_to_favourite(req, pilot_id):
    user_profile = Profile.objects.get(user=get_user(req))
    pilot = Pilot.objects.get(id=pilot_id)
    user_profile.favourite_pilot.add(pilot)
    user_profile.save()
    return redirect('pilots_get', _id=pilot_id)


def pilot_remove_from_favourite(req, pilot_id):
    user_profile = Profile.objects.get(user=get_user(req))
    pilot = Pilot.objects.get(id=pilot_id)
    user_profile.favourite_pilot.remove(pilot)
    user_profile.save()
    return redirect('pilots_get', _id=pilot_id)


# Team Favourites
def team_add_to_favourite(req, team_id):
    user_profile = Profile.objects.get(user=get_user(req))
    team = Team.objects.get(id=team_id)
    user_profile.favourite_team.add(team)
    user_profile.save()
    return redirect('teams_get', _id=team_id)


def team_remove_from_favourite(req, team_id):
    user_profile = Profile.objects.get(user=get_user(req))
    team = Team.objects.get(id=team_id)
    user_profile.favourite_team.remove(team)
    user_profile.save()
    return redirect('teams_get', _id=team_id)


# Car

@api_view(['GET'])
def get_cars(req):
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)

@api_view(['POST'])
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
    serializer1 = RaceSerializer(races,many=True)
    return Response({'circuit': serializer.data,'races': serializer1.data})


@api_view(['POST'])
def new_circuit(req):
    #if not req.user.is_authenticated or req.user.username != 'admin':
    #    return redirect('login')
    serializer = CircuitSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_circuit(req):
    #if not req.user.is_authenticated or req.user.username != 'admin':
    #    return redirect('login')
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
def new_country(req):
    #if not req.user.is_authenticated or req.user.username != 'admin':
    #    return redirect('login')
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
def update_country(req):
    #if not req.user.is_authenticated or req.user.username != 'admin':
    #    return redirect('login')
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
        pilot = Pilot.objects.get(id=id)
        results = Result.objects.filter(pilot=pilot).order_by('-race__date')
    except Pilot.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PilotSerializer(pilot)
    serializer1 = ResultSerializer(results, many=True)
    return Response({'pilot': serializer.data, 'results': serializer1.data})


##def pilots_get(req, _id):
##    pilot = Pilot.objects.get(id=_id)
##    faved = None
##    if not isinstance(get_user(req), AnonymousUser):
##        if pilot in Profile.objects.get(user=get_user(req)).favourite_pilot.all():
##            faved = True
##        else:
##            faved = False
##
##    image = "/static/images/" + pilot.name + ".png"
##    dislike_image = "/static/images/like_button.png"
##    like_image = "/static/images/dislike_button.png"
##
##    results = Result.objects.filter(pilot=pilot).order_by('-race__date')
##    ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
##        -1] if req.user.is_authenticated else None,
##           'header': 'Pilot Details', 'pilot': pilot, 'pilot_image': image, 'results': results, 'favourite': faved,
##           'dislike_image': dislike_image, 'like_image': like_image}
##    return render(req, 'pilot.html', ctx)


@api_view(['POST'])
def add_pilot(req):
    #if not req.user.is_authenticated or req.user.username != 'admin':
    #    return redirect('login')
    serializer = PilotSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_pilot(req):
    #if not req.user.is_authenticated or req.user.username != 'admin':
    #    return redirect('login')
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
def new_race(req):
    #if not req.user.is_authenticated or req.user.username != 'admin':
    #    return redirect('login')
    serializer = RaceSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_race(req):
    #if not req.user.is_authenticated or req.user.username != 'admin':
    #    return redirect('login')
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
def new_result(req):
    #if not req.user.is_authenticated or req.user.username != 'admin':
    #    return redirect('login')
    serializer = ResultSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_result(req):
    #if not req.user.is_authenticated or req.user.username != 'admin':
    #    return redirect('login')
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
    #faved = None
    #if not isinstance(get_user(req), AnonymousUser):
    #    if team in Profile.objects.get(user=get_user(req)).favourite_team.all():
    #        faved = True
    #    else:
    #        faved = False
    id = str(req.GET['id'])
    try:
        team = Team.objects.get(id=id)
        pilots = Pilot.objects.filter(team=team)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = TeamSerializer(team)
    serializer1 = PilotSerializer(pilots, many=True)
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
def new_team(req):
    #if not req.user.is_authenticated or req.user.username != 'admin':
    #    return redirect('login')
    serializer = TeamSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_team(req):
    #if not req.user.is_authenticated or req.user.username != 'admin':
    #    return redirect('login')
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
def new_teamleader(req):
    #if not req.user.is_authenticated or req.user.username != 'admin':
    #    return redirect('login')
    serializer = TeamLeaderSerializer(data=req.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def update_teamleader(req):
    #if not req.user.is_authenticated or req.user.username != 'admin':
    #    return redirect('login')
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
