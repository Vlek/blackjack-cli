import pytest

from blackjack_cli.blackjack import Blackjack, Card, GameState


@pytest.mark.parametrize(
    "playercards,dealercards,gamestate",
    [
        (
            [
                Card(Card.Suit.SPADES, Card.Value.ACE),
                Card(Card.Suit.SPADES, Card.Value.JACK),
            ],
            [
                Card(Card.Suit.SPADES, Card.Value.ACE),
                Card(Card.Suit.SPADES, Card.Value.JACK),
            ],
            GameState.Push,
        ),
        (
            [
                Card(Card.Suit.SPADES, Card.Value.TWO),
                Card(Card.Suit.SPADES, Card.Value.THREE),
            ],
            [
                Card(Card.Suit.SPADES, Card.Value.TWO),
                Card(Card.Suit.SPADES, Card.Value.THREE),
            ],
            GameState.Push,
        ),
        (
            [
                Card(Card.Suit.CLUBS, Card.Value.TWO),
                Card(Card.Suit.SPADES, Card.Value.JACK),
            ],
            [
                Card(Card.Suit.DIAMONDS, Card.Value.SIX),
                Card(Card.Suit.HEARTS, Card.Value.QUEEN),
            ],
            GameState.Lose,
        ),
        (
            [
                Card(Card.Suit.CLUBS, Card.Value.TWO),
                Card(Card.Suit.SPADES, Card.Value.JACK),
                Card(Card.Suit.SPADES, Card.Value.ACE),
                Card(Card.Suit.SPADES, Card.Value.QUEEN),
            ],
            [
                Card(Card.Suit.DIAMONDS, Card.Value.SIX),
                Card(Card.Suit.HEARTS, Card.Value.QUEEN),
            ],
            GameState.Lose,
        ),
        (
            [
                Card(Card.Suit.SPADES, Card.Value.QUEEN),
                Card(Card.Suit.SPADES, Card.Value.KING),
            ],
            [
                Card(Card.Suit.DIAMONDS, Card.Value.SIX),
                Card(Card.Suit.HEARTS, Card.Value.QUEEN),
            ],
            GameState.Win,
        ),
        (
            [
                Card(Card.Suit.SPADES, Card.Value.ACE),
                Card(Card.Suit.SPADES, Card.Value.ACE),
                Card(Card.Suit.SPADES, Card.Value.ACE),
                Card(Card.Suit.SPADES, Card.Value.ACE),
            ],
            [
                Card(Card.Suit.SPADES, Card.Value.QUEEN),
                Card(Card.Suit.SPADES, Card.Value.KING),
                Card(Card.Suit.SPADES, Card.Value.KING),
            ],
            GameState.Win,
        ),
    ],
)
def test_score(
    playercards: list[Card], dealercards: list[Card], gamestate: GameState
) -> None:
    game = Blackjack()

    game.playersCards.cards = playercards
    game.dealersCards.cards = dealercards

    game._calcGameState()

    assert game.gameState == gamestate
