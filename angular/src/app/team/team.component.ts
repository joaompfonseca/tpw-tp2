import {Component} from '@angular/core';
import {User} from "../../interfaces/user";
import {Team} from "../../interfaces/team";
import {Pilot} from "../../interfaces/pilot";
import {ActivatedRoute} from "@angular/router";
import {TeamService} from "../../services/team/team.service";

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
  teamId: number;
  isFavourite: boolean;
  likeImage: string;
  dislikeImage: string;

  constructor(private route: ActivatedRoute, private teamService: TeamService) {
    this.teamId = 0;
    this.header = '';
    this.user = {
      is_authenticated: false,
      is_superuser: false
    }

    this.team = {
      id: 0,
      name: '',

    };
    this.pilots = [
      {
        id: 0,
        name: '',
        team: {
          id: 0,
          name: '',
        },
      }
    ];
    this.isFavourite = true;
    this.likeImage = '';
    this.dislikeImage = '';
  }


  ngOnInit() {
    this.route.paramMap.subscribe(paramMap  => {
      let id = paramMap.get('id');
      if (id !== null) {
        this.teamId = +id;
      }
      this.getTeam();
    })
  }

  getTeam() {
  this.teamService.getTeam(this.teamId).subscribe(data => {
    console.log(data);
    this.team = data.team;
    this.team.teamleader = data.teamleader;
    this.team.points = data.points.points;
    this.header = data.header.header;
    this.pilots = data.pilots;
    this.user = data.auth;

  });
  }

  addToFavourites() {
  }

  removeFromFavourites() {
  }
}
