import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {HomeComponent} from "./home/home.component";
import {LoginComponent} from "./login/login.component";
import {SignupComponent} from "./signup/signup.component";
import {CarComponent} from "./car/car.component";
import {SearchComponent} from "./search/search.component";
import {ListComponent} from "./list/list.component";
import {NewComponent} from "./new/new.component";
import {EditComponent} from "./edit/edit.component";
import {CircuitComponent} from "./circuit/circuit.component";
import {CountryComponent} from "./country/country.component";
import {PilotComponent} from "./pilot/pilot.component";
import {RaceComponent} from "./race/race.component";
import {TeamComponent} from "./team/team.component";
import {TeamleaderComponent} from "./teamleader/teamleader.component";
import {ProfileComponent} from "./profile/profile.component";

const routes = [
  // Home
  {path: '', component: HomeComponent},
  // Auth
  {path: 'login', component: LoginComponent},
  {path: 'logout', component: HomeComponent},
  {path: 'signup', component: SignupComponent},
  // Car
  {path: 'cars', component: ListComponent, data: {type: 'car'}},
  {path: 'cars/new', component: NewComponent, data: {type: 'car'}},
  {path: 'cars/search', component: SearchComponent, data: {type: 'car'}},
  {path: 'cars/:id', component: CarComponent},
  {path: 'cars/:id/edit', component: EditComponent, data: {type: 'car'}},
  // Circuit
  {path: 'circuits', component: ListComponent, data: {type: 'circuit'}},
  {path: 'circuits/new', component: NewComponent, data: {type: 'circuit'}},
  {path: 'circuits/search', component: SearchComponent, data: {type: 'circuit'}},
  {path: 'circuits/:id', component: CircuitComponent},
  {path: 'circuits/:id/edit', component: EditComponent, data: {type: 'circuit'}},
  // Country
  {path: 'countries', component: ListComponent, data: {type: 'country'}},
  {path: 'countries/new', component: NewComponent, data: {type: 'country'}},
  {path: 'countries/search', component: SearchComponent, data: {type: 'country'}},
  {path: 'countries/:id', component: CountryComponent},
  {path: 'countries/:id/edit', component: EditComponent, data: {type: 'country'}},
  // Pilot
  {path: 'pilots', component: ListComponent, data: {type: 'pilot'}},
  {path: 'pilots/new', component: NewComponent, data: {type: 'pilot'}},
  {path: 'pilots/search', component: SearchComponent, data: {type: 'pilot'}},
  {path: 'pilots/:id', component: PilotComponent},
  {path: 'pilots/:id/edit', component: EditComponent, data: {type: 'pilot'}},
  // Race
  {path: 'races', component: ListComponent, data: {type: 'race'}},
  {path: 'races/new', component: NewComponent, data: {type: 'race'}},
  {path: 'races/search', component: SearchComponent, data: {type: 'race'}},
  {path: 'races/:id', component: RaceComponent},
  {path: 'races/:id/edit', component: EditComponent, data: {type: 'race'}},
  // Result
  {path: 'results/new', component: NewComponent, data: {type: 'result'}},
  {path: 'results/:id/edit', component: EditComponent, data: {type: 'result'}},
  // Team
  {path: 'teams', component: ListComponent, data: {type: 'team'}},
  {path: 'teams/new', component: NewComponent, data: {type: 'team'}},
  {path: 'teams/search', component: SearchComponent, data: {type: 'team'}},
  {path: 'teams/:id', component: TeamComponent},
  {path: 'teams/:id/edit', component: EditComponent, data: {type: 'team'}},
  // Team Leader
  {path: 'teamleaders', component: ListComponent, data: {type: 'teamleader'}},
  {path: 'teamleaders/new', component: NewComponent, data: {type: 'teamleader'}},
  {path: 'teamleaders/search', component: SearchComponent, data: {type: 'teamleader'}},
  {path: 'teamleaders/:id', component: TeamleaderComponent},
  {path: 'teamleaders/:id/edit', component: EditComponent, data: {type: 'teamleader'}},
  // Profile
  {path: 'profile', component: ProfileComponent},
  {path: 'profile/edit', component: EditComponent, data: {type: 'profile'}},
]

@NgModule({
  declarations: [],
  exports: [
    RouterModule
  ],
  imports: [
    RouterModule.forRoot(routes)
  ]
})
export class AppRoutingModule {
}
