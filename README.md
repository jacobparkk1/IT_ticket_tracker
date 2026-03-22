# IT Ticket Tracker

A lightweight web-based IT ticket management system built with Python and Flask. Allows IT staff to log, view, edit, and manage support tickets through a clean browser interface — no external database software required.

---

## Features

- **Dashboard** — View all tickets sorted by newest first in a clickable table
- **Create Tickets** — Manually log new tickets with title, description, priority, and status
- **Edit Tickets** — Update any ticket's information with a pre-filled edit form
- **CSV Upload** — Bulk import tickets from a CSV file with automatic data normalization
- **CSV Export** — Download the full ticket list as a dated CSV file
- **Ticket Detail View** — View full details of any individual ticket

---

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite (via Python's built-in `sqlite3`)
- **Frontend:** HTML, CSS, Jinja2, JavaScript
- **Libraries:** `csv`, `io`, `datetime` (all Python standard library — no extra installs beyond Flask)

---

## Project Structure

```
IT_ticket_tracker/
├── app.py               # Flask application, all routes and database logic
├── tickets.db           # SQLite database (auto-generated on first run)
├── static/
│   └── style.css        # Stylesheet
└── templates/
    ├── base.html        # Base layout template
    ├── index.html       # Dashboard / ticket list
    ├── new-ticket.html  # Create new ticket form
    ├── edit-ticket.html # Edit existing ticket form
    ├── ticket.html      # Individual ticket detail view
    └── upload.html      # CSV upload page
```

---

## Getting Started

### Prerequisites

- Python 3.x
- Flask

Install Flask if you don't have it:

```bash
pip install flask
```

### Running the App

```bash
python app.py
```

Then open your browser and go to `http://127.0.0.1:5000`

The `tickets.db` database file will be created automatically in the project directory on first run.

---

## CSV Upload Format

CSV files must have the following headers in the first row:

```
title,description,priority,status,created_at
```

**Valid values:**
- `priority`: `Low`, `Medium`, `High` (case insensitive — auto-normalized on upload)
- `status`: `Opened`, `Active`, `Closed` (case insensitive — `Open` is automatically corrected to `Opened`)
- `created_at`: `YYYY-MM-DD HH:MM` format preferred — Excel's `MM/DD/YYYY HH:MM` format is automatically converted

**Example row:**
```
Printer offline,Printer on 2nd floor not responding,High,Opened,2026-03-18 10:00
```

---
