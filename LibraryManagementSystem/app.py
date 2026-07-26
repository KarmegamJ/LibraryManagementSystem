from flask import Flask, render_template, request, redirect
import pymysql
import sqlite3

app = Flask(__name__)

# Database Configuration
db = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="library"
)

def create_table():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        author TEXT
    )
    """)

    conn.commit()
    conn.close()

create_table()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/addbook', methods=['GET', 'POST'])
def add_book():

    if request.method == 'POST':

        title = request.form['title']
        author = request.form['author']

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO books(title, author) VALUES (?, ?)",
            (title, author)
        )

        conn.commit()
        conn.close()

        return redirect('/viewbooks')

    return render_template('add_book.html')


@app.route('/viewbooks')
def view_books():

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")

    books = cursor.fetchall()

    conn.close()

    return render_template('view_books.html', books=books)


if __name__ == "__main__":
    app.run(debug=True)