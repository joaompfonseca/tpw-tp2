export interface Home {
  stats: {total_pilots: number, total_teams: number, total_races: number}
  pilots_leaderboard: {id: number, name: string, points: number}[]
  teams_leaderboard: {id: number, name: string, points: number}[]
}
