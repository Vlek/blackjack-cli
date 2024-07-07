from pathlib import Path
import json
from datetime import date
from typing import Any

from blackjack.blackjack import GameState


class Stats:
    structure: dict[str, Any] = {
        "wins": 0,
        "losses": 0,
        "pushes": 0,
        "blackjacks": 0,
        "longest winning streak": 0,
        "longest losing streak": 0,
        "last played": None,
        "last outcome": None,
        "current streak": 0,
    }

    def __init__(self, statsFilePath: Path) -> None:
        """Initializes a stats collection object."""

        self.list: dict[str, object] = Stats.structure

        if statsFilePath.exists():
            with open(statsFilePath, "r") as statsFile:
                self.list = json.load(statsFile)

    def save(self, statsFilePath: Path, gameState: GameState) -> None:
        """Saves the last game's state to the stats file."""
        self.list["last played"] = str(date.today())

        lastOutcome: str = ""
        if isinstance(self.list["last outcome"], str):
            lastOutcome = self.list["last outcome"]

        match gameState:
            case winType if winType in [GameState.Win, GameState.Blackjack]:
                if winType == GameState.Win:
                    if isinstance(self.list["wins"], int):
                        self.list["wins"] += 1
                else:
                    if isinstance(self.list["blackjacks"], int):
                        self.list["blackjacks"] += 1

                if isinstance(self.list["current streak"], int):
                    if lastOutcome == "win":
                        self.list["current streak"] += 1
                        if (
                            isinstance(
                                longestWinStreak := self.list["longest winning streak"],
                                int,
                            )
                            and longestWinStreak < self.list["current streak"]
                        ):
                            self.list["longest winning streak"] = self.list[
                                "current streak"
                            ]
                    else:
                        self.list["current streak"] = 1

                self.list["last outcome"] = "win"

            case GameState.Lose:
                if isinstance(self.list["losses"], int):
                    self.list["losses"] += 1

                if isinstance(self.list["current streak"], int):
                    if lastOutcome == "lose":
                        self.list["current streak"] += 1
                        if (
                            isinstance(
                                longestLoseStreak := self.list["longest losing streak"],
                                int,
                            )
                            and longestLoseStreak < self.list["current streak"]
                        ):
                            self.list["longest losing streak"] = self.list[
                                "current streak"
                            ]
                    else:
                        self.list["current streak"] = 1

                self.list["last outcome"] = "lose"

            case GameState.Push:
                if isinstance(self.list["pushes"], int):
                    self.list["pushes"] += 1

        with open(statsFilePath, "w") as statsFile:
            json.dump(self.list, statsFile)
