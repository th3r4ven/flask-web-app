from flask import Flask, render_template, request, redirect, session, flash, url_for
from subprocess import call as command
command(['clear'])

flask_app = Flask(__name__)
flask_app.secret_key = "admin"


class Game:
    def __init__(self, title, category, console):
        self.__title = title
        self.__category = category
        self.__console = console

    @property
    def title(self):
        return self.__title

    @property
    def category(self):
        return self.__category

    @property
    def console(self):
        return self.__console


class User(object):

    def __init__(self, id, name, passwd):
        self.__id = id
        self.__name = name
        self.__passwd = passwd

    @property
    def name(self):
        return self.__name

    @property
    def id(self):
        return self.__id

    def do_login(self, name, passwd):
        return self.__name == name and self.__passwd == passwd


user1 = User(1, 'Raven', '123456')
user2 = User(2, 'Matheus', 'Python')
user3 = User(3, 'Jamela1', 'Javascripto')
users = {
    user1.name: user1,
    user2.name: user2,
    user3.name: user3
}

game01 = Game('Rocket League', 'E-Sports', 'PC, PlayStation and X-Box')
game02 = Game('CS:GO', 'FPS', 'PC')
game03 = Game('PUBG', 'Battle-Royale', 'PC')
games_list = [game01, game02, game03]


@flask_app.route('/')
def game_list():
    return render_template('list.html', title="Games", games=games_list)


@flask_app.route('/new-game')
def newGame():
    if verify_logged_user():
        return render_template('form-game.html', title="New Game")
    else:
        flash('You need to login before accessing this page')
        return redirect(url_for('login', next='newGame'))


@flask_app.route('/createGame', methods=['POST'])
def createGame():
    name = request.form['name']  # get information from form
    category = request.form['category']
    console = request.form['console']

    games_list.append(Game(name, category, console))

    return redirect(url_for('game_list'))


@flask_app.route('/login')
def login():
    return render_template('login.html', next=request.args.get('next'))


@flask_app.route('/authenticator', methods=['POST'])
def auth():
    username = request.form['username']
    passwd = request.form['password']

    if username in users and users[username].do_login(username, passwd):
        session['logged_user'] = username
        session['logged'] = True
        flash('Successfully logged')
        return redirect(url_for(request.form["next"]))
    else:
        flash('Incorrect credentials')
        return redirect(url_for('login'))


@flask_app.route('/logout')
def logout():
    session['logged_user'] = None
    session['logged'] = False
    flash('Successfully logged out')
    return redirect(url_for('game_list'))


def verify_logged_user():
    return session['logged'] == True


if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', debug=True)
