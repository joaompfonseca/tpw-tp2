import {Injectable} from '@angular/core';
import {Pilot} from "../../interfaces/pilot"
import {Observable} from "rxjs";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {DomSanitizer} from "@angular/platform-browser";


const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'})
};

@Injectable({
  providedIn: 'root'
})
export class PilotService {
  private baseURL = 'http://localhost:8000/ws/';

  constructor(private http: HttpClient) {
  }

  getPilot(id: number): Observable<any> {
    const url = this.baseURL + "pilot?id=" + id;
    let pilot: Observable<any> = this.http.get<any>(url);
    return pilot;
  }

  getPilotImage(id: number): Observable<Blob> {
    const url = this.baseURL + "image/pilot/" + id;
    return this.http.get(url, {responseType: 'blob'});
  }

  getPilots(): Observable<Pilot[]> {
    const url = this.baseURL + "pilots";
    let pilots: Observable<Pilot[]> = this.http.get<Pilot[]>(url);
    return pilots;
  }

  createPilot(pilot: Pilot): Observable<any> {
    const url = this.baseURL + "pilotcreate";
    return this.http.post(url, pilot, httpOptions)
  }

  searchPilot(name: string): Observable<Pilot[]> {
    const url = this.baseURL + "pilotsearch?name=" + name;
    return this.http.get<Pilot[]>(url);
  }

  updatePilot(id: number, pilot: Pilot): Observable<any> {
    const url = this.baseURL + "pilotupdate?id=" + id;
    return this.http.put(url, pilot, httpOptions);
  }
}
