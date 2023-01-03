import {Component} from '@angular/core';
import {User} from "../../interfaces/user";
import {Team} from "../../interfaces/team";
import {Pilot} from "../../interfaces/pilot";
import {ActivatedRoute} from "@angular/router";
import {TeamService} from "../../services/team/team.service";
import {DomSanitizer} from "@angular/platform-browser";
import {ProfileService} from "../../services/profile/profile.service";

@Component({
  selector: 'app-team',
  templateUrl: './team.component.html',
  styleUrls: ['./team.component.css']
})
export class TeamComponent {

  teamId: number | undefined;

  header: string | undefined;
  user: User | undefined;
  team: Team | undefined;
  pilots: Pilot[] | undefined;
  // TODO: Fetch API
  isFavourite: boolean = false;
  likeImage: string = '';
  dislikeImage: string = '';

  constructor(
    private route: ActivatedRoute,
    private teamService: TeamService,
    private profileService: ProfileService,
    private sanitizer: DomSanitizer
  ) {
  }


  ngOnInit() {
    this.route.paramMap.subscribe(paramMap => {
      let id = paramMap.get('id');
      if (id !== null) {
        this.teamId = +id;
      }
      this.getTeam();
    })
  }

  getTeam() {
    this.teamService.getTeam(this.teamId!).subscribe(data => {
      this.team = data.team;
      this.team!.teamleader = data.teamleader;
      this.team!.points = data.points.points;
      this.team!.is_fav = data.is_fav.is_fav;
      this.header = data.header.header;
      this.pilots = data.pilots;
      this.user = data.auth;
      this.getTeamImage();
    });
  }

  getTeamImage() {
    this.teamService.getTeamImage(this.teamId!).subscribe(
      image => {
        this.team!.image = this.sanitizer.bypassSecurityTrustUrl(URL.createObjectURL(image));
      });
  }

  toggleFavourite() {
    const bool = !this.team!.is_fav;
    this.team!.is_fav = bool;
    this.profileService.toggleFavouriteTeam(this.teamId!, bool).subscribe();
  }
}
