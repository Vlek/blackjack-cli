"""
This is the base logic file for all of the Blackjack game code.

This is going to house things like:
    - What is a deck?
    - What is a player/dealer?
    - Turn order
"""

from enum import Enum
from typing_extensions import Self

from deck import Deck, Card
from cardhand import CardHand


def blackjackScoringStrategy(cards: list[Card]) -> int:
    """Returns the score of a given list of cards."""
    return 0


class GameState(Enum):
    Playing = 0
    Win = 1
    Lose = 2
    Blackjack = 3


class Blackjack:
    def __init__(self) -> None:
        self.gameState: GameState = GameState.Playing

        # Standard blackjack is played with 4 decks
        # instead of just one.
        self.deck: Deck = Deck() * 4
        self.deck.shuffle()

        self.playersCards: CardHand = CardHand([self.deck.draw(), self.deck.draw()])
        self.dealersCards: CardHand = CardHand([self.deck.draw(), self.deck.draw()])

        # If blackjack:
        if self.playersCards.getScore() == 21:
            self.gameState = GameState.Blackjack

    def hit(self) -> GameState:
        # TODO, maybe this should be a decorator so that these can only be done
        #    if game is still not over?
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

        if playersScore > 21:
            return self

        # TODO: There's something about the dealer having to try to 17 or something?
        while playersScore > (dealersScore := self.dealersCards.getScore()):
            self._drawCard(self.dealersCards)

        endingDealersScore = self.dealersCards.getScore()

        if endingDealersScore < 22 and endingDealersScore > playersScore:
            self.gameState = GameState.Lose
        else:
            self.gameState = GameState.Win

        return self

    def _drawCard(self, playerHand: CardHand) -> Card | None:
        """Draws a card and places it into the given hand."""
        newCard: Card | None = self.deck.draw()
        
        if newCard is not None:
            playerHand.add(newCard)

        return newCard

    def isGameOver(self) -> bool:
        """Returns whether the game is already over."""
        return self.gameState != GameState.Playing


    # TODO: Maybe add a todict so that I can serialize and deserialize?
