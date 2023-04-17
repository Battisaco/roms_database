from flask import Flask, jsonify
import psycopg2


app = Flask(__name__)

conn = psycopg2.connect(
    host='roms-db.cwj1afgxeloy.sa-east-1.rds.amazonaws.com',
    port=5432,
    dbname='postgres',
    user='postgres',
    password='battisaco'
)

@app.route('/games')
def get_games():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM Game;")
        games = cur.fetchall()
    return jsonify(games)

@app.route('/roms')
def get_roms():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM Rom;")
        roms = cur.fetchall()
    return jsonify(roms)

@app.route('/consoles')
def get_consoles():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM Console;")
        consoles = cur.fetchall()
    return jsonify(consoles)

if __name__ == '__main__':
    app.run()