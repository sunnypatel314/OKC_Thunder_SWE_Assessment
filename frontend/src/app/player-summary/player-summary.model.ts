export interface Shot {
    isMake: boolean;
    locationX: number;
    locationY: number;
  }
  
  export interface Game {
    date: string;
    isStarter: boolean;
    minutes: number;
    points: number;
    assists: number;
    offensiveRebounds: number;
    defensiveRebounds: number;
    steals: number;
    blocks: number;
    shots: Shot[];
  }
  
  export interface PlayerSummary {
    name: string;
    games: Game[];
  }
  