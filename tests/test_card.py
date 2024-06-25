import pytest
from deck import Card


@pytest.mark.parametrize(
    "card,expected",
    [
        (Card(Card.Suit.CLUBS, Card.Value.FIVE), "5"),
        (Card(Card.Suit.SPADES, Card.Value.ACE), "as"),
    ],
)
def test_tostr(card: Card, expected: str) -> none:
    """Testing the tostring method overload."""
    assert str(card) == expected
