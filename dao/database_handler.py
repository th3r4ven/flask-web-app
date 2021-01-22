from models.game import Game
from models.user import User

DELETE_GAME = 'delete from game where id = %s'
GAME_BY_ID = 'SELECT id, name, category, console from game where id = %s'
USER_BY_USERNAME = 'SELECT id, name, passwd from user where name = %s'
UPDATE_GAME = 'UPDATE game SET name=%s, category=%s, console=%s where id = %s'
SEARCH_GAME = 'SELECT id, name, category, console from game'
CREATE_GAME = 'INSERT into game (name, category, console) values (%s, %s, %s)'


class GameDao:
    def __init__(self, db):
        self.__db = db

    def save(self, game):
        cursor = self.__db.connection.cursor()

        if game.id:
            cursor.execute(UPDATE_GAME, (game.title, game.category, game.console, game.id))
        else:
            cursor.execute(CREATE_GAME, (game.title, game.category, game.console))
            game.id = cursor.lastrowid
        self.__db.connection.commit()
        return game

    def list_games(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SEARCH_GAME)
        games = translate_game(cursor.fetchall())
        return games

    def search_by_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(GAME_BY_ID, (id,))
        tupla = cursor.fetchone()
        return Game(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def delete(self, id):
        self.__db.connection.cursor().execute(DELETE_GAME, (id, ))
        self.__db.connection.commit()


class UserDao:
    def __init__(self, db):
        self.__db = db

    def search_by_name(self, username):
        cursor = self.__db.connection.cursor()
        cursor.execute(USER_BY_USERNAME, (username,))
        dados = cursor.fetchone()
        usuario = translate_user(dados) if dados else None
        return usuario


def translate_game(games):
    def create_game_tuple(tupla):
        return Game(tupla[1], tupla[2], tupla[3], id=tupla[0])
    return list(map(create_game_tuple, games))


def translate_user(tupla):
    return User(tupla[0], tupla[1], tupla[2])
