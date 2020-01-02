import json
from typing import Union, Dict, List
import random

from orator.orm import has_many, has_one, accessor

from api.app import db
from api import store


class Game(db.Model):
    """ A game of blackjack including a dealer. """

    def __repr__(self):
        return "<Game %r>" % self.id

    __guarded__ = ["deck"]
    __hidden__ = ["deck"]

    deck: List[Dict[str, Union[str, int]]]

    @accessor
    def deck(self) -> List[Dict[str, Union[str, int]]]:
        return json.loads(self.get_raw_attribute("deck"))

    @deck.mutator
    def set_deck(self, deck: List[Dict[str, Union[str, int]]]) -> None:
        self.set_raw_attribute("deck", json.dumps(deck))

    @has_one
    def dealer_hand(self):
        # from api.store.hand import Hand
        return store.hand.Hand

    @has_many
    def player_hands(self):
        from api.store.hand import Hand
        return Hand
        # return store.hand.Hand


def get_game(game_id: int) -> Game:
    """ Returns the Game by ID. """
    return Game.find_or_fail(game_id)


# def create_game(users: list[User]) -> Game:
def create_game(players: List[Dict[str, str]] = None) -> Game:
    """ Creates & returns a new User. """
    new_game = Game()

    # Create a deck & shuffle it
    new_game.deck = [{"suit": suit, "rank": rank} for suit in ["♣", "♦", "♥", "♠"] for rank in range(1, 14)]
    for i, _ in enumerate(new_game.deck):
        x = random.randint(0, i)
        new_game.deck[i], new_game.deck[x] = new_game.deck[x], new_game.deck[i]

    new_game.save()

    for player in players:
        new_game.player_hands.append(store.hand.create_hand(
            player.get("user_id"),
            new_game.id,
            player.get("bet"),
            [new_game.deck.pop() for _ in range(2)]
        ))

    # Create a dealer hand.
    new_game.dealer_hand = store.hand.create_hand(
        user_id=None,
        game_id=new_game.id,
        bet=None,
        cards=[new_game.deck.pop() for _ in range(2)],
        is_dealer_hand=True
    )

    new_game.save()

    return new_game

def draw(game_id: int, n: int = 1) -> List[Dict[str, Union[str, int]]]:
    """ Removes & returns n cards from the game's deck. """
    with db.transaction():
        game = get_game(game_id)
        cards_to_return = [game.deck.pop() for _ in range(n)]
        game.save()
    return cards_to_return
