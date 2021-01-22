from dao.connect import do_connect
from flask import Flask
app = Flask(__name__)

conn = do_connect(app)

create_table = '''SET NAMES utf8;
    CREATE TABLE `game` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(50) COLLATE utf8_bin NOT NULL,
      `category` varchar(40) COLLATE utf8_bin NOT NULL,
      `console` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE `user` (
      `id` int NOT NULL AUTO_INCREMENT,
      `name` varchar(20) COLLATE utf8_bin NOT NULL UNIQUE,
      `passwd` varchar(8) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''

conn.cursor().execute(create_table)

# inserting user
cursor = conn.cursor()
cursor.executemany(
      'INSERT INTO user (name, passwd) VALUES (%s, %s)',
      [
            ('Raven', '123')
      ])

# inserting games
cursor.executemany(
      'INSERT INTO game (name, category, console) VALUES (%s, %s, %s)',
      [
            ('Rocket League', 'E-Sports', 'PC, PS4, Xbox'),
            ('CS:GO', 'FPS', 'PC'),
            ('PUBG', 'Battle Royale', 'PC')
      ])

conn.commit()
cursor.close()
