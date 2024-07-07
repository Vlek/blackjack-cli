from pathlib import Path
import json
from datetime import date

from blackjack.blackjack import GameState
from blackjack.models import BlackjackStats


class Stats:
    def __init__(self, statsFilePath: Path) -> None:
        """Initializes a stats collection object."""

        self.data: BlackjackStats = BlackjackStats()

        if statsFilePath.exists():
            with open(statsFilePath, "r") as statsFile:
                self.data.deserialize(json.load(statsFile))

    def save(self, statsFilePath: Path, gameState: GameState) -> None:
        """Saves the last game's state to the stats file."""
        self.data._last_played = str(date.today())

        match gameState:
            case winType if winType in [GameState.Win, GameState.Blackjack]:
                if winType == GameState.Win:
                    self.data._wins += 1
                else:
                    self.data._blackjacks += 1

                if self.data._last_outcome in [GameState.Win, GameState.Blackjack]:
                    self.data._current_streak += 1

                    if self.data._longest_win_streak < self.data._current_streak:
                        self.data._longest_win_streak = self.data._current_streak

            case GameState.Lose:
                self.data._losses += 1

                if self.data._last_outcome == GameState.Lose:
                    self.data._current_streak += 1

                    if self.data._longested_losing_streak < self.data._current_streak:
                        self.data._longested_losing_streak = self.data._current_streak

            case GameState.Push:
                self.data._pushes += 1

        self.data._last_outcome = gameState

        with open(statsFilePath, "w") as statsFile:
            json.dump(self.data.serialize(), statsFile)
