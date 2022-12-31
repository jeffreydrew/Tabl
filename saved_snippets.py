def update_records(round: str, path: str = PATH_DB)-> None:


    '''
    calls functions to:
    - update win-loss
    - update pd
    - update all round opponents
    this will os.walk and go through all ballots available 
    '''
    
    updates = get_round_updates(round)
    # connect to database
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    # go through each update
    for update in updates:
        # parse info
        winning_team = update[0]
        losing_team = update[1]
        pd = int(update[2])

        #set oppenent for winning team to losing team
        cursor.execute(
            """SELECT * FROM team_records WHERE team_number = ?""", (winning_team,)
        )
        row = cursor.fetchone()
        #set the value at int(round) + 6 to losing_team
        cursor.execute(
            """UPDATE team_records SET round_number = ? WHERE team_number = ?""",
            (winning_team, losing_team),
        )
        
        #set oppenent for losing team to winning team
        cursor.execute(
            """SELECT * FROM team_records WHERE team_number = ?""", (losing_team,)
        )
        row = cursor.fetchone()

        cursor.execute(
            """UPDATE team_records SET round_number = ? WHERE team_number = ?""",
            (losing_team, winning_team),
        )

        # update records
        if pd == 0:
            #add 0.5 to winning teams record at row[2]
            cursor.execute(
                """SELECT * FROM team_records WHERE team_number = ?""", (winning_team,)
            )
            row = cursor.fetchone()
            cursor.execute(
                """UPDATE team_records SET Wins = ? WHERE team_number = ?""",
                (row[2] + 0.5, winning_team),
            )
            # add 0.5 to winning teams record at row[3]
            cursor.execute(
                """SELECT * FROM team_records WHERE team_number = ?""", (winning_team,)
            )
            row = cursor.fetchone()
            cursor.execute(
                """UPDATE team_records SET Losses = ? WHERE team_number = ?""",
                (row[3] + 0.5, winning_team),
            )

            
            # add 0.5 to losing teams record at row[2]
            cursor.execute(
                """SELECT * FROM team_records WHERE team_number = ?""", (losing_team,)
            )
            row = cursor.fetchone()
            cursor.execute(
                """UPDATE team_records SET Wins = ? WHERE team_number = ?""",
                (row[2] + 0.5, losing_team),
            )
            # add 0.5 to losing teams record at row[3]
            cursor.execute(
                """SELECT * FROM team_records WHERE team_number = ?""", (losing_team,)
            )
            row = cursor.fetchone()
            cursor.execute(
                """UPDATE team_records SET Losses = ? WHERE team_number = ?""",
                (row[3] + 0.5, losing_team),
            )

        else:
            # winning team update record then pd
            cursor.execute(
                """SELECT * FROM team_records WHERE team_number = ?""", (winning_team,)
            )
            row = cursor.fetchone()
            cursor.execute(
                """UPDATE team_records SET wins = ? WHERE team_number = ?""",
                (row[2] + 1, winning_team),
            )

            cursor.execute(
                """UPDATE team_records SET PD = ? WHERE team_number = ?""",
                (row[6] + pd, winning_team),
            )

            # losing team update record then pd
            cursor.execute(
                """SELECT * FROM team_records WHERE team_number = ?""", (losing_team,)
            )
            row = cursor.fetchone()
            cursor.execute(
                """UPDATE team_records SET losses = ? WHERE team_number = ?""",
                (row[3] + 1, losing_team),
            )
            cursor.execute(
                """UPDATE team_records SET PD = ? WHERE team_number = ?""",
                (row[6] - pd, losing_team),
            )
    conn.commit()
    conn.close()

