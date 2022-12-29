import {Component, OnInit} from '@angular/core';
import {User} from "../../interfaces/user";
import {Result} from "../../interfaces/result";

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements OnInit {

  header: string;
  user: User;
  result: Result;

  constructor() {
    // TODO: fetch from API
    this.header = 'Result Details';
    this.user = {
      is_authenticated: true,
      is_superuser: true
    }
    this.result = {
      id: 1,
      position: 1,
      pilot: {
        id: 1,
        name: 'Lewis Hamilton',
        date: new Date('1985-01-07'),
        victories: 62,
        pole_positions: 96,
        podiums: 126,
        championships: 5,
        points: 1000,
        contract: 2022,
        entry_year: 2007,
        team: {
          id: 1,
          name: 'Mercedes',
        },
        country: [
          {
            id: 1,
            designation: 'Great Britain',
            code: 'GB'
          }
        ],
        image: ''
      },
      race: {
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
            code: 'AU'
          }
        }
      },
      points: 25
    }

  }

  ngOnInit() {
  }

  getResult() {
  }
}
