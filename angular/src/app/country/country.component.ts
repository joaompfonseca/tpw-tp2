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

  countryId: number | undefined;

  header: string | undefined;
  user: User | undefined;
  country: Country | undefined;
  circuits: Circuit[] | undefined;
  pilots: Pilot[] | undefined;

  constructor(
    private route: ActivatedRoute,
    private countryService: CountryService
  ) {
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
    this.countryService.getCountry(this.countryId!).subscribe(data => {
      this.header = data.header.header;
      this.user = data.auth;
      this.country = data.country;
      this.circuits = data.circuits;
      this.pilots = data.pilots;
    })
  }
}
