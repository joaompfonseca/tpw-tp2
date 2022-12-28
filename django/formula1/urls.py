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
from django.contrib.auth import views as auth_views
from django.urls import path

from app import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    # Home
    path('', views.home, name='home'),
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', views.signup, name='signup'),
    # Car
    path('ws/cars', views.get_cars, name='get_cars'),
    path('ws/car', views.get_car, name='get_car'),
    path('ws/carcre', views.car_create, name='car_create'),
    path('ws/carsearch', views.car_search, name='car_search'),
    path('ws/carupdate', views.update_car, name='car_update'),
    # Circuit
    path('ws/circuits', views.get_circuits, name='get_circuits'),
    path('ws/circuit', views.get_circuit, name='get_circuit'),
    path('ws/circuitcre', views.new_circuit, name='circuit_create'),
    path('ws/circuitsearch', views.search_circuits, name='circuit_search'),
    path('ws/circuitupdate', views.update_circuit, name='circuit_update'),
    # Country
    path('ws/countries', views.get_countries, name='countries_get'),
    path('ws/countrysearch', views.search_countries, name='countries_search'),
    path('ws/country', views.get_country, name='country_get'),
    path('ws/countriycre', views.new_country, name='countries_new'),
    path('ws/countryupdate', views.update_country, name='countries_edit'),
    # Pilot
    path('ws/pilots', views.get_pilots, name='pilots_list'),
    path('ws/pilotsearch', views.search_pilots, name='pilots_search'),
    path('ws/pilot', views.get_pilot, name='pilots_get'),
    path('ws/pilotcre', views.add_pilot, name='pilots_new'),
    path('ws/pilotupdate', views.update_pilot, name='pilots_edit'),
    # Race
    path('ws/races', views.get_races, name='races_list'),
    path('ws/racesearch', views.search_races, name='races_search'),
    path('ws/race', views.get_race, name='races_get'),
    path('ws/racecre', views.new_race, name='races_new'),
    path('ws/raceupdate', views.update_race, name='races_edit'),
    # Result
    #path('results/', views.results_list, name='results_list'),
    #path('results/search/', views.results_search, name='results_search'),
    path('ws/result', views.get_result, name='results_get'),
    path('ws/resultcre', views.new_result, name='results_new'),
    path('ws/resultupdate', views.update_result, name='results_edit'),
    # Team
    path('ws/teams', views.get_teams, name='teams_list'),
    path('ws/teamsearch', views.search_team, name='teams_search'),
    path('ws/team', views.get_team, name='teams_get'),
    path('ws/teamscre', views.new_team, name='teams_new'),
    path('ws/teamsupdate', views.update_team, name='teams_edit'),
    # Team Leader
    path('ws/teamleaders', views.get_teamleaders, name='teamleaders_list'),
    path('ws/teamleadersearch', views.search_teamleader, name='teamleaders_search'),
    path('ws/teamleader', views.get_teamleader, name='teamleaders_get'),
    path('ws/teamleadercre', views.new_teamleader, name='teamleaders_new'),
    path('ws/teamleaderupdate', views.update_teamleader, name='teamleaders_edit'),

    # Template
    path('template_index/', views.template_index, name='template_index'),

    # Profile
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),

    # Pilot Favourites
    # Add to Favourite
    path('pilot/favourite/<int:pilot_id>', views.pilot_add_to_favourite, name='pilot_add_to_favourite'),
    # Remove from Favourite
    path('pilot/remove/<int:pilot_id>', views.pilot_remove_from_favourite, name='pilot_remove_from_favourite'),


    # Team Favourites
    # Add to Favourite
    path('team/favourite/<int:team_id>', views.team_add_to_favourite, name='team_add_to_favourite'),
    # Remove from Favourite
    path('team/remove/<int:team_id>', views.team_remove_from_favourite, name='team_remove_from_favourite'),

]
