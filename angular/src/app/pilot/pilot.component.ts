import {Component, OnInit} from '@angular/core';
import {User} from "../../interfaces/user";
import {Pilot} from "../../interfaces/pilot";
import {Result} from "../../interfaces/result";
import {Race} from "../../interfaces/race";
import {PilotService} from "../../services/pilot/pilot.service";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-pilot',
  templateUrl: './pilot.component.html',
  styleUrls: ['./pilot.component.css']
})
export class PilotComponent implements OnInit {

  pilotId: number | undefined;

  header: string | undefined;
  user: User | undefined;
  pilot: Pilot | undefined;
  results: Result[] | undefined;
  points: number | undefined;
  // TODO: Fetch API
  isFavourite: boolean = false;
  likeImage: string = '';
  dislikeImage: string = '';

  constructor(
    private route: ActivatedRoute,
    private pilotService: PilotService
  ) {
  }

  ngOnInit() {
    this.route.paramMap.subscribe(paramMap => {
      let id = paramMap.get('id');
      if (id !== null) {
        this.pilotId = +id;
      }
      this.getPilot();
    })
  }

  getPilot() {
    this.pilotService.getPilot(this.pilotId!).subscribe(data => {
      this.pilot = data.pilot;
      this.pilot!.country = data.country;
      this.pilot!.team = data.team;
      this.pilot!.points = data.points.points;
      this.results = data.results;
      this.results!.forEach(result => {
        for (let race of data.races) {
          if (result.race == race.id) {
            result.race = race;
          }
        }
      })
      this.points = data.points.points;
      this.user = data.auth;
      this.header = data.header.header;
    });
  }

  addToFavourites() {
  }

  removeFromFavourites() {
  }
}
