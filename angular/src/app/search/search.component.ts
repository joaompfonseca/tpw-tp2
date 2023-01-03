import { Component } from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {PilotService} from "../../services/pilot/pilot.service";
import {TeamService} from "../../services/team/team.service";
import {RaceService} from "../../services/race/race.service";
import {CircuitService} from "../../services/circuit/circuit.service";
import {CarService} from "../../services/car/car.service";
import {TeamLeaderService} from "../../services/teamleader/team-leader.service";
import {CountryService} from "../../services/country/country.service";

@Component({
  selector: 'app-search',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent {
  header: string;
  type: string;
  pilot: string;
  team: string;
  race: string;
  circuit: string;
  car_model: string;
  car_pilot: string;
  country: string;
  teamleader: string;
  results: { url: string, str: string }[][];

  constructor(private route: ActivatedRoute, private pilotService: PilotService, private teamService: TeamService, private raceService: RaceService, private circuitService: CircuitService, private carService: CarService, private countryService: CountryService, private teamleaderService: TeamLeaderService) {
    this.header = '';
    this.type = '';
    this.pilot = '';
    this.team = '';
    this.race = '';
    this.circuit = '';
    this.car_model = '';
    this.car_pilot = '';
    this.country = '';
    this.teamleader = '';
    this.results = [];
  }

  ngOnInit() {
    this.type = this.route.snapshot.data['type']
    switch (this.type) {
      case 'pilot':
        this.header = 'Search Pilot';
        break;
      case 'team':
        this.header = 'Search Team';
        break;
      case 'race':
        this.header = 'Search Race';
        break;
      case 'circuit':
        this.header = 'Search Circuit';
        break;
      case 'car':
        this.header = 'Search Car';
        break;
      case 'country':
        this.header = 'Search Country';
        break;
      case 'teamleader':
        this.header = 'Search Team Leader';
        break;

    }

  }


  search_pilot() {
    this.pilotService.searchPilot(this.pilot).subscribe(data => {
      this.results = [];
      for (let i = 0; i < data.length; i++) {
        this.results.push([{url: '/pilots/' + data[i].id, str: data[i].name}]);
      }
    }
    );
  }

  search_team() {
    this.teamService.searchTeam(this.team).subscribe(data => {
        this.results = [];
        for (let i = 0; i < data.length; i++) {
          this.results.push([{url: '/teams/' + data[i].id, str: data[i].name}]);
        }
      }
    );
  }

  search_race() {
    this.raceService.searchRace(this.race).subscribe(data => {
        this.results = [];
        for (let i = 0; i < data.length; i++) {
          this.results.push([{url: '/races/' + data[i].id, str: data[i].name}]);
        }
      }
    );
  }

  search_circuit() {
    this.circuitService.searchCircuit(this.circuit).subscribe(data => {
        this.results = [];
        for (let i = 0; i < data.length; i++) {
          this.results.push([{url: '/circuits/' + data[i].id, str: data[i].name}]);
        }
      }
    );
  }

  search_car() {
    this.carService.searchCar(this.car_model, this.car_pilot).subscribe(data => {
        this.results = [];
        for (let i = 0; i < data.length; i++) {
          this.results.push([{url: '/cars/' + data[i].id, str: data[i].model}]);
        }
      }
    );
  }

  search_country() {
    this.countryService.searchCountry(this.country).subscribe(data => {
        this.results = [];
        for (let i = 0; i < data.length; i++) {
          this.results.push([{url: '/countries/' + data[i].id, str: data[i].designation}]);
        }
      }
    );
  }

  search_teamleader() {
    this.teamleaderService.searchTeamLeader(this.teamleader).subscribe(data => {
        this.results = [];
        for (let i = 0; i < data.length; i++) {
          this.results.push([{url: '/teamleaders/' + data[i].id, str: data[i].name}]);
        }
      }
    );
  }








}
