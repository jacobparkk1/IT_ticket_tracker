"""
IT Ticket Tracker
Author: Jacob Park
Purpose: Track IT tickets, import and export ticket lists,
create and edit individual tickets.
"""

from time import strftime
from flask import Flask, render_template, request, redirect, make_response
from datetime import datetime, time
import sqlite3, csv, io
#___________________________________________________________________________________________________________
app = Flask(__name__)

def init_db():
    """ 
    Initilize "tickets.db" database in directory if none exists.
    Establishes ticket ID in autoincrement
    """
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
#________________________________________________________________________________________________________
@app.route('/')
def index():
    """ Renders index template with dashboard list, sorting by descending ticket ID """
    
    conn = sqlite3.connect("tickets.db")
    tickets = conn.execute("SELECT * FROM tickets ORDER BY id DESC").fetchall()

    return render_template("index.html", tickets=tickets)
#__________________________________________________________________________________________________________
@app.route("/upload", methods=["GET","POST"])
def upload():
    """ 
    Renders upload page where csv can be provided. Post method recieves
    data from each row and inserts into the database 
    """
    if request.method == "GET":
        return render_template("upload.html")
        
    elif request.method == "POST":
        file = request.files["file-input"] # initialize csv parsing
        stream = file.stream.read().decode("utf-8").splitlines()
        reader = csv.DictReader(stream)
        conn = sqlite3.connect("tickets.db") # connect database
        
        for element in reader: # strip data by keys
            title = element["title"].capitalize()
            priority = element["priority"].capitalize()
            status = element["status"].capitalize()
            if status == "Open": # Autocorrect instances of O/open to standardized "Opened"
                status = "Opened"
            created_at = element["created_at"]
            try: # Checks for and corrects automatic excel date format to standardize
                created_at = datetime.strptime(created_at, "%m/%d/%Y %H:%M").strftime("%Y-%m-%d %H:%M")
            except ValueError:
                pass
            description = element["description"]
            # insert data into database
            conn.execute(""" 
            INSERT INTO tickets (title, description, priority, status, created_at)
                VALUES (?,?,?,?,?)
                """, (title, description, priority, status, created_at))
        conn.commit()
        conn.close()
        return redirect("/") # send user to index (dashboard}
#__________________________________________________________________________________________________________
@app.route("/download", methods=["GET"])
def download():
    """ Grabs data from database, writes to csv file and returns to user as attachment """
    
    date = datetime.now().strftime("%Y-%m-%d") # sets date
    
    conn = sqlite3.connect("tickets.db") # connect database, inialize csv writer and header
    tickets = conn.execute("SELECT * FROM tickets ORDER BY id DESC").fetchall()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "title", "description", "priority", "status", "created_at"])
    for ticket in tickets: # write each row to csv
        writer.writerow(ticket)
    output.seek(0) # return to start of stringIO

    # wraps csv in HTTP response, labeled and treated as csv
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename=tickets-{date}.csv"
    response.headers["Content-Type"] = "text/csv"
    return response # send attatchement to user
#_____________________________________________________________________________________________________________
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
