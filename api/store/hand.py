import json
from typing import Union, Dict, List

from orator.orm import belongs_to, accessor

from api.app import db


class Hand(db.Model):
    """ A blackjack hand belonging to a dealer or player. """

    __fillable__ = ["user_id", "game_id", "bet", "cards", "is_dealer_hand"]

    @accessor
    def cards(self) -> List[Dict[str, Union[str, int]]]:
        return json.loads(self.get_raw_attribute("cards"))

    @cards.mutator
    def set_cards(self, cards: List[Dict[str, Union[str, int]]]) -> None:
        self.set_raw_attribute("cards", json.dumps(cards))

    def __repr__(self):
        return "<Hand %r>" % self.id

    @belongs_to
    def user(self):
        from api.store.game import User
        return User

    @belongs_to
    def game(self):
        from api.store.game import Game
        return Game


def create_hand(
        user_id: str,
        game_id: str,
        bet: int = None,
        cards: List[Dict[str, Union[str, int]]] = None,
        is_dealer_hand: bool = False
    ) -> Hand:
    """ Creates & returns a new Hand. """
    new_hand = Hand(
        user_id=user_id,
        game_id=game_id,
        bet=bet,
        cards=cards,
        is_dealer_hand=is_dealer_hand
    )
    new_hand.save()

    return new_hand