import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {User} from "../../interfaces/user";

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private baseURL = 'http://localhost:8000/ws/';
  constructor(private http: HttpClient) { }

  getUser(): Observable<User> {
    const url = this.baseURL + "user";
    return this.http.get<User>(url);
  }

  login(username: string, password: string): Observable<User> {
    const url = this.baseURL + "login";
    return this.http.post<User>(url, {username: username, password: password});
  }
}
