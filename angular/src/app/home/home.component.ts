import {Component, OnInit} from '@angular/core';
import {HomeService} from "../../services/home/home.service";
import {ActivatedRoute} from "@angular/router";
import {Home} from "../../interfaces/home";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  home: Home | undefined;

  constructor(
    private route: ActivatedRoute,
    private homeService: HomeService,
  ) { }

  ngOnInit() {
    this.getHome();
  }

  getHome() {
    this.homeService.get().subscribe(home => this.home = home);
  }
}
