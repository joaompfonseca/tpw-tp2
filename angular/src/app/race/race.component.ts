import {Component, OnInit} from '@angular/core';
import {Race} from "../../interfaces/race";
import {User} from "../../interfaces/user";
import {Result} from "../../interfaces/result";
import {ActivatedRoute} from "@angular/router";
import {RaceService} from "../../services/race/race.service";

@Component({
  selector: 'app-race',
  templateUrl: './race.component.html',
  styleUrls: ['./race.component.css']
})
export class RaceComponent implements OnInit {

  header: string
  raceId: number;
  user: User
  race: Race
  results: Result[]

  constructor(private route: ActivatedRoute, private raceService: RaceService) {
    this.header = '';
    this.raceId = 0;
    this.user = {
      is_authenticated: false,
      is_superuser: false
    };
    this.race = {
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
    };
    this.results = [
      {
        id: 0,
        position: 0,
        pilot: {
          id: 0,
          name: '',
          team: {
            id: 0,
            name: '',
          }
        },
        race: {
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
        },
        points: 0
      }
    ]
  }

  ngOnInit() {
    this.route.paramMap.subscribe(paramMap  => {
      let id = paramMap.get('id');
      if (id !== null) {
        this.raceId = +id;
      }
      this.getRace();
    })
  }

  getRace() {
    this.raceService.getRace(this.raceId).subscribe(data => {
      console.log(data);
      this.header = data.header.header;
      this.race = data.race;
      this.race.circuit = data.circuit;
      this.race.fast_lap = data.race.fast_lap.substring(3);
      this.user = data.auth;
      let results = data.results;
      let pilots = data.pilots;
      for (let i = 0; i < results.length; i++) {
        results[i].pilot = pilots[i].name;
      }
      this.results = data.results;

    })
  }
}
