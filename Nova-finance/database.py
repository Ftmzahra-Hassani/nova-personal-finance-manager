import sqlite3
from datetime import date


class Database:

    def __init__(self):

        self.connection = sqlite3.connect("finance.db")

        self.cursor = self.connection.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""

            CREATE TABLE IF NOT EXISTS transactions (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                title TEXT NOT NULL,

                amount REAL NOT NULL,

                category TEXT NOT NULL,

                transaction_type TEXT NOT NULL,

                transaction_date TEXT NOT NULL,

                note TEXT

            )

        """)

        self.connection.commit()

    def add_transaction(
        self,
        title,
        amount,
        category,
        transaction_type,
        transaction_date,
        note
    ):

        self.cursor.execute("""

            INSERT INTO transactions (

                title,
                amount,
                category,
                transaction_type,
                transaction_date,
                note

            )

            VALUES (?, ?, ?, ?, ?, ?)

        """, (

            title,
            amount,
            category,
            transaction_type,
            transaction_date,
            note

        ))

        self.connection.commit()

    def get_transactions(self, search="", transaction_type="All"):

        query = "SELECT * FROM transactions WHERE 1=1"

        parameters = []

        if search:

            query += " AND title LIKE ?"

            parameters.append(f"%{search}%")

        if transaction_type != "All":

            query += " AND transaction_type = ?"

            parameters.append(transaction_type)

        query += " ORDER BY transaction_date DESC, id DESC"

        self.cursor.execute(query, parameters)

        return self.cursor.fetchall()

    def delete_transaction(self, transaction_id):

        self.cursor.execute("""

            DELETE FROM transactions

            WHERE id = ?

        """, (transaction_id,))

        self.connection.commit()

    def get_summary(self):

        self.cursor.execute("""

            SELECT

                SUM(
                    CASE
                        WHEN transaction_type = 'Income'
                        THEN amount
                        ELSE 0
                    END
                ),

                SUM(
                    CASE
                        WHEN transaction_type = 'Expense'
                        THEN amount
                        ELSE 0
                    END
                )

            FROM transactions

        """)

        result = self.cursor.fetchone()

        income = result[0] or 0

        expense = result[1] or 0

        balance = income - expense

        return income, expense, balance

    def get_monthly_summary(self):

        current_month = date.today().strftime("%Y-%m")

        self.cursor.execute("""

            SELECT

                SUM(
                    CASE
                        WHEN transaction_type = 'Income'
                        THEN amount
                        ELSE 0
                    END
                ),

                SUM(
                    CASE
                        WHEN transaction_type = 'Expense'
                        THEN amount
                        ELSE 0
                    END
                )

            FROM transactions

            WHERE transaction_date LIKE ?

        """, (current_month + "%",))

        result = self.cursor.fetchone()

        income = result[0] or 0

        expense = result[1] or 0

        return income, expense

    def close(self):
        self.connection.close()