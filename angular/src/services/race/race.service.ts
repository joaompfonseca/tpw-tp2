import { Injectable } from '@angular/core';
import {Race} from "../../interfaces/race"
import {Observable} from "rxjs";
import {HttpClient, HttpHeaders} from "@angular/common/http";

const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root'
})
export class RaceService {
  private baseURL = 'http://localhost:8000/ws/';
  constructor(private http: HttpClient) { }

  getRace(id: number): Observable<Race> {
    const url = this.baseURL + "race?id=" + id;
    return this.http.get<Race>(url);
  }

  getRaces(): Observable<Race[]> {
    const url = this.baseURL + "races";
    return this.http.get<Race[]>(url);
  }

  createRace(race: Race): Observable<any> {
    const url = this.baseURL + "racecre";
    return this.http.post(url, race, httpOptions)
  }

  searchRace(name: string): Observable<Race[]> {
    const url = this.baseURL + "racesearch?name=" + name;
    return this.http.get<Race[]>(url);
  }

  updateRace(id: number, race: Race): Observable<any>{
    const url = this.baseURL + "raceupdate?id=" + id;
    return this.http.put(url, race, httpOptions);
  }
}
