import {
  ChangeDetectorRef,
  Component,
  OnDestroy,
  OnInit,
  ViewEncapsulation,
} from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { untilDestroyed, UntilDestroy } from '@ngneat/until-destroy';
import { PlayersService } from '../_services/players.service';

@UntilDestroy()
@Component({
  selector: 'player-summary-component',
  templateUrl: './player-summary.component.html',
  styleUrls: ['./player-summary.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class PlayerSummaryComponent implements OnInit, OnDestroy {
  playerId: number;
  playerSummary: any;
  errorMessage: string;

  constructor(
    protected activatedRoute: ActivatedRoute,
    protected cdr: ChangeDetectorRef,
    protected playersService: PlayersService
  ) {}

  ngOnInit(): void {
    this.playerId = 1;
  }

  fetchPlayerSummary(): void {
    if (this.playerId && this.playerId > 0) {
      this.playersService
        .getPlayerSummary(this.playerId)
        .pipe(untilDestroyed(this))
        .subscribe({
          next: (data) => {
            this.playerSummary = data.apiResponse;
            console.log(this.playerSummary);
            this.playerSummary.games.forEach((game) => {
              game.shots.forEach((shot) => {
                shot.description = this.getShotDescription(shot);
              });
            });
          },
          error: (err) => {
            if (err.status === 404) {
              this.errorMessage = err.response.error.error; 
              this.playerSummary = null; 
            } else {
              this.errorMessage = 'An unexpected error occurred';
              this.playerSummary = null; 
            }
          },
        });
    }
  }

  isThree(x: number, y: number) {
    if (Math.abs(x) >= 22 || Math.sqrt(x * x + y * y) >= 23.75) {
      return true;
    }
    return false;
  }

  getShotDescription(shot: {
    isMake: boolean;
    locationX: number;
    locationY: number;
  }): string {
    const { locationX, locationY, isMake } = shot;

    const isThreePointer = this.isThree(locationX, locationY);
    const distanceFromBasket = parseFloat(
      Math.sqrt(locationX * locationX + locationY * locationY).toFixed(1)
    );
    const shotType =
      distanceFromBasket > 28
        ? 'deep 3-pt'
        : isThreePointer
        ? '3-pt'
        : distanceFromBasket <= 10
        ? 'close-range'
        : 'mid-range';

    let shotDescription = `${
      isMake ? 'Made' : 'Missed'
    } ${shotType} shot from ${
      distanceFromBasket <= 1
        ? 'less than a foot away'
        : `${distanceFromBasket} feet away`
    }  (${locationX}, ${locationY}) ${
      isMake && isThreePointer
        ? '+3 points'
        : isMake && !isThreePointer
        ? '+2 points'
        : ''
    } `;

    return shotDescription;
  }

  ngOnDestroy() {}
}
