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

  raceId: number | undefined;

  header: string | undefined;
  user: User | undefined;
  race: Race | undefined;
  results: Result[] | undefined;

  constructor(
    private route: ActivatedRoute,
    private raceService: RaceService
  ) {
  }

  ngOnInit() {
    this.route.paramMap.subscribe(paramMap => {
      let id = paramMap.get('id');
      if (id !== null) {
        this.raceId = +id;
      }
      this.getRace();
    })
  }

  getRace() {
    this.raceService.getRace(this.raceId!).subscribe(data => {
      this.header = data.header.header;
      this.race = data.race;
      this.race!.circuit = data.circuit;
      this.race!.fast_lap = data.race.fast_lap;
      this.user = data.auth;
      let results = data.results;
      let pilots = data.pilots;
      for (let i = 0; i < results.length; i++) {
        results[i].pilot = {
          'id': pilots[i].id,
          'name': pilots[i].name
        };
      }
      this.results = data.results;
    })
  }
}
