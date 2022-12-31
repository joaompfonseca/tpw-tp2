import {Component, OnInit} from '@angular/core';
import {User} from "../../interfaces/user";
import {Pilot} from "../../interfaces/pilot";
import {Result} from "../../interfaces/result";
import {PilotService} from "../../services/pilot/pilot.service";
import {ActivatedRoute} from "@angular/router";

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
  points: number;

  isFavourite: boolean;
  likeImage: string;
  dislikeImage: string;
  pilotId: number;

  constructor(private route: ActivatedRoute, private pilotService: PilotService) {
    this.header = '';
    this.pilotId = 0;
    this.user = {
      is_authenticated: false,
      is_superuser: false,
    }
    this.pilot = {
      id: 0,
      name: '',
      country: [{
        id: 0,
        designation: '',
        code: '',
      }],
      team: {
        id: 0,
        name: '',
        date: new Date(),
        championships: 0,
        image: '',},
      victories: 0,
      pole_positions: 0,
      podiums: 0,
      championships: 0,
      contract: 0,
      entry_year: 0,
      image: '',
      }
    this.results = [];
    this.points = 0;
    this.isFavourite = true;
    this.likeImage = '';
    this.dislikeImage = '';
  }

  ngOnInit() {
    this.route.paramMap.subscribe(paramMap  => {
      let id = paramMap.get('id');
     if (id !== null) {
       this.pilotId = +id;
     }
     this.getPilot();
    })
  }

  getPilot() {
    this.pilotService.getPilot(this.pilotId).subscribe(data => {
      this.pilot = data.pilot;
      this.pilot.country = data.country;
      this.pilot.team = data.team;
      this.results = data.results;
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
