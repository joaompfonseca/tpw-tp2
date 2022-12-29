import {Race} from "./race";
import {Pilot} from "./pilot";

export interface Result {
  id: number
  position: number
  pilot: Pilot
  race: Race
  points: number
}
