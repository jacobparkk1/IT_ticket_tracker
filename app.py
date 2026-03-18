from time import strftime

from flask import Flask, render_template, request, redirect
from datetime import datetime
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("tickets.db")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    priority TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL)
    """)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect("tickets.db")
    tickets = conn.execute("SELECT * FROM tickets ORDER BY id DESC").fetchall()

    return render_template("index.html", tickets=tickets)

@app.route("/upload", methods=["GET","POST"])
def upload():
    return render_template("upload.html")

@app.route("/ticket/new", methods=["GET", "POST"])
def new():
    if request.method == "GET":
        return render_template("new-ticket.html")

    elif request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]
        status = request.form["status"]
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect("tickets.db")
        conn.execute("""
        INSERT INTO tickets (title, description, priority, status, created_at)
            VALUES (?,?,?,?,?)
            """, (title, description, priority, status, created_at))
        conn.commit()
        conn.close()
        return redirect("/")


@app.route("/ticket/<int:id>")
def ticket(id):
    conn = sqlite3.connect("tickets.db")
    ticket = conn.execute("SELECT * FROM tickets WHERE id = ?", (id,))
    ticket = ticket.fetchone()
    return render_template("single-ticket.html", ticket=ticket)


@app.route("/ticket/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect("tickets.db")
    ticket = conn.execute("SELECT * FROM tickets WHERE id = ?", (id,))
    ticket = ticket.fetchone()
    if request.method == "GET":
        return render_template("edit-ticket.html", ticket=ticket)
    elif request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        priority = request.form["priority"]
        status = request.form["status"]

        conn.execute("""
                     UPDATE tickets SET title=?, description=?, priority=?, status=? WHERE id=?
                     """, (title, description, priority, status, id))
        conn.commit()
        conn.close()

        return redirect(f"/ticket/{id}")


        #created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")



if __name__ == '__main__':
    init_db()
    app.run(debug=True)