import bcrypt
from orator.orm import has_many
from orator.pagination import LengthAwarePaginator

from api.app import db


class User(db.Model):
    """ A user player. """

    def __repr__(self):
        return "<User %r>" % self.username

    __fillable__ = ["username", "bank"]
    __guarded__ = ["password"]
    __hidden__ = ["password"]

    username: str
    bank: int
    password: bytes

    @has_many
    def hands(self):
        from api.store.hand import Hand
        return Hand

    def set_password(self, plaintext_pw: str) -> None:
        """ Bcrypts & stores the password. """
        self.password = bcrypt.hashpw(plaintext_pw.encode(), bcrypt.gensalt())

    def is_correct_password(self, password_guess: str) -> bool:
        """ Checks if the guess matches the hashed value. """
        return bcrypt.checkpw(password_guess.encode(), self.password)


def create_user(username: str, password: str, bank: int = None) -> User:
    """ Creates & returns a new User. """
    new_user = User(username=username, password=password, bank=bank)
    new_user.set_password(password)
    new_user.save()

    return new_user


def get_user(user_id: int) -> User:
    """ Returns the User by ID. """
    return User.find_or_fail(user_id)


# TODO: Add sorting
def list_users(page: int = 1, page_size: int = 20) -> LengthAwarePaginator:
    """ Paginated list of all Users. """
    return User.paginate(page, page_size)
