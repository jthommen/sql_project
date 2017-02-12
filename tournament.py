#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""

    # Database connection & delete
    con = connect()
    cur = con.cursor()
    query = "delete from matches"
    cur.execute(query)
    con.commit()
    con.close()


def deletePlayers():
    """Remove all the player records from the database."""

    # Database connection & delete
    con = connect()
    cur = con.cursor()
    query = "delete from players"
    cur.execute(query)
    con.commit()
    con.close()


def countPlayers():
    """Returns the number of players currently registered."""

    # Database connection & query
    con = connect()
    cur = con.cursor()
    query = "select count(*) from players"
    cur.execute(query)

    # Fetches one row from result and saves first element
    # of result tuple in count variable
    count = cur.fetchone()[0]
    con.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    # Import sanitization with bleach
    name = bleach.clean(name)

    # Database connection & insert
    con = connect()
    cur = con.cursor()

    # Safe/escaped insert with tuples
    cur.execute("insert into players(name) values(%s)", (name,))
    con.commit()
    con.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    # Database connection & query
    db = connect()
    c = db.cursor()
    query = "select * from standings;"
    c.execute(query)
    standings = c.fetchall()
    db.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # Database connection & insert
    con = connect()
    cur = con.cursor()

    # Safe/escaped insert with tuples
    cur.execute(
        "insert into matches (winner, loser) values(%s, %s)",
        (winner, loser,)
    )
    con.commit()
    con.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    # Database connection & query
    con = connect()
    cur = con.cursor()
    query = "select * from standings"
    cur.execute(query)
    players = cur.fetchall()
    con.close()

    # Number of players to pair
    count = len(players)

    # Empty list to append Swiss pairs
    swiss_pairings = []

    # Iterating over players to pair them
    for rank in range(0, count-1, 2):
        # pair = (id1, name1, id2, name2)
        pair = (
            players[rank][0],
            players[rank][1],
            players[rank+1][0],
            players[rank+1][1]
        )
        swiss_pairings.append(pair)
    return swiss_pairings


# # Testing Functions
# Function to insert data into db for testing purposes
def register():
    registerPlayer("James Johnson")
    registerPlayer("Abraham Lincoln")
    registerPlayer("Drude Abilow")
    registerPlayer("Jared Reed")


# Function to insert data into db for testing purposes
def report():
    reportMatch(1, 3)
    reportMatch(3, 4)
    reportMatch(4, 1)
    reportMatch(4, 2)


# Some custom test function calls to get feedback on progress
def test():
    deleteMatches()
    print "Delete players..."
    deletePlayers()
    print "----------"

    print "Count existing players after delete: " + str(countPlayers())
    print "----------"

    print "Register four players...."
    register()
    print "----------"

    print "Count existing players after registering: " + str(countPlayers())
    print "----------"

    print "These are the player standings: " + str(playerStandings())
    print "----------"

    print "These are the Swiss pairings: " + str(swissPairings())
    print "----------"

# register()
# report()
# test()
