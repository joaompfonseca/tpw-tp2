import {Component, OnInit} from '@angular/core';
import {User} from "../../interfaces/user";
import {Country} from "../../interfaces/country";
import {Circuit} from "../../interfaces/circuit";
import {Pilot} from "../../interfaces/pilot";

@Component({
  selector: 'app-country',
  templateUrl: './country.component.html',
  styleUrls: ['./country.component.css']
})
export class CountryComponent implements OnInit {

  header: string;
  user: User;
  country: Country;
  circuits: Circuit[];
  pilots: Pilot[];

  constructor() {
    // TODO: fetch from API
    this.header = 'Country Details';
    this.user = {
      is_authenticated: true,
      is_superuser: true,
    };
    this.country = {
      id: 1,
      designation: 'Australia',
      code: 'AU',
    };
    this.circuits = [
      {
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
    ];
    this.pilots = [
      {
        id: 5,
        name: 'Daniel Ricciardo',
        team: {
          id: 5,
          name: 'Renault',
        }
      }
    ];
  }

  ngOnInit() {
  }

  getCountry() {
  }
}
