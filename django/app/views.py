from django.contrib.auth import authenticate, login, get_user
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.shortcuts import render, redirect

from app.models import *
from app.forms import *


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

def cars_list(req):
    cars = Car.objects.all()
    actions = [{'str': 'Search Car', 'url': '/cars/search'}]
    if req.user.is_authenticated and req.user.username == 'admin':
        actions += [{'str': 'New Car', 'url': '/cars/new'}]
    lst = [[{'str': c.model, 'url': f'/cars/{c.id}'}] for c in cars]

    ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
        -1] if req.user.is_authenticated else None,
           'header': 'Cars', 'actions': actions, 'list': lst}
    return render(req, 'list.html', ctx)


def cars_new(req):
    if req.method == 'POST':
        form = CarForm(req.POST)
        if form.is_valid():
            Car.objects.create(
                model=form.cleaned_data['model'],
                engine=form.cleaned_data['engine'],
                weight=form.cleaned_data['weight'],
                pilot=form.cleaned_data['pilot']
            )

            return redirect('cars_list')
    else:
        form = CarForm()
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'New Car', 'form': form}
        return render(req, 'new.html', ctx)


def cars_search(req):
    if req.method == 'POST':
        form = CarSearchForm(req.POST)
        if form.is_valid():
            model = form.cleaned_data['model']
            pilot = form.cleaned_data['pilot']

            query = f'Car.model={model};Car.pilot={pilot}'
            if 'searched' in req.session:
                # print('I entered searched.')
                if query in req.session['searched'].keys():
                    lst = req.session['searched'][query]
                    # print("I entered cache")
                    # print(req.session['searched'].keys())
                else:
                    # print("I entered query")
                    model = form.cleaned_data['model']
                    pilot = form.cleaned_data['pilot']
                    cars = Car.objects.filter(Q(model__icontains=model)
                                              & Q(pilot__name__icontains=pilot))
                    lst = [[{'str': c.model, 'url': f'/cars/{c.id}'}] for c in cars]

                    # print(len(req.session['searched'].keys()))
                    if len(req.session['searched'].keys()) >= 10:
                        # print("I entered removed")
                        # removes first added element to cache
                        (k := next(iter(req.session['searched'])), req.session['searched'].pop(k))

                    req.session['searched'][query] = lst
                    req.session.save()
                    # print("Just added and saved session")
            else:
                # print("I entered have to initialize searched")
                req.session['searched'] = dict()
                # make query
                model = form.cleaned_data['model']
                pilot = form.cleaned_data['pilot']
                cars = Car.objects.filter(Q(model__icontains=model)
                                          & Q(pilot__name__icontains=pilot))
                lst = [[{'str': c.model, 'url': f'/cars/{c.id}'}] for c in cars]
                req.session['searched'][query] = lst
            ctx = {
                'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
                    -1] if req.user.is_authenticated else None,
                'header': 'List of Cars', 'list': lst, 'query': f'Model {model}; Pilot {pilot}'}
            return render(req, 'list.html', ctx)
    else:
        form = CarSearchForm()
        cars = Car.objects.all()
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'Search Car', 'form': form, 'options': cars, 'id_field': 'id_model', 'id_field2': 'id_pilot'}
        return render(req, 'search.html', ctx)


def cars_get(req, _id):
    car = Car.objects.get(id=_id)

    ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
        -1] if req.user.is_authenticated else None,
           'header': 'Car Details', 'car': car}
    return render(req, 'car.html', ctx)


def cars_edit(req, _id):
    car = Car.objects.get(id=_id)
    if req.method == 'POST':
        form = CarForm(req.POST)
        if form.is_valid():
            car.model = form.cleaned_data['model']
            car.engine = form.cleaned_data['engine']
            car.weight = form.cleaned_data['weight']
            car.pilot = form.cleaned_data['pilot']
            car.save()

            return redirect('cars_get', _id=_id)
    else:
        form = CarForm(initial={
            'model': car.model,
            'engine': car.engine,
            'weight': car.weight,
            'pilot': car.pilot})
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'Edit Car', 'form': form}
        return render(req, 'edit.html', ctx)


# Circuit

def circuits_list(req):
    circuits = Circuit.objects.all()
    actions = [{'str': 'Search Circuit', 'url': '/circuits/search'}]
    if req.user.is_authenticated and req.user.username == 'admin':
        actions += [{'str': 'New Circuit', 'url': '/circuits/new'}]
    lst = [[{'str': c.name, 'url': f'/circuits/{c.id}'}] for c in circuits]

    ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
        -1] if req.user.is_authenticated else None,
           'header': 'List of Circuits', 'actions': actions, 'list': lst}
    return render(req, 'list.html', ctx)


def circuits_search(req):
    # If POST request, process form data
    if req.method == 'POST':
        # Create a form instance and pass data to it
        form = CircuitSearchForm(req.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

            query = f'Circuit.name={name}'
            if 'searched' in req.session:
                # print('I entered searched.')
                if query in req.session['searched'].keys():
                    lst = req.session['searched'][query]
                    # print("I entered cache")
                    # print(req.session['searched'].keys())
                else:
                    # print("I entered query")
                    circuits = Circuit.objects.filter(name__icontains=name)
                    lst = [[{'str': p.name, 'url': f'/circuits/{p.id}'}]
                           for p in circuits]
                    # print(len(req.session['searched'].keys()))
                    if len(req.session['searched'].keys()) >= 10:
                        # print("I entered removed")
                        # removes first added element to cache
                        (k := next(iter(req.session['searched'])), req.session['searched'].pop(k))

                    req.session['searched'][query] = lst
                    req.session.save()
                    # print("Just added and saved session")
            else:
                # print("I entered have to initialize searched")
                req.session['searched'] = dict()
                # make query
                circuits = Circuit.objects.filter(name__icontains=name)
                lst = [[{'str': p.name, 'url': f'/circuits/{p.id}'}]
                       for p in circuits]
                req.session['searched'][query] = lst

            ctx = {
                'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
                    -1] if req.user.is_authenticated else None,
                'header': 'List of Circuits', 'list': lst, 'query': name}
            return render(req, 'list.html', ctx)
    else:
        # If GET (or any other method), create blank form
        form = CircuitSearchForm()
        circuits = Circuit.objects.all()
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'Search Circuit', 'form': form, 'options': circuits, 'id_field': 'id_name'}
        return render(req, 'search.html', ctx)


def circuits_get(req, _id):
    circuit = Circuit.objects.get(id=_id)
    races = Race.objects.filter(circuit=circuit)
    ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
        -1] if req.user.is_authenticated else None,
           'header': 'Circuit Details', 'circuit': circuit, 'races': races}
    return render(req, 'circuit.html', ctx)


def circuits_new(req):
    if not req.user.is_authenticated or req.user.username != 'admin':
        return redirect('login')
    if req.method == 'POST':
        form = CircuitForm(req.POST)
        if form.is_valid():
            Circuit.objects.create(
                name=form.cleaned_data['name'],
                length=form.cleaned_data['length'],
                location=form.cleaned_data['location'],
                last_winner=form.cleaned_data['last_winner'],
                country=form.cleaned_data['country'],
            )

            return redirect('circuits_list')
    else:
        form = CircuitForm()
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'New Circuit', 'form': form}
        return render(req, 'new.html', ctx)


def circuits_edit(req, _id):
    if not req.user.is_authenticated or req.user.username != 'admin':
        return redirect('login')
    circuit = Circuit.objects.get(id=_id)
    if req.method == 'POST':
        form = CircuitForm(req.POST)
        if form.is_valid():
            circuit.name = form.cleaned_data['name']
            circuit.length = form.cleaned_data['length']
            circuit.location = form.cleaned_data['location']
            circuit.last_winner = form.cleaned_data['last_winner']
            circuit.country = form.cleaned_data['country']
            circuit.save()

            return redirect('circuits_get', _id=_id)
    else:
        form = CircuitForm(initial={
            'name': circuit.name,
            'length': circuit.length,
            'location': circuit.location,
            'last_winner': circuit.last_winner,
            'country': circuit.country.id
        })
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'Edit Circuit', 'form': form}
        return render(req, 'edit.html', ctx)


# Country

def countries_list(req):
    countries = Country.objects.all()
    actions = [{'str': 'Search Country', 'url': '/countries/search'}]
    if req.user.is_authenticated and req.user.username == 'admin':
        actions += [{'str': 'New Country', 'url': '/countries/new'}]
    lst = [[{'str': c.designation, 'url': f'/countries/{c.id}'}] for c in countries]
    ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
        -1] if req.user.is_authenticated else None,
           'header': 'Countries', 'actions': actions, 'list': lst}
    return render(req, 'list.html', ctx)


def countries_get(req, _id):
    country = Country.objects.get(id=_id)

    circuits = Circuit.objects.filter(country=country)
    pilots = Pilot.objects.filter(country=country)

    ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
        -1] if req.user.is_authenticated else None,
           'header': 'Country Details', 'country': country, 'circuits': circuits, 'pilots': pilots}
    return render(req, 'country.html', ctx)


def countries_new(req):
    if not req.user.is_authenticated or req.user.username != 'admin':
        return redirect('login')
    if req.method == 'POST':
        form = CountryForm(req.POST)
        if form.is_valid():
            Country.objects.create(
                designation=form.cleaned_data['designation'],
                code=form.cleaned_data['code']
            )

            return redirect('countries_list')
    else:
        form = CountryForm()
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'New Country', 'form': form}
        return render(req, 'new.html', ctx)


def countries_search(req):
    if req.method == 'POST':
        form = CountrySearchForm(req.POST)
        if form.is_valid():
            designation = form.cleaned_data['designation']

            query = f'Country.designation={designation}'
            if 'searched' in req.session:
                # print('I entered searched.')
                if query in req.session['searched'].keys():
                    lst = req.session['searched'][query]
                    # print("I entered cache")
                    # print(req.session['searched'].keys())
                else:
                    # print("I entered query")
                    countries = Country.objects.filter(designation__icontains=designation)

                    lst = [[{'str': c.designation, 'url': f'/countries/{c.id}'}]
                           for c in countries]
                    # print(len(req.session['searched'].keys()))
                    if len(req.session['searched'].keys()) >= 10:
                        # print("I entered removed")
                        # removes first added element to cache
                        (k := next(iter(req.session['searched'])), req.session['searched'].pop(k))

                    req.session['searched'][query] = lst
                    req.session.save()
                    # print("Just added and saved session")
            else:
                # print("I entered have to initialize searched")
                req.session['searched'] = dict()
                # make query
                countries = Country.objects.filter(designation__icontains=designation)

                lst = [[{'str': c.designation, 'url': f'/countries/{c.id}'}]
                       for c in countries]
                req.session['searched'][query] = lst

            ctx = {
                'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
                    -1] if req.user.is_authenticated else None,
                'header': 'Countries', 'list': lst, 'query': designation}
            return render(req, 'list.html', ctx)
    else:
        form = CountrySearchForm()
        countries = Country.objects.all()
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'Search Country', 'form': form, 'options': countries, 'id_field': 'id_designation'}
        return render(req, 'search.html', ctx)


def countries_edit(req, _id):
    if not req.user.is_authenticated or req.user.username != 'admin':
        return redirect('login')
    country = Country.objects.get(id=_id)
    if req.method == 'POST':
        form = CountryForm(req.POST)
        if form.is_valid():
            country.designation = form.cleaned_data['designation']
            country.code = form.cleaned_data['code']
            country.save()

            return redirect('countries_get', _id=_id)
    else:
        form = CountryForm(initial={
            'designation': country.designation,
            'code': country.code
        })
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'Edit Country', 'form': form}
        return render(req, 'edit.html', ctx)


# Pilot

def pilots_list(req):
    pilots = Pilot.objects.all()
    actions = [{'str': 'Search Pilot', 'url': '/pilots/search'}]
    if req.user.is_authenticated and req.user.username == 'admin':
        actions += [{'str': 'New Pilot', 'url': '/pilots/new'}]

    lst = [[{'str': p.name, 'url': f'/pilots/{p.id}'}] for p in pilots]

    ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
        -1] if req.user.is_authenticated else None,
           'header': 'List of Pilots', 'actions': actions, 'list': lst}
    return render(req, 'list.html', ctx)


def pilots_search(req):
    # If POST request, process form data
    if req.method == 'POST':
        # Create a form instance and pass data to it
        form = PilotSearchForm(req.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            query = f'Pilot.name={name}'
            if 'searched' in req.session:
                # print('I entered searched.')
                if query in req.session['searched'].keys():
                    lst = req.session['searched'][query]
                    # print("I entered cache")
                    # print(req.session['searched'].keys())
                else:
                    # print("I entered query")
                    pilots = Pilot.objects.filter(name__icontains=name)
                    lst = [[{'str': p.name, 'url': f'/pilots/{p.id}'}]
                           for p in pilots]
                    # print(len(req.session['searched'].keys()))
                    if len(req.session['searched'].keys()) >= 10:
                        # print("I entered removed")
                        # removes first added element to cache
                        (k := next(iter(req.session['searched'])), req.session['searched'].pop(k))

                    req.session['searched'][query] = lst
                    req.session.save()
                    # print("Just added and saved session")
            else:
                # print("I entered have to initialize searched")
                req.session['searched'] = dict()
                # make query
                pilots = Pilot.objects.filter(name__icontains=name)
                lst = [[{'str': p.name, 'url': f'/pilots/{p.id}'}]
                       for p in pilots]
                req.session['searched'][query] = lst

            ctx = {
                'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
                    -1] if req.user.is_authenticated else None,
                'header': 'List of Pilots', 'list': lst, 'query': name}
            return render(req, 'list.html', ctx)
    else:
        # If GET (or any other method), create blank form
        pilots = Pilot.objects.all()
        form = PilotSearchForm()
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'Search Pilot', 'form': form, 'options': pilots, 'id_field': "id_name"}
        return render(req, 'search.html', ctx)


def pilots_get(req, _id):
    pilot = Pilot.objects.get(id=_id)
    faved = None
    if not isinstance(get_user(req), AnonymousUser):
        if pilot in Profile.objects.get(user=get_user(req)).favourite_pilot.all():
            faved = True
        else:
            faved = False

    image = "/static/images/" + pilot.name + ".png"
    dislike_image = "/static/images/like_button.png"
    like_image = "/static/images/dislike_button.png"

    results = Result.objects.filter(pilot=pilot).order_by('-race__date')
    ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
        -1] if req.user.is_authenticated else None,
           'header': 'Pilot Details', 'pilot': pilot, 'pilot_image': image, 'results': results, 'favourite': faved,
           'dislike_image': dislike_image, 'like_image': like_image}
    return render(req, 'pilot.html', ctx)


def pilots_new(req):
    if not req.user.is_authenticated or req.user.username != 'admin':
        return redirect('login')
    if req.method == 'POST':
        form = PilotForm(req.POST)
        if form.is_valid():
            pilot = Pilot.objects.create(
                name=form.cleaned_data['name'],
                date=form.cleaned_data['date'],
                victories=form.cleaned_data['victories'],
                pole_positions=form.cleaned_data['pole_positions'],
                podiums=form.cleaned_data['podiums'],
                championships=form.cleaned_data['championships'],
                contract=form.cleaned_data['contract'],
                entry_year=form.cleaned_data['entry_year'],
                team=form.cleaned_data['team']
            )
            pilot.country.set(form.cleaned_data['country'])

            return redirect('pilots_list')
    else:
        form = PilotForm()
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'New Pilot', 'form': form}
        return render(req, 'new.html', ctx)


def pilots_edit(req, _id):
    if not req.user.is_authenticated or req.user.username != 'admin':
        return redirect('login')
    pilot = Pilot.objects.get(id=_id)
    if req.method == 'POST':
        form = PilotForm(req.POST)
        if form.is_valid():
            pilot.name = form.cleaned_data['name']
            pilot.date = form.cleaned_data['date']
            pilot.victories = form.cleaned_data['victories']
            pilot.pole_positions = form.cleaned_data['pole_positions']
            pilot.podiums = form.cleaned_data['podiums']
            pilot.championships = form.cleaned_data['championships']
            pilot.contract = form.cleaned_data['contract']
            pilot.entry_year = form.cleaned_data['entry_year']
            pilot.team = form.cleaned_data['team']
            pilot.country.set(form.cleaned_data['country'])
            pilot.save()

            return redirect('pilots_get', _id=_id)
    else:
        form = PilotForm(initial={
            'name': pilot.name,
            'date': pilot.date,
            'victories': pilot.victories,
            'pole_positions': pilot.pole_positions,
            'podiums': pilot.podiums,
            'championships': pilot.championships,
            'contract': pilot.contract,
            'entry_year': pilot.entry_year,
            'team': pilot.team.id,
            'country': [c.id for c in pilot.country.all()]
        })
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'Edit Pilot', 'form': form}
        return render(req, 'edit.html', ctx)


# Race

def races_list(req):
    races = Race.objects.all()
    actions = [{'str': 'Search Race', 'url': '/races/search'}]
    if req.user.is_authenticated and req.user.username == 'admin':
        actions += [{'str': 'New Race', 'url': '/races/new'}]
    lst = [[{'str': r.name, 'url': f'/races/{r.id}'}] for r in races]

    ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
        -1] if req.user.is_authenticated else None,
           'header': 'List of Races', 'actions': actions, 'list': lst}
    return render(req, 'list.html', ctx)


def races_search(req):
    # If POST request, process form data
    if req.method == 'POST':
        # Create a form instance and pass data to it
        form = RaceSearchForm(req.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

            query = f'Race.name={name}'
            if 'searched' in req.session:
                # print('I entered searched.')
                if query in req.session['searched'].keys():
                    lst = req.session['searched'][query]
                    # print("I entered cache")
                    # print(req.session['searched'].keys())
                else:
                    # print("I entered query")
                    races = Race.objects.filter(name__icontains=name)
                    lst = [[{'str': r.name, 'url': f'/races/{r.id}'}]
                           for r in races]
                    # print(len(req.session['searched'].keys()))
                    if len(req.session['searched'].keys()) >= 10:
                        # print("I entered removed")
                        # removes first added element to cache
                        (k := next(iter(req.session['searched'])), req.session['searched'].pop(k))

                    req.session['searched'][query] = lst
                    req.session.save()
                    # print("Just added and saved session")
            else:
                # print("I entered have to initialize searched")
                req.session['searched'] = dict()
                # make query
                races = Race.objects.filter(name__icontains=name)
                lst = [[{'str': r.name, 'url': f'/races/{r.id}'}]
                       for r in races]
                req.session['searched'][query] = lst

            ctx = {
                'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
                    -1] if req.user.is_authenticated else None,
                'header': 'List of Races', 'list': lst, 'query': name}
            return render(req, 'list.html', ctx)
    else:
        # If GET (or any other method), create blank form
        form = RaceSearchForm()
        races = Race.objects.all()
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'Search Race', 'form': form, 'options': races, 'id_field': "id_name"}
        return render(req, 'search.html', ctx)


def races_get(req, _id):
    race = Race.objects.get(id=_id)
    results = Result.objects.filter(race=race).order_by('position')

    ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
        -1] if req.user.is_authenticated else None,
           'header': 'Race Details', 'race': race, 'results': results}
    return render(req, 'race.html', ctx)


def races_new(req):
    if not req.user.is_authenticated or req.user.username != 'admin':
        return redirect('login')
    if req.method == 'POST':
        form = RaceForm(req.POST)
        if form.is_valid():
            Race.objects.create(
                name=form.cleaned_data['name'],
                date=form.cleaned_data['date'],
                season=form.cleaned_data['season'],
                fast_lap=form.cleaned_data['fast_lap'],
                circuit=form.cleaned_data['circuit'],
            )

            return redirect('races_list')
    else:
        form = RaceForm()
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'New Race', 'form': form}
        return render(req, 'new.html', ctx)


def races_edit(req, _id):
    if not req.user.is_authenticated or req.user.username != 'admin':
        return redirect('login')
    race = Race.objects.get(id=_id)
    if req.method == 'POST':
        form = RaceForm(req.POST)
        if form.is_valid():
            race.name = form.cleaned_data['name']
            race.date = form.cleaned_data['date']
            race.season = form.cleaned_data['season']
            race.fast_lap = form.cleaned_data['fast_lap']
            race.circuit = form.cleaned_data['circuit']
            race.save()

            return redirect('races_get', _id=_id)
    else:
        form = RaceForm(initial={
            'name': race.name,
            'date': race.date,
            'season': race.season,
            'fast_lap': race.fast_lap,
            'circuit': race.circuit.id
        })
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'Edit Race', 'form': form}
        return render(req, 'edit.html', ctx)


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


def results_get(req, _id):
    result = Result.objects.get(id=_id)

    ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
        -1] if req.user.is_authenticated else None,
           'header': 'Result Details', 'result': result}
    return render(req, 'result.html', ctx)


def results_new(req):
    if not req.user.is_authenticated or req.user.username != 'admin':
        return redirect('login')
    if req.method == 'POST':
        form = ResultForm(req.POST)
        if form.is_valid():
            result = Result.objects.create(
                position=form.cleaned_data['position'],
                pilot=form.cleaned_data['pilot'],
                race=form.cleaned_data['race'],
                points=form.cleaned_data['points']
            )

            return redirect('races_get', _id=result.race.id)
    else:
        form = ResultForm()
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'New Result', 'form': form}
        return render(req, 'new.html', ctx)


def results_edit(req, _id):
    if not req.user.is_authenticated or req.user.username != 'admin':
        return redirect('login')
    result = Result.objects.get(id=_id)
    if req.method == 'POST':
        form = ResultForm(req.POST)
        if form.is_valid():
            result.position = form.cleaned_data['position']
            result.pilot = form.cleaned_data['pilot']
            result.race = form.cleaned_data['race']
            result.points = form.cleaned_data['points']
            result.save()

            return redirect('races_get', _id=result.race.id)
    else:
        form = ResultForm(initial={
            'position': result.position,
            'pilot': result.pilot,
            'race': result.race,
            'points': result.points
        })
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'Edit Result', 'form': form}
        return render(req, 'edit.html', ctx)


# Team

def teams_list(req):
    teams = Team.objects.all()
    actions = [{'str': 'Search Team', 'url': '/teams/search'}]
    if req.user.is_authenticated and req.user.username == 'admin':
        actions += [{'str': 'New Team', 'url': '/teams/new'}]
    lst = [[{'str': t.name, 'url': f'/teams/{t.id}'}] for t in teams]

    ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
        -1] if req.user.is_authenticated else None,
           'header': 'List of Teams', 'actions': actions, 'list': lst}
    return render(req, 'list.html', ctx)


def teams_search(req):
    # If POST request, process form data
    if req.method == 'POST':
        # Create a form instance and pass data to it
        form = TeamSearchForm(req.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

            query = f'Team.name={name}'

            if 'searched' in req.session:
                # print('I entered searched.')
                if query in req.session['searched'].keys():
                    lst = req.session['searched'][query]
                    # print("I entered cache")
                    # print(req.session['searched'].keys())
                else:
                    # print("I entered query")
                    teams = Team.objects.filter(name__icontains=name)
                    lst = [[{'str': t.name, 'url': f'/teams/{t.id}'}]
                           for t in teams]
                    # print(len(req.session['searched'].keys()))
                    if len(req.session['searched'].keys()) >= 10:
                        # print("I entered removed")
                        # removes first added element to cache
                        (k := next(iter(req.session['searched'])), req.session['searched'].pop(k))

                    req.session['searched'][query] = lst
                    req.session.save()
                    # print("Just added and saved session")
            else:
                # print("I entered have to initialize searched")
                req.session['searched'] = dict()
                # make query
                teams = Team.objects.filter(name__icontains=name)
                lst = [[{'str': t.name, 'url': f'/teams/{t.id}'}]
                       for t in teams]
                req.session['searched'][query] = lst

            ctx = {
                'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
                    -1] if req.user.is_authenticated else None,
                'header': 'List of Teams', 'list': lst, 'query': name}
            return render(req, 'list.html', ctx)
    else:
        # If GET (or any other method), create blank form
        form = TeamSearchForm()
        teams = Team.objects.all()
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'Search Team', 'form': form, 'options': teams, 'id_field': "id_name"}
        return render(req, 'search.html', ctx)


def teams_get(req, _id):
    team = Team.objects.get(id=_id)

    faved = None
    if not isinstance(get_user(req), AnonymousUser):
        if team in Profile.objects.get(user=get_user(req)).favourite_team.all():
            faved = True
        else:
            faved = False

    dislike_image = "/static/images/like_button.png"
    like_image = "/static/images/dislike_button.png"
    image = "/static/images/" + team.name + ".png"

    pilots = Pilot.objects.filter(team=team)

    team_points = sum([p.total_points for p in pilots])

    ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
        -1] if req.user.is_authenticated else None,
           'header': 'Team Details', 'team': team, 'team_image': image, 'pilots': pilots, 'team_points': team_points,
           'favourite': faved, 'dislike_image': dislike_image, 'like_image': like_image}
    return render(req, 'team.html', ctx)


def teams_new(req):
    if not req.user.is_authenticated or req.user.username != 'admin':
        return redirect('login')
    if req.method == 'POST':
        form = TeamForm(req.POST)
        if form.is_valid():
            Team.objects.create(
                name=form.cleaned_data['name'],
                date=form.cleaned_data['date'],
                championships=form.cleaned_data['championships']
            )

            return redirect('teams_list')
    else:
        form = TeamForm()
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'New Team', 'form': form}
        return render(req, 'new.html', ctx)


def teams_edit(req, _id):
    if not req.user.is_authenticated or req.user.username != 'admin':
        return redirect('login')
    team = Team.objects.get(id=_id)
    if req.method == 'POST':
        form = TeamForm(req.POST)
        if form.is_valid():
            team.name = form.cleaned_data['name']
            team.date = form.cleaned_data['date']
            team.championships = form.cleaned_data['championships']
            team.save()

            return redirect('teams_get', _id=_id)
    else:
        form = TeamForm(initial={
            'name': team.name,
            'date': team.date,
            'championships': team.championships
        })
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'Edit Team', 'form': form}
        return render(req, 'edit.html', ctx)


# TeamLeader

def teamleaders_list(req):
    teamleaders = TeamLeader.objects.all()
    actions = [{'str': 'Search Team Leader', 'url': '/teamleaders/search'}]
    if req.user.is_authenticated and req.user.username == 'admin':
        actions += [{'str': 'New Team Leader', 'url': '/teamleaders/new'}]
    lst = [[{'str': tl.name, 'url': f'/teamleaders/{tl.id}'}] for tl in teamleaders]

    ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
        -1] if req.user.is_authenticated else None,
           'header': 'List of Team Leaders', 'actions': actions, 'list': lst}
    return render(req, 'list.html', ctx)


def teamleaders_search(req):
    # If POST request, process form data
    if req.method == 'POST':
        # Create a form instance and pass data to it
        form = TeamLeaderSearchForm(req.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

            query = f'TeamLeader.name={name}'
            if 'searched' in req.session:
                # print('I entered searched.')
                if query in req.session['searched'].keys():
                    lst = req.session['searched'][query]
                    # print("I entered cache")
                    # print(req.session['searched'].keys())
                else:
                    # print("I entered query")
                    teamleaders = TeamLeader.objects.filter(name__icontains=name)

                    lst = [[{'str': tl.name, 'url': f'/teamleaders/{tl.id}'}]
                           for tl in teamleaders]
                    # print(len(req.session['searched'].keys()))
                    if len(req.session['searched'].keys()) >= 10:
                        # print("I entered removed")
                        # removes first added element to cache
                        (k := next(iter(req.session['searched'])), req.session['searched'].pop(k))

                    req.session['searched'][query] = lst
                    req.session.save()
                    # print("Just added and saved session")
            else:
                print("I entered have to initialize searched")
                req.session['searched'] = dict()
                # make query
                teamleaders = TeamLeader.objects.filter(name__icontains=name)

                lst = [[{'str': tl.name, 'url': f'/teamleaders/{tl.id}'}]
                       for tl in teamleaders]
                req.session['searched'][query] = lst
            ctx = {
                'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
                    -1] if req.user.is_authenticated else None,
                'header': 'List of Team Leaders', 'list': lst, 'query': name}
            return render(req, 'list.html', ctx)
    else:
        # If GET (or any other method), create blank form
        form = TeamLeaderSearchForm()
        teamleadres = TeamLeader.objects.all()
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'Search Team Leader', 'form': form, 'options': teamleadres, 'id_field': "id_name"}
        return render(req, 'search.html', ctx)


def teamleaders_get(req, _id):
    teamleader = TeamLeader.objects.get(id=_id)
    image = "/static/images/" + teamleader.name + ".jpeg"
    ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
        -1] if req.user.is_authenticated else None,
           'header': 'Team Leader Details', 'teamleader': teamleader, 'teamleader_image': image}
    return render(req, 'teamleader.html', ctx)


def teamleaders_new(req):
    if not req.user.is_authenticated or req.user.username != 'admin':
        return redirect('login')
    if req.method == 'POST':
        form = TeamLeaderForm(req.POST)
        if form.is_valid():
            TeamLeader.objects.create(
                name=form.cleaned_data['name'],
                team=form.cleaned_data['team']
            )

            return redirect('teamleaders_list')
    else:
        form = TeamLeaderForm()
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'New Team Leader', 'form': form}
        return render(req, 'new.html', ctx)


def teamleaders_edit(req, _id):
    if not req.user.is_authenticated or req.user.username != 'admin':
        return redirect('login')
    teamleader = TeamLeader.objects.get(id=_id)
    if req.method == 'POST':
        form = TeamLeaderForm(req.POST)
        if form.is_valid():
            teamleader.name = form.cleaned_data['name']
            teamleader.team = form.cleaned_data['team']
            teamleader.save()

            return redirect('teamleaders_get', _id=_id)
    else:
        form = TeamLeaderForm(initial={
            'name': teamleader.name,
            'team': teamleader.team.id
        })
        ctx = {'image': 'images/profiles/' + Profile.objects.get(user=get_user(req)).profile_image.url.split('/')[
            -1] if req.user.is_authenticated else None,
               'header': 'Edit Team Leader', 'form': form}
        return render(req, 'edit.html', ctx)


def template_index(req):
    return render(req, 'template_index.html')
