from flask_mysqldb import MySQL


def do_connect(app):
    app.config['MYSQL_HOST'] = "0.0.0.0"
    app.config['MYSQL_USER'] = "root"
    app.config['MYSQL_PASSWORD'] = ""
    app.config['MYSQL_DB'] = "Raven_games"
    app.config['MYSQL_PORT'] = 3306

    return MySQL(app)
