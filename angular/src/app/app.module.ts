import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { CarComponent } from './car/car.component';
import { CircuitComponent } from './circuit/circuit.component';
import { CountryComponent } from './country/country.component';
import { EditComponent } from './edit/edit.component';
import { HomeComponent } from './home/home.component';
import { LayoutComponent } from './layout/layout.component';
import { ListComponent } from './list/list.component';
import { LoginComponent } from './login/login.component';
import { LoginpartialComponent } from './loginpartial/loginpartial.component';
import { NewComponent } from './new/new.component';
import { PilotComponent } from './pilot/pilot.component';
import { ProfileComponent } from './profile/profile.component';
import { RaceComponent } from './race/race.component';
import { ResultComponent } from './result/result.component';
import { SearchComponent } from './search/search.component';
import { SignupComponent } from './signup/signup.component';
import { TeamComponent } from './team/team.component';
import { TeamleaderComponent } from './teamleader/teamleader.component';

@NgModule({
  declarations: [
    AppComponent,
    CarComponent,
    CircuitComponent,
    CountryComponent,
    EditComponent,
    HomeComponent,
    LayoutComponent,
    ListComponent,
    LoginComponent,
    LoginpartialComponent,
    NewComponent,
    PilotComponent,
    ProfileComponent,
    RaceComponent,
    ResultComponent,
    SearchComponent,
    SignupComponent,
    TeamComponent,
    TeamleaderComponent
  ],
  imports: [
    BrowserModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
