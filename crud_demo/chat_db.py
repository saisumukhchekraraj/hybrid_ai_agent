import sqlite3
DB_NAME = "chat_memory.db"
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            user_input TEXT NOT NULL,
            ai_response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
def add_conversation(
    user_name,
    user_input,
    ai_response
):
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
              """
              INSERT INTO chat_history
              (user_name, user_input, ai_response)
              VALUES (?, ?, ?)
              """,
              (user_name, user_input, ai_response)
)
    conn.commit()
    conn.close()
def get_all_conversations():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM chat_history""")
    conversations = cursor.fetchall()
    conn.close()
    return [dict(row) for row in conversations]
def get_conversation(id):

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
    """
    SELECT *
    FROM chat_history
    WHERE id = ?
    """,
    (id,)
    )
    conversation = cursor.fetchone()
    conn.close()
    return dict(conversation) if conversation else None
def update_conversation(
    conversation_id,
    new_user_input,
    new_ai_response
): 
    conn= get_connection()
    cursor=conn.cursor()
    cursor.execute(
        """ 
    UPDATE chat_history
    SET
    user_input = ?,
    ai_response = ?
    WHERE id=?
""", (   new_user_input,
    new_ai_response,
    conversation_id)
    )
    rows_updated = cursor.rowcount

    conn.commit()
    conn.close()
    return rows_updated 
def delete_conversation(
    conversation_id
):
    conn= get_connection()
    cursor= conn.cursor()
    cursor.execute(
        """
    DELETE FROM chat_history
    WHERE id=?
""", (conversation_id,)
    )
    rows_deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_deleted