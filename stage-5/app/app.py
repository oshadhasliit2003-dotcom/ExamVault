"""EV-05 Exam Portal: an INTENTIONALLY VULNERABLE training app (IDOR only).
Run only inside the isolated CTF lab. Do not expose to any real network."""
import os, sqlite3
from flask import Flask, g, redirect, render_template, request, session, url_for, abort

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")
DB = os.environ.get("DB_PATH", "/tmp/portal.db")
FLAG = os.environ.get("FLAG", "EXAM{placeholder_set_FLAG_env}")

def db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close(_):
    d = g.pop("db", None)
    if d: d.close()

def init_db():
    if os.path.exists(DB): os.remove(DB)
    c = sqlite3.connect(DB)
    c.executescript("""
    CREATE TABLE users(id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, role TEXT);
    CREATE TABLE records(id INTEGER PRIMARY KEY, owner_id INTEGER, title TEXT, body TEXT);
    """)
    c.executemany("INSERT INTO users VALUES(?,?,?,?)", [
        (1, "exam_office", "not-for-players-9f3a", "staff"),
        (2, "student_guest", "guest2026", "student")])
    c.executemany("INSERT INTO records VALUES(?,?,?,?)", [
        (100, 2, "Your exam registration", "You are registered for Applied Network Defence."),
        (101, 1, "Internal: leak review reference", "Case reference: " + FLAG),
        (102, 1, "Invigilator roster", "Roster is held by the Examinations Office."),
        (103, 1, "Hall B seating plan", "Seating plans are published two days before exams."),
        (104, 2, "Results release notice", "Results are released after moderation.")])
    c.commit(); c.close()

def current_user():
    uid = session.get("uid")
    if not uid: return None
    return db().execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()

@app.route("/")
def index():
    return redirect(url_for("dashboard") if current_user() else url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        u = db().execute("SELECT * FROM users WHERE username=? AND password=?",
                         (request.form.get("username", ""), request.form.get("password", ""))).fetchone()
        if u:
            session["uid"] = u["id"]
            return redirect(url_for("dashboard"))
        error = "Wrong username or password."
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    u = current_user()
    if not u: return redirect(url_for("login"))
    rows = db().execute("SELECT id, title FROM records WHERE owner_id=?", (u["id"],)).fetchall()
    return render_template("dashboard.html", user=u, records=rows)

@app.route("/record/<int:rid>")
def record(rid):
    u = current_user()
    if not u: return redirect(url_for("login"))
    r = db().execute("SELECT * FROM records WHERE id=?", (rid,)).fetchone()  # INTENTIONAL FLAW: no owner check
    if not r: abort(404)
    return render_template("record.html", record=r, user=u)

init_db()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
