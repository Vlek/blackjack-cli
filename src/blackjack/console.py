"""
Entryway into the project for console-based usage.
"""

import rich_click as click
import pickle
from pathlib import Path

from blackjack.blackjack import Blackjack, GameState
from blackjack.config import Config

# from blackjack.stats import Stats

from blackjack.cardhand import CardHand


config = Config()
# stats = Stats(config.config_folder_path)

STATE_FILE_PATH: Path = config.config_folder_path / "gamestate.pickle"

isNewGame: bool = not STATE_FILE_PATH.exists()

if isNewGame:
    game_instance = Blackjack()
else:
    with open(STATE_FILE_PATH, "rb") as sf:
        game_instance: Blackjack = pickle.load(sf)


@click.group()
def bj() -> None:
    """Blackjack CLI"""
    ...


@bj.command()
def hit() -> None:
    """Asks dealer for another card."""
    gameState: GameState = GameState.Playing

    if not isNewGame:
        gameState = game_instance.hit()

    if gameState != GameState.Playing:
        __print_end_of_game(game_instance)
        STATE_FILE_PATH.unlink(missing_ok=True)
    else:
        click.echo(f"{__get_hands_string(game_instance, True)} Hit or Stand?")
        __save_state(STATE_FILE_PATH, game_instance)


@bj.command()
def stand() -> None:
    """Performs the dealer's turn and ends the game."""

    game_instance.stand()

    __print_end_of_game(game_instance)

    STATE_FILE_PATH.unlink(missing_ok=True)


@bj.command()
def stats() -> None:
    """Lists the player's game statistics."""
    ...


def __save_state(filepath: Path, gameData: Blackjack) -> None:
    with open(filepath, "wb") as stateFile:
        stateFile.write(pickle.dumps(gameData))


def __print_end_of_game(game: Blackjack) -> None:
    result_text: str = "You lose"

    match game.gameState:
        case GameState.Win:
            result_text = "You win"
        case GameState.Blackjack:
            result_text = "Blackjack"

    click.echo(f"{__get_hands_string(game, False)} {result_text}!")


def __get_hands_string(game: Blackjack, hideDealerSecondCard: bool) -> str:
    """Returns the formatted string for player and dealer."""
    if hideDealerSecondCard:
        dealersCards: str = " ".join([str(game.dealersCards.cards[0]), "?"])
        dealersScore: str = "?"
    else:
        dealersCards = str(game_instance.dealersCards)
        dealersScore = __get_score_string(game.dealersCards)

    return f"Player: {game.playersCards} ({__get_score_string(game.playersCards)}). House: {dealersCards} ({dealersScore})."


def __get_score_string(hand: CardHand) -> str:
    """Returns either Blackjack or the score of a hand."""
    handScore = hand.getScore()

    if handScore == 21 and len(hand.cards) == 2:
        scoreOutput: str = "Blackjack"
    else:
        scoreOutput = str(handScore)

    return scoreOutput
