import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { CarComponent } from './car/car.component';
import { CircuitComponent } from './circuit/circuit.component';
import { CountryComponent } from './country/country.component';
import { EditComponent } from './edit/edit.component';
import { HomeComponent } from './home/home.component';
import { ListComponent } from './list/list.component';
import { LoginComponent } from './login/login.component';
import { LoginpartialComponent } from './loginpartial/loginpartial.component';
import { NewComponent } from './new/new.component';
import { PilotComponent } from './pilot/pilot.component';
import { ProfileComponent } from './profile/profile.component';
import { RaceComponent } from './race/race.component';
import { SearchComponent } from './search/search.component';
import { SignupComponent } from './signup/signup.component';
import { TeamComponent } from './team/team.component';
import { TeamleaderComponent } from './teamleader/teamleader.component';
import { AppRoutingModule } from './app-routing.module';

import {HttpClientModule, HttpClientXsrfModule} from '@angular/common/http';
import {FormsModule} from "@angular/forms";

@NgModule({
  declarations: [
    AppComponent,
    CarComponent,
    CircuitComponent,
    CountryComponent,
    EditComponent,
    HomeComponent,
    ListComponent,
    LoginComponent,
    LoginpartialComponent,
    NewComponent,
    PilotComponent,
    ProfileComponent,
    RaceComponent,
    SearchComponent,
    SignupComponent,
    TeamComponent,
    TeamleaderComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    HttpClientXsrfModule,
    FormsModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
