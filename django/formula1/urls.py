"""formula1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    # Auth
    path('ws/login', views.LoginAPI.as_view()),
    path('ws/logout', views.LogoutAPI.as_view()),
    path('ws/signup', views.RegisterAPI.as_view()),
    path('ws/user', views.user_get),
    # Car
    path('ws/car', views.car_get),
    path('ws/cars', views.cars_get),
    path('ws/carsearch', views.car_search),
    path('ws/carcreate', views.car_create),
    path('ws/carupdate', views.car_update),
    # Circuit
    path('ws/circuit', views.circuit_get),
    path('ws/circuits', views.circuits_get),
    path('ws/circuitsearch', views.circuit_search),
    path('ws/circuitcreate', views.circuit_create),
    path('ws/circuitupdate', views.circuit_update),
    # Country
    path('ws/country', views.country_get),
    path('ws/countries', views.countries_get),
    path('ws/countrysearch', views.country_search),
    path('ws/countrycreate', views.country_create),
    path('ws/countryupdate', views.country_update),
    # Pilot
    path('ws/pilot', views.pilot_get),
    path('ws/pilots', views.pilots_get),
    path('ws/pilotsearch', views.pilot_search),
    path('ws/pilotcreate', views.pilot_create),
    path('ws/pilotupdate', views.pilot_update),
    # Race
    path('ws/race', views.race_get),
    path('ws/races', views.races_get),
    path('ws/racesearch', views.race_search),
    path('ws/racecreate', views.race_create),
    path('ws/raceupdate', views.race_update),
    # Result
    path('ws/result', views.result_get),


    path('ws/resultcreate', views.result_create),
    path('ws/resultupdate', views.result_update),
    # Team
    path('ws/team', views.team_get),
    path('ws/teams', views.teams_get),
    path('ws/teamsearch', views.team_search),
    path('ws/teamcreate', views.team_create),
    path('ws/teamupdate', views.team_update),
    # Team Leader
    path('ws/teamleader', views.teamleader_get),
    path('ws/teamleaders', views.teamleaders_get),
    path('ws/teamleadersearch', views.teamleader_search),
    path('ws/teamleadercreate', views.teamleader_create),
    path('ws/teamleaderupdate', views.teamleader_update),
    # Profile
    path('ws/profile', views.profile_get),
    path('ws/profileupdate', views.profile_update),
    # Pilot Favourites
    path('ws/pilotfavadd', views.pilot_fav_add),
    path('ws/pilotfavrem', views.pilot_fav_rem),
    # Team Favourites
    path('ws/teamfavadd', views.team_fav_add),
    path('ws/teamfavrem', views.team_fav_rem),
]
