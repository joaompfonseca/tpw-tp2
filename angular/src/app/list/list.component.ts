import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {PilotService} from "../../services/pilot/pilot.service";
import {TeamService} from "../../services/team/team.service";
import {RaceService} from "../../services/race/race.service";
import {CircuitService} from "../../services/circuit/circuit.service";
import {CarService} from "../../services/car/car.service";
import {CountryService} from "../../services/country/country.service";
import {TeamLeaderService} from "../../services/teamleader/team-leader.service";
import {UserService} from "../../services/user/user.service";
import {User} from "../../interfaces/user";

@Component({
  selector: 'app-list',
  templateUrl: './list.component.html',
  styleUrls: ['./list.component.css']
})
export class ListComponent implements OnInit {

  header: string;
  user: User | undefined;
  actions: { url: string, str: string }[];
  list: { url: string, str: string }[][];
  query?: string;
  type: string;
  pilots: any;

  constructor(private route: ActivatedRoute,
              private pilotService: PilotService,
              private teamService: TeamService,
              private raceService: RaceService,
              private circuitService: CircuitService,
              private carService: CarService,
              private countryService: CountryService,
              private teamleaderService: TeamLeaderService,
              private userService: UserService) {
    this.header = '';
    this.type = '';
    this.actions = [
      {url: '', str: ''},
    ];
    this.list = [];
  }

  ngOnInit() {
    this.type = this.route.snapshot.data['type']

    this.getUser();

    switch (this.type) {
      case 'pilot':
        this.header = 'List of Pilots';
        this.actions = [
          {url: '/pilots/search', str: 'Search Pilot'},
          {url: '/pilots/new', str: 'New Pilot'}
        ];
        this.getPilots();
        break;
      case 'team':
        this.header = 'List of Teams';
        this.actions = [
          {url: '/teams/search', str: 'Search Team'},
          {url: '/teams/new', str: 'New Team'}
        ];
        this.getTeams();
        break;
      case 'race':
        this.header = 'List of Races';
        this.actions = [
          {url: '/races/search', str: 'Search Race'},
          {url: '/races/new', str: 'New Race'}];
        this.getRaces();
        break;
      case 'circuit':
        this.header = 'List of Circuits';
        this.actions = [
          {url: '/circuits/search', str: 'Search Circuit'},
          {url: '/circuits/new', str: 'New Circuit'}
        ];
        this.getCircuits();
        break;
      case 'car':
        this.header = 'List of Cars';
        this.actions = [
          {url: '/cars/search', str: 'Search Car'},
          {url: '/cars/new', str: 'New Car'}
        ];
        this.getCars();
        break;
      case 'country':
        this.header = 'List of Countries';
        this.actions = [
          {url: '/countries/search', str: 'Search Country'},
          {url: '/countries/new', str: 'New Country'}
        ];
        this.getCountries();
        break;
      case 'teamleader':
        this.header = 'List of Team Leaders';
        this.actions = [
          {url: '/teamleaders/search', str: 'Search Team Leader'},
          {url: '/teamleaders/new', str: 'New Team Leader'}
        ];
        this.getTeamleaders();
        break;

    }
  }

  getPilots() {
    this.pilotService.getPilots().subscribe(pilots => {
      this.list = pilots.map((pilot) => {
        return [{url: '/pilots/' + pilot.id, str: pilot.name}];
      });
    });
  }

  getTeams() {
    this.teamService.getTeams().subscribe(teams => {
        this.list = teams.map((team) => {
          return [{url: '/teams/' + team.id, str: team.name}];
        });
      }
    );
  }

  getRaces() {
    this.raceService.getRaces().subscribe(races => {
        this.list = races.map((race) => {
          return [{url: '/races/' + race.id, str: race.name}];
        });
      }
    );
  }

  getCircuits() {
    this.circuitService.getCircuits().subscribe(circuits => {
        this.list = circuits.map((circuit) => {
          return [{url: '/circuits/' + circuit.id, str: circuit.name}];
        });
      }
    );
  }

  getCars() {
    this.carService.getCars().subscribe(cars => {
        this.list = cars.map((car) => {
          return [{url: '/cars/' + car.id, str: car.model}];
        });
      }
    );
  }

  getCountries() {
    this.countryService.getCountries().subscribe(countries => {
        this.list = countries.map((country) => {
          return [{url: '/countries/' + country.id, str: country.designation}];
        });
      }
    );
  }

  getTeamleaders() {
    this.teamleaderService.getTeamleaders().subscribe(teamleaders => {
      this.list = teamleaders.map((teamleader) => {
        return [{url: '/teamleaders/' + teamleader.id, str: teamleader.name}];
      });
    });
  }

  getUser() {
    this.userService.getUser().subscribe(user => {
      this.user = user;
    });
  }
}
