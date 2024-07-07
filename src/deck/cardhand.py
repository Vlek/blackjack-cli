"""
This deals with holding and evaluating cards that
a player has in their hand.
"""

from deck import Card
from typing_extensions import Self

from typing import Callable


class CardHand:

    def __init__(self, cards: list[Card | None], scoringStrategy: Callable[[list[Card]], int] = lambda x: -1) -> None:
        """Initializes a cardhand."""

        self.cards: list[Card] = [c for c in cards if c is not None]
        self.scoringStrategy = scoringStrategy

    def setScoringStrategy(self, scoringStrategy: Callable[[list[Card]], int]) -> Self:
        """Sets the strategy for how to score the given hand."""
        self.scoringStrategy = scoringStrategy
        return self

    def getScore(self) -> int:
        """Returns the score of the current hand with the given strategy."""
        return self.scoringStrategy(self.cards)

    def add(self, card: Card | None) -> Self:
        """Add a card to the player's hand."""
        if card is not None:
            self.cards.append(card)
        return self

    def __str__(self) -> str:
        """Returns string representation of the cardhand."""
        return " ".join(str(c) for c in self.cards)
