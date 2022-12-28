import {Pilot} from "./pilot";
import {Country} from "./country";

export interface Circuit {
  id: number
  name: string
  length: number
  location: string
  last_winner: Pilot
  country: Country
}
