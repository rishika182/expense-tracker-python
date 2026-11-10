import sqlite3

def get_connection():
    return sqlite3.connect("expenses.db")

def create_table():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            note TEXT,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_expense(amount, category, note, date):
    conn = get_connection()
    conn.execute(
        "INSERT INTO expenses (amount, category, note, date) VALUES (?, ?, ?, ?)",
        (amount, category, note, date),
    )
    conn.commit()
    conn.close()

def get_all_expenses():
    conn = get_connection()
    rows = conn.execute(
        "SELECT id, amount, category, note, date FROM expenses ORDER BY date DESC"
    ).fetchall()
    conn.close()
    return rows

def update_expense(expense_id, amount, category, note):
    conn = get_connection()
    conn.execute(
        "UPDATE expenses SET amount = ?, category = ?, note = ? WHERE id = ?",
        (amount, category, note, expense_id),
    )
    conn.commit()
    conn.close()

def delete_expense(expense_id):
    conn = get_connection()
    conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

def get_monthly_summary(month):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT category, ROUND(SUM(amount), 2) AS total
        FROM expenses
        WHERE substr(date, 1, 7) = ?
        GROUP BY category
        ORDER BY total DESC
        """,
        (month,),
    ).fetchall()
    conn.close()
    return rows