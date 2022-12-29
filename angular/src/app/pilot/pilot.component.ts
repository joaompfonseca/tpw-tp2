import {Component, OnInit} from '@angular/core';
import {User} from "../../interfaces/user";
import {Pilot} from "../../interfaces/pilot";
import {Result} from "../../interfaces/result";

@Component({
  selector: 'app-pilot',
  templateUrl: './pilot.component.html',
  styleUrls: ['./pilot.component.css']
})
export class PilotComponent implements OnInit {

  header: string;
  user: User;
  pilot: Pilot;
  results: Result[];
  isFavourite: boolean;
  likeImage: string;
  dislikeImage: string;


  constructor() {
    // TODO: fetch the API
    this.header = 'Pilot Details';
    this.user = {
      is_authenticated: true,
      is_superuser: true,
    };
    this.pilot = {
      id: 1,
      name: 'Lewis Hamilton',
      date: new Date('1985-01-07'),
      victories: 84,
      pole_positions: 98,
      podiums: 155,
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
          designation: 'United Kingdom',
          code: 'GB',
        }
      ],
      image: ''
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
            name: 'Albert Park Grand Prix Circuit',
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
        points: 25,
      }
    ];
    this.isFavourite = true;
    this.likeImage = '';
    this.dislikeImage = '';
  }

  ngOnInit() {
  }

  getPilot() {
  }

  addToFavourites() {
  }

  removeFromFavourites() {
  }
}
