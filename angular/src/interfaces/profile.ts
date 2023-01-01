import {User} from "./user";
import {SafeUrl} from "@angular/platform-browser";

export interface Profile {
  id: number;
  user: User;
  image?: SafeUrl;
  biography: string;
  favourite_pilot: {id: number, name: string, image?: SafeUrl}[];
  favourite_team: {id: number, name: string, image?: SafeUrl}[];
}
