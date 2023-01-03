import {Injectable} from '@angular/core';
import {TeamLeader} from "../../interfaces/teamleader"
import {Observable} from "rxjs";
import {HttpClient, HttpHeaders} from "@angular/common/http";


const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'}),
  withCredentials: true
};

@Injectable({
  providedIn: 'root'
})
export class TeamLeaderService {
  private baseURL = 'http://localhost:8000/ws/';

  constructor(private http: HttpClient) {
  }

  getTeamleader(id: number): Observable<any> {
    const url = this.baseURL + "teamleader?id=" + id;
    return this.http.get<any>(url, httpOptions);
  }

  getTeamleaderImage(id: number): Observable<Blob> {
    const url = this.baseURL + "image/teamleader/" + id;
    return this.http.get(url, {...httpOptions, responseType: 'blob'});
  }

  getTeamleaders(): Observable<TeamLeader[]> {
    const url = this.baseURL + "teamleaders";
    return this.http.get<TeamLeader[]>(url, httpOptions);
  }

  createTeamLeader(teamleader: any): Observable<any> {
    const url = this.baseURL + "teamleadercreate";
    return this.http.post(url, teamleader, httpOptions)
  }

  searchTeamLeader(name: string): Observable<TeamLeader[]> {
    const url = this.baseURL + "teamleadersearch?name=" + name;
    return this.http.get<TeamLeader[]>(url, httpOptions);
  }

  updateTeamLeader(id: number, teamleader: any): Observable<any> {
    const url = this.baseURL + "teamleaderupdate?id=" + id;
    return this.http.put(url, teamleader, httpOptions);
  }
}
