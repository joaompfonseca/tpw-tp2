import { Injectable } from '@angular/core';
import {TeamLeader} from "../../interfaces/teamleader"
import {Observable} from "rxjs";
import {HttpClient, HttpHeaders} from "@angular/common/http";



const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root'
})
export class TeamLeaderService {
  private baseURL = 'http://localhost:8000/ws/';
  constructor(private http: HttpClient) { }

  getTeamLeader(id: number): Observable<any> {
    const url = this.baseURL + "teamleader?id=" + id;
    return this.http.get<any>(url);
  }

  getTeamLeaders(): Observable<TeamLeader[]> {
    const url = this.baseURL + "teamleaders";
    return this.http.get<TeamLeader[]>(url);
  }

  createTeamLeader(teamleader: TeamLeader): Observable<any> {
    const url = this.baseURL + "teamleadercre";
    return this.http.post(url, teamleader, httpOptions)
  }

  searchTeamLeader(name: string): Observable<TeamLeader[]> {
    const url = this.baseURL + "teamleadersearch?name=" + name;
    return this.http.get<TeamLeader[]>(url);
  }

  updateTeamLeader(id: number, teamleader: TeamLeader): Observable<any>{
    const url = this.baseURL + "teamleaderupdate?id=" + id;
    return this.http.put(url, teamleader, httpOptions);
  }
}
