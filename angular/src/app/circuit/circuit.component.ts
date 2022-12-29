import {Component, OnInit} from '@angular/core';
import {User} from "../../interfaces/user";
import {Circuit} from "../../interfaces/circuit";
import {Race} from "../../interfaces/race";

@Component({
  selector: 'app-circuit',
  templateUrl: './circuit.component.html',
  styleUrls: ['./circuit.component.css']
})
export class CircuitComponent implements OnInit {

  header: string;
  user: User;
  circuit: Circuit;
  races: Race[];

  constructor() {
    // TODO: fetch from API
    this.header = 'Circuit Details';
    this.user = {
      is_authenticated: true,
      is_superuser: true,
    };
    this.circuit = {
      id: 1,
      name: 'Albert Park',
      length: 5.303,
      location: 'Melbourne',
      last_winner: {
        id: 5,
        name: 'Daniel Ricciardo',
        team: {
          id: 5,
          name: 'Renault',
        }
      },
      country: {
        id: 1,
        designation: 'Australia'
      }
    };
    this.races = [
      {
        id: 1,
        name: 'Australian Grand Prix',
        circuit: {
          id: 1,
          name: 'Albert Park',
          last_winner: {
            id: 5,
            name: 'Daniel Ricciardo',
            team: {
              id: 5,
              name: 'Renault',
            }
          },
          country: {
            id: 1,
            designation: 'Australia',
            code: 'AU',
          }
        }
      }
    ]
  }

  ngOnInit() {
  }

  getCircuit() {
  }
}
