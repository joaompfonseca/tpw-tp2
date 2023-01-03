import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable} from "rxjs";
import {Profile} from "../../interfaces/profile";


const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'}),
  withCredentials: true
};

@Injectable({
  providedIn: 'root'
})
export class ProfileService {
  private baseURL = 'http://localhost:8000/ws/';

  constructor(private http: HttpClient) {
  }

  getProfile(): Observable<Profile> {
    const url = this.baseURL + 'profile';
    return this.http.get<Profile>(url, {withCredentials: true});
  }

  getProfileImage(): Observable<Blob> {
    const url = this.baseURL + "image/profile";
    return this.http.get(url, {withCredentials: true, responseType: 'blob'});
  }

  updateProfile(profile: Profile): Observable<any> {
    const url = this.baseURL + 'profileupdate';
    return this.http.put(url, profile, httpOptions);
  }

  toggleFavouritePilot(id: number, bool: boolean): Observable<any> {
    const url = this.baseURL + 'pilotfav' + ((bool) ? 'add' : 'rem') + '?id=' + id;
    return this.http.post(url, {}, {withCredentials: true});
  }

  toggleFavouriteTeam(id: number, bool: boolean): Observable<any> {
    const url = this.baseURL + 'teamfav' + ((bool) ? 'add' : 'rem') + '?id=' + id;
    return this.http.post(url, {}, {withCredentials: true});
  }
}
