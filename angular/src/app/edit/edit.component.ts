import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {PilotService} from "../../services/pilot/pilot.service";
import {TeamService} from "../../services/team/team.service";
import {RaceService} from "../../services/race/race.service";
import {CircuitService} from "../../services/circuit/circuit.service";
import {CarService} from "../../services/car/car.service";
import {CountryService} from "../../services/country/country.service";
import {TeamLeaderService} from "../../services/teamleader/team-leader.service";
import {Pilot} from "../../interfaces/pilot";
import {Team} from "../../interfaces/team";
import {Race} from "../../interfaces/race";
import {Circuit} from "../../interfaces/circuit";
import {Country} from "../../interfaces/country";
import {Car} from "../../interfaces/car";
import {TeamLeader} from "../../interfaces/teamleader";

@Component({
  selector: 'app-edit',
  templateUrl: './edit.component.html',
  styleUrls: ['./edit.component.css']
})
export class EditComponent implements OnInit {

  header: string;

  type: string;

  data: any;

  pilot: Pilot | undefined;

  team: Team | undefined;

  race: Race | undefined;

  circuit: Circuit | undefined;

  car: Car | undefined;

  country: Country | undefined;

  teamleader: TeamLeader | undefined;

  selectedTeamP: Team | undefined;

  selectedCountryP: Country | undefined;

  selectedCircuitR: Circuit | undefined;

  selectedCountryC: Country | undefined;

  selectedPilotC: Pilot | undefined;

  selectedPilotCar: Pilot | undefined;

  selectedTeamTL: Team | undefined;

  Teams: any;

  Countries: any;

  Circuits: any;

  Pilots: any;

  constructor(private route: ActivatedRoute,
              private pilotService: PilotService,
              private teamService: TeamService,
              private raceService: RaceService,
              private circuitService: CircuitService,
              private carService: CarService,
              private countryService: CountryService,
              private teamleaderService: TeamLeaderService) {
    this.header = '';
    this.type = '';
  }

  ngOnInit() {
    this.type = this.route.snapshot.data['type'];
    switch (this.type) {
      case 'pilot':
        this.header = 'Edit Pilot';
        this.getPilot();
        break;
      case 'team':
        this.header = 'Edit Team';
        this.getTeam();
        break;
      case 'race':
        this.header = 'Edit Race';
        this.getRace();
        break;
      case 'circuit':
        this.header = 'Edit Circuit';
        this.getCircuit();
        break;
      case 'car':
        this.header = 'Edit Car';
        this.getCar();
        break;
      case 'country':
        this.header = 'Edit Country';
        this.getCountry();
        break;
      case 'teamleader':
        this.header = 'Edit Team Leader';
        this.getTeamLeader();
        break;
    }
  }

  getTeamLeader() {
  let id = this.route.snapshot.params['id'];
    this.teamleaderService.getTeamleader(id).subscribe(data => {
      this.teamleader = data.teamleader;
      this.teamleader!.team = data.team;
      this.getAllTeamsL();
    });
  }

  getAllTeamsL(){
    this.teamService.getTeams().subscribe(data => {
      this.Teams = [];
      for (let t of data) {
        if (t.id != this.teamleader!.team!.id) {
          this.Teams.push(t);
        }
      }
    });
  }

  updateTeamLeader() {
    this.teamleader!.team = this.selectedTeamTL;
    this.teamleaderService.updateTeamLeader(this.teamleader!.id,this.teamleader!).subscribe(data => {
      console.log(data);
    });
  }

  getCountry() {
    let id = this.route.snapshot.params['id'];
    this.countryService.getCountry(id).subscribe(data => {
      this.country = data.country;
      console.log(this.country);
    });
  }

  updateCountry() {
    this.countryService.updateCountry(this.country!.id,this.country!).subscribe(data => {
      console.log(data);
    });
  }


  getCar(){
    let id = this.route.snapshot.params['id'];
    this.carService.getCar(id).subscribe(data => {
      this.car = data.car;
      this.car!.pilot = data.pilot;
      this.car!.pilot.team = data.team;
      this.getAllPilotsCar();
    })
  }

  getAllPilotsCar(){
    this.pilotService.getPilots().subscribe(data => {
      this.Pilots = [];
      for (let t of data) {
        if (t.id != this.car!.pilot.id) {
          this.Pilots.push(t);
        }
      }
    });
  }

  updateCar() {
    if (this.selectedPilotCar) {
      this.car!.pilot = this.selectedPilotCar;
    }
    this.carService.updateCar(this.car!.id,this.car!).subscribe(data => {
      console.log(data);
    });
  }

  getPilot() {
    let id = this.route.snapshot.params['id'];
    this.pilotService.getPilot(id).subscribe(data => {
      this.pilot = data.pilot;
      this.pilot!.country = data.country;
      this.pilot!.team = data.team;
      this.pilot!.points = data.points.points;
      this.getAllTeams();
      this.getAllCountries();
    });
  }

  getAllTeams() {
    this.teamService.getTeams().subscribe(data => {
      this.Teams = [];
      for (let t of data) {
        if (t.id != this.pilot!.team.id) {
          this.Teams.push(t);
        }
      }
    });
  }

  getAllCountries() {
    this.countryService.getCountries().subscribe(data => {
      let temp = data;
      let ids = [];
      for (let t of this.pilot!.country!){
        ids.push(t.id);
      }
      this.Countries = [];
      for (let t of temp) {
        if (!ids.includes(t.id)) {
          console.log(t);
          this.Countries.push(t);
        }
      }
      console.log(this.Countries);
    });
  }

  updatePilot() {
    this.pilotService.updatePilot(this.pilot!.id,this.pilot!).subscribe(data => {
      console.log(data);
    });
  }

  print() {
    console.log(this.selectedTeamP)
  }

  getTeam() {
    let id = this.route.snapshot.params['id'];
    this.teamService.getTeam(id).subscribe(data => {
      this.team = data.team;
      this.team!.teamleader = data.teamleader;
      this.team!.points = data.points.points;
    });
  }

  updateTeam() {
    this.teamService.updateTeam(this.team!.id,this.team!).subscribe(data => {
      console.log(data);
    });
  }

  getRace() {
    let id = this.route.snapshot.params['id'];
    this.raceService.getRace(id).subscribe(data => {
      this.race = data.race;
      this.race!.circuit = data.circuit;
      this.race!.fast_lap = data.race.fast_lap.substring(3);
      this.getAllCircuits();
    });
  }

  getAllCircuits() {
    this.circuitService.getCircuits().subscribe(data => {
      this.Circuits = [];
      for (let t of data) {
        if (t.id != this.race!.circuit.id) {
          this.Circuits.push(t);
        }
      }
    });
  }

  updateRace() {
    this.raceService.updateRace(this.race!.id,this.race!).subscribe(data => {
      console.log(data);
    })
  }

  getCircuit() {
    let id = this.route.snapshot.params['id'];
    this.circuitService.getCircuit(id).subscribe(data => {
      this.circuit = data.circuit;
      this.circuit!.country = data.country;
      this.circuit!.last_winner = data.last_winner;
      this.getAllPilots();
      this.getAllCountries1();
    });
  }

  getAllPilots() {
    this.pilotService.getPilots().subscribe(data => {
      this.Pilots = [];
      for (let t of data) {
        if (t.id != this.circuit!.last_winner.id) {
          this.Pilots.push(t);
        }
      }
    });
  }

  getAllCountries1() {
    this.countryService.getCountries().subscribe(data => {
      this.Countries = [];
      for (let t of data) {
        if (t.id != this.circuit!.country.id) {
          this.Countries.push(t);
        }
      }
    });
  }

  updateCircuit() {
    if (this.selectedPilotC) {
      this.circuit!.last_winner = this.selectedPilotC;
    }
    if (this.selectedCountryC) {
      this.circuit!.country = this.selectedCountryC;
    }
    this.circuitService.updateCircuit(this.circuit!.id,this.circuit!).subscribe(data => {
      console.log(data);
    })
  }
}


