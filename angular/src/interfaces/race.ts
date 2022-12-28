import {Circuit} from "./circuit";

export interface Race {
  id: number
  name: string
  date: Date
  season: number
  fast_lap: string
  circuit: Circuit
}
