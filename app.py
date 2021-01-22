from flask import Flask, render_template, request, redirect, session, flash, url_for
from dao.database_handler import GameDao, UserDao
from dao.connect import do_connect
from models.game import Game
from models.user import User


flask_app = Flask(__name__)
flask_app.secret_key = "admin"

db = do_connect(flask_app)

gamedao = GameDao(db)
userdao = UserDao(db)


@flask_app.route('/')
def game_list():
    return render_template('list.html', title="Games", games=gamedao.list_games())


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

    gamedao.save(Game(name, category, console))

    return redirect(url_for('game_list'))


@flask_app.route('/editGame/<int:id>')
def editGame(id):
    if verify_logged_user():
        game = gamedao.search_by_id(id)
        return render_template('edit-game.html', title="Edit Game", game=game)
    else:
        flash('You need to login before accessing this page')
        return redirect(url_for('login', next='editGame'))


@flask_app.route('/updateGame', methods=['POST'])
def updateGame():
    id = request.form['id']
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']

    gamedao.save(Game(name, category, console, id))

    return redirect(url_for('game_list'))


@flask_app.route('/deleteGame/<int:id>')
def deleteGame(id):
    gamedao.delete(id)
    flash('Game was successfully deleted!')
    return redirect(url_for('game_list'))


@flask_app.route('/login')
def login():
    return render_template('login.html', next=request.args.get('next'))


@flask_app.route('/authenticator', methods=['POST'])
def auth():
    username = request.form['username']
    passwd = request.form['password']
    users = userdao.search_by_name(username)

    if users.do_login(username, passwd):
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
