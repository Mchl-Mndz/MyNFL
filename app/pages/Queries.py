import streamlit as st
from db import get_connection

st.title("📋 Prewritten Query Viewer")

# Connect to MySQL (prompts for password and database)
conn = get_connection()

if not conn:
    st.warning("Please enter your MySQL password and database name to connect.")
    st.stop()

queries = {
    "UCF Alumni": {
        "sql": """
            SELECT DISTINCT Player
            FROM players p, college c
            WHERE p.ID = c.ID AND `College/Univ` = "Central Florida"
        """, 
        "description": "View all players who attended UCF"
    },
    "SB Gainers": {
        "sql": """
            WITH sb_games AS (
            SELECT gameID
            FROM football.games
            WHERE DAYOFWEEK(date) = 1
                AND MONTH(date) = 2
                AND DAY(date) BETWEEN 8 AND 14
            ),
            sb_player_yards AS (
            SELECT 
                pRU.ID AS playerID,
                ROUND(pRU.`RushYards/Game` + pRC.RecYds) AS total_Yds
            FROM sb_games sb
            JOIN p_rushing pRU ON pRU.gameID = sb.gameID
            JOIN p_recieving pRC ON pRC.gameID = sb.gameID AND pRU.ID = pRC.ID
            )
            SELECT 
            sp.playerID,
            pl.Player AS playerName,
            sp.total_Yds
            FROM sb_player_yards sp
            JOIN players pl ON sp.playerID = pl.ID
            ORDER BY sp.total_Yds DESC
            LIMIT 1;
        """,        
        "description": "What player totalled the most scrimmage yards in the Super Bowl (rushing+receiving)?"
    },
    "Reciever by Comittee": {
        "sql": """
            SELECT TeamName, COUNT(DISTINCT ID) AS num_receivers
            FROM teams, p_recieving
            WHERE teams.TeamInitial = p_recieving.Team and Receptions > 0
            GROUP BY TeamName
            ORDER BY num_receivers DESC
            LIMIT 1;
        """,
        "description": "Which team had the most distinct players catch a pass?"
    },
    "Kieran the Kicker?": {
        "sql": """
            SELECT DISTINCT Player, KickLong
            FROM players, p_kicking
            WHERE p_kicking.ID = players.ID and BirthDate > '2000-08-17' and KickLong >= 55;
        """,
        "description": "Select all players who are younger than Kieran and have a longest field goal longer than 55 yards."
    },
    "Stadium Scoreboard Sums": {
        "sql": """
            SELECT stadium, SUM(awayScore + homeScore) AS total_points
            FROM games
            GROUP BY stadium
            ORDER BY total_points DESC
        """,
        "description": "In which stadium were the most points scored during this season?"
    },
    "Tackle University": {
        "sql": """
            SELECT `College/Univ`, TotalTackles
            FROM (
                SELECT c.`College/Univ`, SUM(d.Comb) AS TotalTackles
                FROM players p, p_defense d, college c
                WHERE p.ID = d.ID AND p.ID = c.ID
                GROUP BY c.`College/Univ`
            ) AS CollegeTackles
            WHERE TotalTackles = (
                SELECT MAX(SumComb)
                FROM (
                    SELECT SUM(d.Comb) AS SumComb
                    FROM players p, p_defense d, college c
                    WHERE p.ID = d.ID AND p.ID = c.ID
                    GROUP BY c.`College/Univ`
                ) AS MaxTackles
            );
        """,
        "description": "Which college produced the most tackles this year?"
    },
    "Absolute Mismatch": {
        "sql": """
            WITH TeamPoints AS (
            SELECT t.TeamInitial,
                SUM(
                CASE 
                    WHEN g.homeTeam = t.TeamInitial THEN g.homeScore
                    WHEN g.awayTeam = t.TeamInitial THEN g.awayScore
                    ELSE 0
                END
                ) AS PF,
                SUM(
                CASE 
                    WHEN g.homeTeam = t.TeamInitial THEN g.awayScore
                    WHEN g.awayTeam = t.TeamInitial THEN g.homeScore
                    ELSE 0
                END
                ) AS PS
            FROM teams t, games g
            WHERE g.homeTeam = t.TeamInitial OR g.awayTeam = t.TeamInitial
            GROUP BY t.TeamInitial
            ),
            PD AS (
            SELECT TeamInitial, (PF - PS) AS PointDifferential
            FROM TeamPoints
            )
            SELECT *
            FROM PD
            ORDER BY PointDifferential ASC
            LIMIT 1;
        """,
        "description": "Which team had the worst point differential ( = Points scored - Points against)?"
    },
    "Week Two Warrior": {
        "sql": """
            WITH week2 AS (
            SELECT gameID
            FROM football.games
            WHERE DAYOFWEEK(date) = 2  -- Monday
                AND MONTH(date) = 9
                AND DAY(date) BETWEEN 8 AND 14
            ),
            week2_passing AS (
            SELECT pPA.ID AS playerID, pPA.gameID, pPA.PassYds
            FROM p_passing pPA
            JOIN week2 W2 ON pPA.gameID = W2.gameID
            ),
            mostPassingYards AS (
            SELECT *
            FROM week2_passing
            ORDER BY PassYds DESC
            LIMIT 1
            )
            SELECT 
            m.playerID,
            pl.Player AS playerName,
            m.PassYds
            FROM mostPassingYards m
            JOIN players pl ON m.playerID = pl.ID
        """,
        "description": "What player in week 2 had the most passing yards?"
    }
}

# Let the user pick a query
query_name = st.selectbox("Choose a query:", list(queries.keys()))

if query_name:
    q = queries[query_name]
    st.subheader(query_name)
    st.write(q["description"])
    st.code(q["sql"], language="sql")

    try:
        cursor = conn.cursor()
        cursor.execute(q["sql"])
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        if rows:
            st.dataframe([dict(zip(columns, row)) for row in rows])
        else:
            st.info("No results found.")
    except Exception as e:
        st.error(f"Error running query: {e}")
