import {Component, OnInit} from '@angular/core';
import {Race} from "../../interfaces/race";
import {User} from "../../interfaces/user";
import {Result} from "../../interfaces/result";

@Component({
  selector: 'app-race',
  templateUrl: './race.component.html',
  styleUrls: ['./race.component.css']
})
export class RaceComponent implements OnInit {

  header: string
  user: User
  race: Race
  results: Result[]

  constructor() {
    // TODO: fetch from API
    this.header = 'Race Details';
    this.user = {
      is_authenticated: true,
      is_superuser: true
    };
    this.race = {
      id: 1,
      name: 'Australian Grand Prix',
      date: new Date('2021-03-21'),
      season: 2021,
      fast_lap: '1:29.552',
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
    };
    this.results = [
      {
        id: 1,
        position: 1,
        pilot: {
          id: 1,
          name: 'Lewis Hamilton',
          team: {
            id: 1,
            name: 'Mercedes',
          }
        },
        race: {
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
        },
        points: 25
      }
    ]
  }

  ngOnInit() {
  }

  getRace() {
  }
}
