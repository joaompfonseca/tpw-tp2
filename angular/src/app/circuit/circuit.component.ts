import {Component, OnInit} from '@angular/core';
import {User} from "../../interfaces/user";
import {Circuit} from "../../interfaces/circuit";
import {Race} from "../../interfaces/race";
import {ActivatedRoute} from "@angular/router";
import {CircuitService} from "../../services/circuit/circuit.service";

@Component({
  selector: 'app-circuit',
  templateUrl: './circuit.component.html',
  styleUrls: ['./circuit.component.css']
})
export class CircuitComponent implements OnInit {

  header: string;
  circuitId: number;
  user: User;
  circuit: Circuit;
  races: Race[];

  constructor(private route: ActivatedRoute, private circuitService: CircuitService) {
    this.header = '';
    this.circuitId = 0;
    this.user = {
      is_authenticated: false,
      is_superuser: false,
    };
    this.circuit = {
      id: 0,
      name: '',
      last_winner: {
        id: 0,
        name: '',
        team: {
          id: 0,
          name: '',
        }
      },
      country: {
        id: 0,
        designation: ''
      }
    };
    this.races = [
      {
        id: 0,
        name: '',
        circuit: {
          id: 0,
          name: '',
          last_winner: {
            id: 0,
            name: '',
            team: {
              id: 0,
              name: '',
            }
          },
          country: {
            id: 0,
            designation: '',
          }
        }
      }
    ]
  }

  ngOnInit() {
    this.route.paramMap.subscribe(paramMap => {
      let id = paramMap.get('id');
      if (id !== null) {
        this.circuitId = +id;
      }
      this.getCircuit();
    })
  }

  getCircuit() {
    this.circuitService.getCircuit(this.circuitId).subscribe(data => {
      console.log(data);
      this.header = data.header.header;
      this.user = data.auth;
      this.circuit = data.circuit;
      this.circuit.country = data.country;
      this.circuit.last_winner = data.last_winner;
      this.races = data.races;

    })
  }
}
