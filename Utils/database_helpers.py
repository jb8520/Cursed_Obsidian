from mysql.connector import MySQLConnection, connect
from mysql.connector.cursor import MySQLCursor

from typing import Optional, Any, List, Tuple

from . import DatabaseConnectionFail

from Configuration.env_loader import EnvLoader

def _open_database_connection() -> Tuple[Optional[MySQLConnection], Optional[MySQLCursor]]:
    database: Optional[MySQLConnection] = connect(
        host = EnvLoader.DATABASE_HOST,
        user = EnvLoader.DATABASE_USER,
        password = EnvLoader.DATABASE_PASSWORD,
        database = EnvLoader.DATABASE_NAME
    )
    cursor: Optional[MySQLCursor] = database.cursor()

    return database, cursor

def _close_database_connection(database: MySQLConnection, cursor: MySQLCursor):
    cursor.close()
    database.close()



def get_bans_by_case_number(case: int) -> Optional[Any]:
    database, cursor = _open_database_connection()

    if not database:
        raise DatabaseConnectionFail()
    
    cursor.execute(
        'SELECT * FROM banlist WHERE ban_id = %s',
        (case)
    )

    ban_case = cursor.fetchone()

    _close_database_connection(database = database, cursor = cursor)

    return ban_case


def check_if_banned(discord_id: int = None, xbox_gamertag: str = None):
    database, cursor = _open_database_connection()
    banned_cases = {}
    if not database:
        raise DatabaseConnectionFail()
    
    if discord_id:
        cursor.execute(
            f'SELECT * FROM banlist WHERE discord_id = %s',
            (str(discord_id))
        )

        banned_cases['discord'] = cursor.fetchall()

    if xbox_gamertag:
        cursor.execute(
            f'SELECT * FROM banlist WHERE xbox_name = %s',
            (xbox_gamertag)
        )

        banned_cases['discord'] = cursor.fetchall()

    _close_database_connection(database = database, cursor = cursor)

    return banned_cases


def check_friends_by_xbox_name(friends_gamertags: List[str]):
    database, cursor = _open_database_connection()

    if not database:
        raise DatabaseConnectionFail()
    
    placeholder = ', '.join(['%s'] * len(friends_gamertags))

    cursor.execute(
        f'SELECT * FROM banlist WHERE xbox_name IN ({placeholder})',
        (friends_gamertags)
    )

    friend_ban_cases = cursor.fetchall()

    _close_database_connection(database = database, cursor = cursor)

    return friend_ban_cases

def add_ban(member_name: str, member_id: int, xbox_gamertag: str, reason: str):
    database, cursor = _open_database_connection()

    if not database:
        raise DatabaseConnectionFail()

    cursor.execute(
        'INSERT INTO banlist(discord_name,discord_id,xbox_name,reason) VALUES (%s,%s,%s,%s)',
        (member_name, member_id, xbox_gamertag, reason)
    )

    database.commit()
    
    _close_database_connection(database = database, cursor = cursor)


def delete_ban(case: int):
    database, cursor = _open_database_connection()

    cursor.execute(
        'DELETE FROM banlist WHERE ban_id = %s',
        (case)
    )

    database.commit()

    _close_database_connection(database = database, cursor = cursor)