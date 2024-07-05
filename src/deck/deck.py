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

from deck import Card
from typing_extensions import Self
from random import randint


class Deck:
    def __init__(self) -> None:
        self.cards: list[Card] = []
        self.isShuffled = False
        self.__add_cards()

    def shuffle(self) -> Self:
        """Returns the deck of cards shuffled."""
        self.isShuffled = True
        return self

    def draw(self) -> Card | None:
        """Returns a card from the deck."""
        result: Card | None

        if len(self.cards) == 0:
            result = None
        elif self.isShuffled:
            cardChoice: int = randint(0, len(self.cards) - 1)
            result = self.cards.pop(cardChoice)
        else:
            result = self.cards.pop()

        return result

    def __add__(self, otherDeck: Self) -> Self:
        """Puts to decks of cards together."""
        self.cards += otherDeck.cards

        return self

    def __len__(self) -> int:
        """Returns the number of cards in the deck."""
        return len(self.cards)

    def __mul__(self, num: int) -> Self:
        """Duplicates the cards in the deck num times."""
        self.cards *= num

        return self

    def __add_cards(self) -> Self:
        """Adds initial cards to the deck."""
        for suit in Card.Suit:
            for value in Card.Value:
                self.cards.append(Card(suit, value))

        return self
