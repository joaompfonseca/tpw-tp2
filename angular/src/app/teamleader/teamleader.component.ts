import {Component, OnInit} from '@angular/core';
import {TeamLeader} from "../../interfaces/teamleader";
import {User} from "../../interfaces/user";
import {ActivatedRoute} from "@angular/router";
import {TeamLeaderService} from "../../services/teamleader/team-leader.service";


@Component({
  selector: 'app-teamleader',
  templateUrl: './teamleader.component.html',
  styleUrls: ['./teamleader.component.css']
})
export class TeamleaderComponent implements OnInit {

  header: string;
  teamleaderId: number;
  user: User;
  teamleader: TeamLeader;

  constructor(private route: ActivatedRoute, private teamleaderService: TeamLeaderService) {
    this.header = '';
    this.teamleaderId = 0;
    this.user = {
      is_authenticated: false,
      is_superuser: false
    }
    this.teamleader = {
      id: 0,
      image: '',
      name: '',
      team: {
        id: 0,
        name: '',
      }
    };
  }


  ngOnInit() {
    this.route.paramMap.subscribe(paramMap => {
      let id = paramMap.get('id');
      if (id !== null) {
        this.teamleaderId = +id;
      }
      this.getTeamleader();
    })
  }

  getTeamleader() {
this.teamleaderService.getTeamLeader(this.teamleaderId).subscribe(data => {
      console.log(data);
      this.header = data.header.header;
      this.user = data.auth;
      this.teamleader = data.teamleader;
      this.teamleader.team = data.team;
    });

  }
}
