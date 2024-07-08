"""
This is the base logic file for all of the Blackjack game code.

This is going to house things like:
    - What is a deck?
    - What is a player/dealer?
    - Turn order
"""

from enum import Enum
from typing_extensions import Self

from deck import Deck, Card, CardHand


def blackjackScoringStrategy(cards: list[Card]) -> int:
    """Returns the score of a given list of cards."""

    # We do a shallow copy so that we do not mess up the order.
    cards = cards.copy()

    def aceLastSorting(key: Card) -> int:
        """Puts aces last in a list of cards when sorting."""
        if key.value == Card.Value.ACE:
            return 1
        return 0

    cards.sort(key=aceLastSorting)

    result: int = 0

    for card in cards:
        if isinstance(card.value.value, int):
            value: int = card.value.value
        elif card.value == Card.Value.ACE:
            if result + 11 > 21:
                value = 1
            else:
                value = 11
        else:
            value = 10

        result += value
    return result


class GameState(Enum):
    Playing = "playing"
    Win = "wins"
    Lose = "losses"
    Blackjack = "blackjacks"
    Push = "pushes"


class Blackjack:
    def __init__(self) -> None:
        self.gameState: GameState = GameState.Playing

        # Standard blackjack is played with 4 decks
        # instead of just one.
        self.deck: Deck = Deck() * 4
        self.deck.shuffle()

        self.playersCards: CardHand = CardHand([self.deck.draw(), self.deck.draw()])
        self.dealersCards: CardHand = CardHand([self.deck.draw(), self.deck.draw()])

        for hand in [self.playersCards, self.dealersCards]:
            hand.setScoringStrategy(blackjackScoringStrategy)

        playersScore: int = self.playersCards.getScore()
        dealersScore: int = self.dealersCards.getScore()

        # If one or both blackjack:
        if playersScore == 21:
            self.gameState = GameState.Blackjack

            if dealersScore == 21:
                self.gameState = GameState.Push

    def hit(self) -> GameState:
        if self.isGameOver():
            return self.gameState

        self._drawCard(self.playersCards)

        newScore: int = self.playersCards.getScore()

        if newScore > 21:
            self.gameState = GameState.Lose
        elif newScore == 21:
            self.gameState = GameState.Win

        return self.gameState

    def stand(self) -> GameState:
        if not self.isGameOver():
            self.performDealersTurn()

        return self.gameState

    def performDealersTurn(self) -> Self:
        """Performs the dealer's moves and finishes the game."""
        playersScore: int = self.playersCards.getScore()
        dealersScore: int = self.dealersCards.getScore()

        # If the player bust or the dealer got blackjack
        if playersScore > 21 or dealersScore == 21:
            self.gameState = GameState.Lose
            return self

        while (dealersScore := self.dealersCards.getScore()) <= 16:
            self._drawCard(self.dealersCards)

        dealersScore = self.dealersCards.getScore()

        if playersScore > dealersScore or dealersScore > 21:
            self.gameState = GameState.Win
        else:
            if playersScore == dealersScore:
                self.gameState = GameState.Push
            else:
                self.gameState = GameState.Lose

        return self

    def _drawCard(self, hand: CardHand) -> Card | None:
        """Draws a card and places it into the given hand."""
        newCard: Card | None = self.deck.draw()

        if newCard is not None:
            hand.add(newCard)

        return newCard

    def isGameOver(self) -> bool:
        """Returns whether the game is already over."""
        return self.gameState != GameState.Playing
