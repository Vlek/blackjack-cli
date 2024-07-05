"""
Handles the logic for a single Card within a Deck.
"""

from enum import Enum


class Card:
    class Suit(Enum):
        SPADES = "♠"
        CLUBS = "♣"
        DIAMONDS = "♦"
        HEARTS = "♥"

    class Value(Enum):
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
        SIX = 6
        SEVEN = 7
        EIGHT = 8
        NINE = 9
        TEN = 10
        JACK = "J"
        QUEEN = "Q"
        KING = "K"
        ACE = "A"

    def __init__(self, suit: Suit, value: Value) -> None:
        self.suit = suit
        self.value = value

    def __str__(self) -> str:
        """Returns the string representation of a Card."""
        return f"{self.suit.value}{self.value.value}"

    def __eq__(self, otherCard) -> bool:
        """Determine whether one card is the same as the other."""
        return self.suit == otherCard.suit and self.value == otherCard.value


if __name__ == "__main__":
    card = Card(Card.Suit.SPADES, Card.Value.ACE)
    otherCard = Card(Card.Suit.SPADES, Card.Value.ACE)

    print(card)

    print(card == otherCard)
