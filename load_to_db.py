import psycopg2
import json

conn = psycopg2.connect(
    host="roms-db.cwj1afgxeloy.sa-east-1.rds.amazonaws.com",
    port=5432,
    dbname="postgres",
    user="postgres",
    password="battisaco",
)

if conn.status == psycopg2.extensions.STATUS_READY:
    print("Connection is active.")
else:
    print("Connection is not active.")

cur = conn.cursor()

with open("Data/console.json") as f:
    console_data = json.load(f)

with open("Data/games.json") as f:
    game_data = json.load(f)

with open("Data/roms.json") as f:
    roms_data = json.load(f)

for console in console_data:
    cur.execute(
        """
        INSERT INTO Console (id, name, image, url) 
        VALUES (%s, %s, %s, %s);
        """,
        (console["id"], console["name"], console["image"], json.dumps(console["url"])),
    )

conn.commit()
print("Console commit, ok")


for game in game_data:
    insert_query = """
    INSERT INTO Game (id, console_id, name, image, console, url) 
    VALUES ('{}', '{}', '{}', '{}', '{}', '{}')
    """.format(
        game["id"],
        game["console_id"],
        game["name"].replace("'", "''"),
        game["image"],
        game["console"],
        json.dumps(game["url"]),
    )
    cur.execute(insert_query)

conn.commit()
print("Game commit, ok")

for rom in roms_data:
    try:
        rom_name = rom["name"].replace("'", "''")
    except AttributeError:
        rom_name = ""

    insert_query = """
    INSERT INTO Rom (id, game_id, name, size, type, link, provider, version) 
    VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')
    """.format(
        rom["id"],
        rom["game_id"],
        rom_name,
        rom["size"],
        rom["type"],
        "Del",
        rom["provider"],
        rom["version"],
    )
    cur.execute(insert_query)

conn.commit()
print("Roms commit, ok")


conn.close()
