"""
Logic for having a deck of cards.

NOTE: THIS DOES NOT NECESSARILY HAVE ANYTHING TO DO WITH BLACKJACK!

We have 52 cards:
    4 Suits:
        Clubs, Spades, Hearts, Diamonds

        9 Number cards:
            2 - 10

        3 Face cards:
            Jack
            Queen
            King

        1 Ace
"""

from typing import Self
import Card


class Deck:
    def __init__(self) -> None:
        self.cards: list[Card] = []

    def shuffle(self) -> Self:
        """Returns the deck of cards shuffled."""
        return self
