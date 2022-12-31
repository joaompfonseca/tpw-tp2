import {Component, OnInit} from '@angular/core';
import {User} from "../../interfaces/user";
import {Country} from "../../interfaces/country";
import {Circuit} from "../../interfaces/circuit";
import {Pilot} from "../../interfaces/pilot";
import {ActivatedRoute} from "@angular/router";
import {CountryService} from "../../services/country/country.service";

@Component({
  selector: 'app-country',
  templateUrl: './country.component.html',
  styleUrls: ['./country.component.css']
})
export class CountryComponent implements OnInit {

  header: string;
  countryId: number;
  user: User;
  country: Country;
  circuits: Circuit[];
  pilots: Pilot[];

  constructor(private route: ActivatedRoute, private countryService: CountryService) {
    this.header = '';
    this.countryId = 0;
    this.user = {
      is_authenticated: false,
      is_superuser: false,
    };
    this.country = {
      id: 0,
      designation: '',
    };
    this.circuits = [
      {
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
    ];
    this.pilots = [
      {
        id: 0,
        name: '',
        team: {
          id: 0,
          name: '',
        }
      }
    ];
  }

  ngOnInit() {
    this.route.paramMap.subscribe(paramMap => {
      let id = paramMap.get('id');
      if (id !== null) {
        this.countryId = +id;
      }
      this.getCountry();
    })
  }

  getCountry() {
this.countryService.getCountry(this.countryId).subscribe(data => {
      this.header = data.header.header;
      this.user = data.auth;
      this.country = data.country;
      this.circuits = data.circuits;
      this.pilots = data.pilots;
    })
  }
}
