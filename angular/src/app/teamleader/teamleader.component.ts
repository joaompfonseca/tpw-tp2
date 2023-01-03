import {Component, OnInit} from '@angular/core';
import {TeamLeader} from "../../interfaces/teamleader";
import {User} from "../../interfaces/user";
import {ActivatedRoute} from "@angular/router";
import {TeamLeaderService} from "../../services/teamleader/team-leader.service";
import {DomSanitizer} from "@angular/platform-browser";


@Component({
  selector: 'app-teamleader',
  templateUrl: './teamleader.component.html',
  styleUrls: ['./teamleader.component.css']
})
export class TeamleaderComponent implements OnInit {

  teamleaderId: number | undefined;

  header: string | undefined;
  user: User | undefined;
  teamleader: TeamLeader | undefined;

  constructor(
    private route: ActivatedRoute,
    private teamleaderService: TeamLeaderService,
    private sanitizer: DomSanitizer
  ) {
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
    this.teamleaderService.getTeamleader(this.teamleaderId!).subscribe(data => {
      this.header = data.header.header;
      this.user = data.auth;
      this.teamleader = data.teamleader;
      this.teamleader!.team = data.team;
      this.getTeamleaderImage();
    });
  }

  getTeamleaderImage() {
    this.teamleaderService.getTeamleaderImage(this.teamleaderId!).subscribe(
      image => {
        if (image.type == 'text/html')
          this.teamleader!.image = 'assets/images/pilot-default.jpg';
        else
          this.teamleader!.image = this.sanitizer.bypassSecurityTrustUrl(URL.createObjectURL(image));
      });
  }
}
