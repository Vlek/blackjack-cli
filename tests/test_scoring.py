import pytest

from blackjack_cli.blackjack import Blackjack, Card


@pytest.mark.parametrize(
    "cards,score",
    [
        (
            [
                Card(Card.Suit.SPADES, Card.Value.ACE),
                Card(Card.Suit.SPADES, Card.Value.JACK),
            ],
            21,
        ),
        (
            [
                Card(Card.Suit.CLUBS, Card.Value.TWO),
                Card(Card.Suit.SPADES, Card.Value.JACK),
            ],
            12,
        ),
        (
            [
                Card(Card.Suit.DIAMONDS, Card.Value.SIX),
                Card(Card.Suit.HEARTS, Card.Value.QUEEN),
            ],
            16,
        ),
        (
            [
                Card(Card.Suit.SPADES, Card.Value.QUEEN),
                Card(Card.Suit.SPADES, Card.Value.KING),
            ],
            20,
        ),
        (
            [
                Card(Card.Suit.SPADES, Card.Value.ACE),
                Card(Card.Suit.SPADES, Card.Value.ACE),
                Card(Card.Suit.SPADES, Card.Value.ACE),
                Card(Card.Suit.SPADES, Card.Value.ACE),
            ],
            14,
        ),
    ],
)
def test_score(cards: list[Card], score: int) -> None:
    game = Blackjack()

    game.playersCards.cards = cards

    assert game.playersCards.getScore() == score
