import {Component, OnInit} from '@angular/core';
import {User} from "../../interfaces/user";
import {Pilot} from "../../interfaces/pilot";
import {Result} from "../../interfaces/result";
import {Race} from "../../interfaces/race";
import {PilotService} from "../../services/pilot/pilot.service";
import {ActivatedRoute} from "@angular/router";
import {DomSanitizer} from "@angular/platform-browser";
import {ProfileService} from "../../services/profile/profile.service";

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
    private pilotService: PilotService,
    private profileService: ProfileService,
    private sanitizer: DomSanitizer
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
      console.log(data)
      this.pilot = data.pilot;
      this.pilot!.country = data.country;
      this.pilot!.team = data.team;
      this.pilot!.points = data.points.points;
      this.pilot!.is_fav = data.is_fav.is_fav;
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
      this.getPilotImage();
    });
  }

  getPilotImage() {
    this.pilotService.getPilotImage(this.pilotId!).subscribe(
      image => {
        if (image.type == 'text/html')
          this.pilot!.image = 'assets/images/teamleader-default.jpg';
        else
          this.pilot!.image = this.sanitizer.bypassSecurityTrustUrl(URL.createObjectURL(image));
      });
  }

  toggleFavourite() {
    const bool = !this.pilot!.is_fav;
    this.pilot!.is_fav = bool;
    this.profileService.toggleFavouritePilot(this.pilotId!, bool).subscribe();
  }
}
