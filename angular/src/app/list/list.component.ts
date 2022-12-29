import {Component, OnInit} from '@angular/core';

@Component({
  selector: 'app-list',
  templateUrl: './list.component.html',
  styleUrls: ['./list.component.css']
})
export class ListComponent implements OnInit {

  header: string;
  actions: { url: string, str: string }[];
  list: { url: string, str: string }[][];
  query?: string;

  constructor() {
    // TODO: fetch from API
    this.header = 'List of Pilots';
    this.actions = [
      {url: '/pilots/search', str: 'Search Pilot'},
    ];
    this.list = [
      [{url: '/pilots/1', str: 'Lewis Hamilton'}],
      [{url: '/pilots/2', str: 'Valtteri Bottas'}],
      [{url: '/pilots/3', str: 'Max Verstappen'}],
    ];
  }

  ngOnInit() {
  }
}
