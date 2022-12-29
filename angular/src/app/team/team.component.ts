import {Component} from '@angular/core';
import {User} from "../../interfaces/user";
import {Team} from "../../interfaces/team";
import {Pilot} from "../../interfaces/pilot";

@Component({
  selector: 'app-team',
  templateUrl: './team.component.html',
  styleUrls: ['./team.component.css']
})
export class TeamComponent {

  header: string;
  user: User;
  team: Team;
  pilots: Pilot[];
  isFavourite: boolean;
  likeImage: string;
  dislikeImage: string;

  constructor() {
    // TODO: fetch from API
    this.header = 'Team Details';
    this.user = {
      is_authenticated: true,
      is_superuser: true
    }
    this.team = {
      id: 1,
      name: 'Mercedes',
      date: new Date('2010-01-01'),
      championships: 5,
      points: 1000,
      image: '',
      teamleader: {
        id: 1,
        name: 'Toto Wolff',
        image: ''
      }
    };
    this.pilots = [
      {
        id: 1,
        name: 'Lewis Hamilton',
        date: new Date('1985-01-07'),
        victories: 62,
        pole_positions: 96,
        podiums: 126,
        championships: 5,
        contract: 2022,
        entry_year: 2007,
        team: {
          id: 1,
          name: 'Mercedes',
          date: new Date('2010-01-01'),
          championships: 5,
          points: 1000,
          image: '',
          teamleader: {
            id: 1,
            name: 'Toto Wolff',
            image: ''
          }
        },
        country: [
          {
            id: 1,
            designation: 'United Kingdom',
            code: 'GB'
          }
        ],
        image: ''
      }
    ];
    this.isFavourite = true;
    this.likeImage = '';
    this.dislikeImage = '';
  }


  ngOnInit() {
  }

  getTeam() {
  }

  addToFavourites() {
  }

  removeFromFavourites() {
  }
}
