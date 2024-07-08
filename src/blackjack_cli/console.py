"""
Entryway into the project for console-based usage.
"""

import rich_click as click
import pickle
from pathlib import Path
from random import choice

from blackjack_cli.blackjack import Blackjack, GameState
from blackjack_cli.config import Config
from blackjack_cli.stats import Stats

from deck import CardHand


config = Config()

STATS_FILE_PATH: Path = config.config_folder_path / "stats.json"
STATE_FILE_PATH: Path = config.config_folder_path / "gamestate.pickle"

playerStats = Stats(STATS_FILE_PATH)

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
    """Starts new game or asks dealer for another card."""
    gameState: GameState = game_instance.gameState

    if not isNewGame:
        gameState = game_instance.hit()

    if gameState != GameState.Playing:
        __print_end_of_game(game_instance)
        playerStats.save(STATS_FILE_PATH, game_instance.gameState)
        STATE_FILE_PATH.unlink(missing_ok=True)
    else:
        click.echo(
            f"{__get_hands_string(game_instance.playersCards, game_instance.dealersCards, True)} Hit or Stand?"
        )
        __save_state(STATE_FILE_PATH, game_instance)


@bj.command()
def stand() -> None:
    """Performs the dealer's turn and ends the game."""
    if isNewGame:
        click.echo("Type 'hit' to start a new game.")
        return

    game_instance.stand()

    __print_end_of_game(game_instance)
    playerStats.save(STATS_FILE_PATH, game_instance.gameState)

    STATE_FILE_PATH.unlink(missing_ok=True)


@bj.command()
def stats() -> None:
    """Lists the player's game statistics."""
    click.echo("Player stats:")

    click.echo(playerStats.data)


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
        case GameState.Push:
            result_text = "Push"

    previousGameState: GameState = playerStats.data._last_outcome
    currentStreak: int = playerStats.data._current_streak

    sass: str = __get_sass(
        game.gameState,
        previousGameState,
        currentStreak,
    )

    click.echo(
        f"{__get_hands_string(game.playersCards, game.dealersCards, False)} {result_text}! {sass}"
    )


def __get_hands_string(
    playerHand: CardHand, dealerHand: CardHand, hideDealersSecondCard: bool
) -> str:
    """Returns the formatted string for player and dealer."""
    if hideDealersSecondCard:
        dealersCards: str = " ".join([str(dealerHand.cards[0]), "?"])
        dealersScore: str = "?"
    else:
        dealersCards = str(dealerHand)
        dealersScore = __get_score_string(dealerHand)

    return f"Player: {playerHand} ({playerHand.getScore()}). House: {dealersCards} ({dealersScore})."


def __get_score_string(hand: CardHand) -> str:
    """Returns either Blackjack or the score of a hand."""
    handScore = hand.getScore()

    if handScore == 21 and len(hand.cards) == 2:
        scoreOutput: str = "Blackjack"
    else:
        scoreOutput = str(handScore)

    return scoreOutput


def __get_sass(
    gameState: GameState, lastGameOutcome: GameState, currentStreak: int
) -> str:
    """Given game state, returns some flavor text to add to the end of game."""
    responseBank: list[str]

    loseResponseBank: list[str] = [
        "Play again?",
        "The house always wins!",
        "Maybe next time.",
        "💩",
        "Tough luck.",
        "Womp womp",
        "You can turn it around next time.",
    ]

    winResponseBank: list[str] = [
        "Another win?",
        "Next time you'll lose! >:C",
        "I will shuffle better next time. :..<.",
        "🎆",
        "🎉",
        "🔥",
    ]

    pushResponseBank: list[str] = [
        "Draw!",
        "Alright, we will call it a draw.",
        "Maybe you'll win next time?",
        "Give it another shot.",
        "Maybe next time.",
    ]

    # This is before the streak is incremented in the stats, so what is saved
    # is our previous streak. Need to increment to include current win/lose
    currentStreak += 1

    # If a streak continues
    if gameState == lastGameOutcome:
        # Winning streak continues
        if gameState in [GameState.Win, GameState.Blackjack]:
            responseBank = [
                f"Continuing the winning streak to {currentStreak}!",
                f"{currentStreak} times a winner!",
                f"Will you lose after winning {currentStreak} times?",
            ] + winResponseBank
        elif gameState == GameState.Push:
            responseBank = [
                f"{currentStreak} pushes? That's rare.",
            ] + pushResponseBank
        # Losing streak continues.
        # Here's where the real sass is!
        else:
            responseBank = [
                f"You increase your losing streak to {currentStreak}!",
                f"{currentStreak} losses. Maybe you'll win next time?",
            ] + loseResponseBank

    # A losing streak was broken
    elif gameState in [GameState.Win, GameState.Blackjack]:
        responseBank = [
            "You broke your losing streak!",
            f"Losing streak of {currentStreak} broken!",
            "Now to turn this into a winning streak!",
        ] + winResponseBank

    elif gameState == GameState.Push:
        responseBank = pushResponseBank

    # A winning streak was broken
    else:
        responseBank = [
            "Wining streak broken!",
            "Will this lead to a losing streak?",
        ] + loseResponseBank

    return choice(responseBank)
