from typing import Any
from blackjack_cli.blackjack import GameState
from typing_extensions import Self


class BlackjackStats:
    _wins: int = 0
    _losses: int = 0
    _pushes: int = 0
    _blackjacks: int = 0
    _longest_win_streak: int = 0
    _longested_losing_streak: int = 0
    _longest_push_streak: int = 0
    _current_streak: int = 0
    _last_outcome: GameState = GameState.Playing
    _last_played: str = ""

    def __init__(self) -> None:
        """Initializes a BlackjackStats object."""

    def deserialize(self, data: dict[str, Any]) -> Self:
        """Imports a json string, updates class variables."""

        if "_last_outcome" in data:
            data["_last_outcome"] = GameState(data["_last_outcome"])

        self.__dict__ = data

        return self

    def serialize(self) -> dict[str, Any]:
        """Exports class data as a saveable dict"""

        result: dict[str, Any] = self.__dict__
        result["_last_outcome"] = self._last_outcome.value

        return result

    def __str__(self) -> str:
        """Returns a string representation of the stats values"""
        result: list[str] = []
        values: dict[str, Any] = self.__dict__

        keysToOutput: dict[str, str] = {
            "_wins": "Wins",
            "_losses": "Losses",
            "_pushes": "Pushes",
            "_blackjacks": "Blackjacks",
            "_longest_win_streak": "Longest winning streak",
            "_longested_losing_streak": "Longest losing streak",
            "_longest_push_streak": "Longest push streak",
            "_current_streak": "Current streak",
            "_last_played": "Last played",
        }

        for key, value in keysToOutput.items():
            if key in values:
                result.append(f"{value}: {values[key]}")

        return "  " + "\n  ".join(result)
