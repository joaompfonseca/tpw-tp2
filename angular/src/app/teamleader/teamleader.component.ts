import {Component, OnInit} from '@angular/core';
import {TeamLeader} from "../../interfaces/teamleader";
import {User} from "../../interfaces/user";

@Component({
  selector: 'app-teamleader',
  templateUrl: './teamleader.component.html',
  styleUrls: ['./teamleader.component.css']
})
export class TeamleaderComponent implements OnInit {

  header: string;
  user: User;
  teamleader: TeamLeader;

  constructor() {
    // TODO: fetch from API
    this.header = 'Team Leader Details';
    this.user = {
      is_authenticated: true,
      is_superuser: true
    }
    this.teamleader = {
      id: 1,
      image: '',
      name: 'Toto Wolff',
      team: {
        id: 1,
        name: 'Mercedes',
        date: new Date('2010-01-01'),
        championships: 5,
        points: 1000,
        image: ''
      }
    };
  }


  ngOnInit() {
  }

  getTeamleader() {
    // const id = +this.route.snapshot.paramMap.get('id');
    // this.teamleaderService.getTeamleader(id).subscribe(teamleader => this.teamleader = teamleader);
  }
}
