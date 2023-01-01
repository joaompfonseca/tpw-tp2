import {TeamLeader} from "./teamleader";
import {SafeUrl} from "@angular/platform-browser";

export interface Team {
  id: number
  name: string
  date?: Date
  championships?: number
  points?: number
  image?: SafeUrl
  teamleader?: TeamLeader
}
