import sqlite3


def create_table(path="databases/team_records.db"):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS team_records
                    (team_number text, wins integer, losses integer)"""
    )
    # insert 6 teams with 0 wins and 0 losses
    cursor.execute("""INSERT INTO team_records VALUES (1, 0, 0)""")
    cursor.execute("""INSERT INTO team_records VALUES (2, 0, 0)""")
    cursor.execute("""INSERT INTO team_records VALUES (3, 0, 0)""")
    cursor.execute("""INSERT INTO team_records VALUES (4, 0, 0)""")
    cursor.execute("""INSERT INTO team_records VALUES (5, 0, 0)""")
    cursor.execute("""INSERT INTO team_records VALUES (6, 0, 0)""")

    conn.commit()
    conn.close()


def update_records(team_number, win_loss):
    conn = sqlite3.connect("databases/team_records.db")
    cursor = conn.cursor()
    cursor.execute(
        """SELECT * FROM team_records WHERE team_number = ?""", (team_number,)
    )
    row = cursor.fetchone()
    if win_loss == "win":
        cursor.execute(
            """UPDATE team_records SET wins = ? WHERE team_number = ?""",
            (row[1] + 1, team_number),
        )
    elif win_loss == "loss":
        cursor.execute(
            """UPDATE team_records SET losses = ? WHERE team_number = ?""",
            (row[2] + 1, team_number),
        )

    conn.commit()
    conn.close()


def clear_table():
    conn = sqlite3.connect("databases/team_records.db")
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM team_records""")
    conn.commit()
    conn.close()


def get_records():
    conn = sqlite3.connect("databases/team_records.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM team_records""")
    rows = cursor.fetchall()
    conn.close()
    return rows
