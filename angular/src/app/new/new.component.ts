import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {PilotService} from "../../services/pilot/pilot.service";
import {TeamService} from "../../services/team/team.service";
import {RaceService} from "../../services/race/race.service";
import {CircuitService} from "../../services/circuit/circuit.service";
import {CarService} from "../../services/car/car.service";
import {CountryService} from "../../services/country/country.service";
import {TeamLeaderService} from "../../services/teamleader/team-leader.service";
import {Pilot} from "../../interfaces/pilot";
import {Team} from "../../interfaces/team";
import {Country} from "../../interfaces/country";
import {Circuit} from "../../interfaces/circuit";
import {Race} from "../../interfaces/race";
import {Car} from "../../interfaces/car";
import {TeamLeader} from "../../interfaces/teamleader";


@Component({
  selector: 'app-new',
  templateUrl: './new.component.html',
  styleUrls: ['./new.component.css']
})
export class NewComponent implements OnInit {

  header: string;

  type: string;

  pilot: Pilot;

  team: Team;

  race: Race;

  car: Car;

  circuit: Circuit;

  country: Country;

  teamleader: TeamLeader;

  Teams: any;

  Countries: any;

  Circuits: any;

  Pilots: any;

  selectedTeamP: Team | undefined;

  selectedCountryP: Country[] | undefined;

  selectedCircuitR: Circuit | undefined;

  selectedPilotC: Pilot | undefined;

  selectedCountryC: Country | undefined;

  selectedPilotCar: Pilot | undefined;

  selectedTeamTL: Team | undefined;

  constructor(private router: Router,
              private route: ActivatedRoute,
              private pilotService: PilotService,
              private teamService: TeamService,
              private raceService: RaceService,
              private circuitService: CircuitService,
              private carService: CarService,
              private countryService: CountryService,
              private teamleaderService: TeamLeaderService) {
    this.header = '';
    this.type = '';
    this.pilot = {
      id: 0,
      name: '',
      team: {
        id: 0,
        name: '',
        is_fav: false,
      },
      is_fav: false,
    }
    this.team = {
      id: 0,
      name: '',
      date: undefined,
      championships: undefined,
      is_fav: false,
    }
    this.race = {
      id: 0,
      name: '',
      date: undefined,
      season: undefined,
      fast_lap: undefined,
      circuit: {
        id: 0,
        name: '',
        length: undefined,
        location: undefined,
        last_winner: {
          id: 0,
          name: '',
          team: {
            id: 0,
            name: '',
            is_fav: false
          },
          is_fav: false
        },
        country: {
          id: 0,
          designation: '',
          code: '',
        }
      }
    }
    this.circuit = {
      id: 0,
      name: '',
      length: undefined,
      location: undefined,
      last_winner: {
        id: 0,
        name: '',
        team: {
          id: 0,
          name: '',
          is_fav: false
        },
        is_fav: false
      },
      country: {
        id: 0,
        designation: '',
        code: '',
      }
    }
    this.car = {
      id: 0,
      model: '',
      engine: '',
      weight: 0,
      pilot: {
        id: 0,
        name: '',
        team: {
          id: 0,
          name: '',
          is_fav: false
        },
        is_fav: false
      }
    }
    this.country = {
      id: 0,
      designation: '',
      code: '',
    }
    this.teamleader = {
      id: 0,
      name: '',
      team: {
        id: 0,
        name: '',
        date: undefined,
        championships: undefined,
        is_fav: false
      }
    }
  }

  ngOnInit() {
    this.type = this.route.snapshot.data['type'];
    switch (this.type) {
      case 'pilot':
        this.header = 'Add new pilot';
        this.getAllTeams();
        break;
      case 'team':
        this.header = 'Add new team';
        break;
      case 'race':
        this.header = 'Add new Race';
        this.getAllCircuits();
        break;
      case 'circuit':
        this.header = 'Add new Circuit';
        this.getAllPilots();
        break;
      case 'car':
        this.header = 'Add new Car';
        this.getAllPilots();
        break;
      case 'country':
        this.header = 'Add new Country';
        break;
      case 'teamleader':
        this.header = 'Add new Team Leader';
        this.getAllTeams();
        break;
    }
  }

  createTeamLeader() {
    this.teamleaderService.createTeamLeader({
      name: this.teamleader!.name,
      team: this.selectedTeamTL?.id
    })
      .subscribe(() => this.router.navigate(['/teamleaders']).then(() => window.location.reload()));
  }

  createCountry() {
    this.countryService.createCountry({
      designation: this.country!.designation,
      code: this.country!.code,
    })
      .subscribe(() => this.router.navigate(['/countries']).then(() => window.location.reload()));
  }

  createCar() {
    this.carService.createCar({
      model: this.car!.model,
      engine: this.car!.engine,
      weight: this.car!.weight,
      pilot: this.selectedPilotCar?.id
    })
      .subscribe(() => this.router.navigate(['/cars']).then(() => window.location.reload()));
  }

  getAllPilots() {
    this.pilotService.getPilots().subscribe(data => {
      this.Pilots = data;
      console.log(this.Teams);
    });
    this.getAllCountries();
  }

  createCircuit() {
    this.circuitService.createCircuit({
      name: this.circuit!.name,
      length: this.circuit!.length,
      location: this.circuit!.location,
      last_winner: this.selectedPilotC?.id,
      country: this.selectedCountryC?.id
    })
      .subscribe(() => this.router.navigate(['/circuits']).then(() => window.location.reload()));
  }

  getAllCircuits() {
    this.circuitService.getCircuits()
      .subscribe(() => this.router.navigate(['/circuits']).then(() => window.location.reload()));
  }

  createRace() {
    this.raceService.createRace({
      name: this.race!.name,
      date: this.race!.date,
      season: this.race!.season,
      fast_lap: this.race!.fast_lap,
      circuit: this.selectedCircuitR?.id
    })
      .subscribe(() => this.router.navigate(['/races']).then(() => window.location.reload()));
  }

  createTeam() {
    this.teamService.createTeam(this.team)
      .subscribe(() => this.router.navigate(['/teams']).then(() => window.location.reload()));
  }

  getAllTeams() {
    this.teamService.getTeams().subscribe(data => {
      this.Teams = data;
      console.log(this.Teams);
      this.getAllCountries();
    });
  }

  getAllCountries() {
    this.countryService.getCountries().subscribe(data => {
      this.Countries = data;
      console.log(this.Countries);
    });
  }

  newPilot() {
    let id_c = [];
    for (let c of this.selectedCountryP!) {
      id_c.push(c.id);
    }
    this.pilotService.createPilot({
      name: this.pilot!.name,
      date: this.pilot!.date,
      victories: this.pilot!.victories,
      pole_positions: this.pilot!.pole_positions,
      podiums: this.pilot!.podiums,
      championships: this.pilot!.championships,
      contract: this.pilot!.contract,
      entry_year: this.pilot!.entry_year,
      team: this.selectedTeamP?.id,
      country: id_c
    })
      .subscribe(() => this.router.navigate(['/pilots']).then(() => window.location.reload()));
  }
}
