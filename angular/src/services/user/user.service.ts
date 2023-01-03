import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable} from "rxjs";
import {User} from "../../interfaces/user";

const httpOptions = {
  headers: new HttpHeaders({'Content-Type': 'application/json'}),
  withCredentials: true
};

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private baseURL = 'http://localhost:8000/ws/';

  constructor(private http: HttpClient) {
  }

  getUser(): Observable<User> {
    const url = this.baseURL + 'user';
    return this.http.get<User>(url, httpOptions);
  }

  signup(username: string, email: string, password: string): Observable<User> {
    const url = this.baseURL + 'signup';
    return this.http.post<User>(url, {username: username, email: email, password: password}, httpOptions);
  }

  login(username: string, password: string): Observable<User> {
    const url = this.baseURL + 'login';
    return this.http.post<User>(url, {username: username, password: password}, httpOptions);
  }

  logout(): Observable<any> {
    const url = this.baseURL + 'logout';
    return this.http.get(url, httpOptions);
  }
}
