import { Injectable } from '@angular/core';
import {Team} from "../../interfaces/team"
import {Observable} from "rxjs";
import {HttpClient, HttpHeaders} from "@angular/common/http";



const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'}),
  withCredentials: true
};

@Injectable({
  providedIn: 'root'
})
export class TeamService {
  private baseURL = 'http://localhost:8000/ws/';
  constructor(private http: HttpClient) { }

  getTeam(id: number): Observable<any> {
    const url = this.baseURL + "team?id=" + id;
    return this.http.get<any>(url);
  }

  getTeamImage(id: number): Observable<Blob> {
    const url = this.baseURL + "image/team/" + id;
    return this.http.get(url, {responseType: 'blob'});
  }

  getTeams(): Observable<Team[]> {
    const url = this.baseURL + "teams";
    return this.http.get<Team[]>(url);
  }

  createTeam(team: Team): Observable<any> {
    const url = this.baseURL + "teamcreate";
    return this.http.post(url, team, httpOptions)
  }

  searchTeam(name: string): Observable<Team[]> {
    const url = this.baseURL + "teamsearch?name=" + name;
    return this.http.get<Team[]>(url);
  }

  updateTeam(id: number, team: Team): Observable<any>{
    const url = this.baseURL + "teamupdate?id=" + id;
    return this.http.put(url, team, httpOptions);
  }
}
