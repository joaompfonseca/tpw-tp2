import {Team} from "./team";
import {Country} from "./country";
import {SafeUrl} from "@angular/platform-browser";

export interface Pilot {
  id: number;
  name: string;
  date?: Date;
  victories?: number;
  pole_positions?: number;
  podiums?: number;
  championships?: number;
  points?: number;
  contract?: number;
  entry_year?: number;
  team: Team;
  country?: Country[];
  image?: SafeUrl;
  is_fav: boolean;
}
