from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "bus.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS bookings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        passenger_name TEXT NOT NULL,
        departure_city TEXT NOT NULL,
        destination_city TEXT NOT NULL,
        travel_date TEXT NOT NULL,
        seats INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/booking", methods=["GET", "POST"])
def booking():

    if request.method == "POST":

        passenger_name = request.form["passenger_name"]
        departure_city = request.form["departure_city"]
        destination_city = request.form["destination_city"]
        travel_date = request.form["travel_date"]
        seats = request.form["seats"]

        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO bookings
        (passenger_name, departure_city, destination_city, travel_date, seats)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            passenger_name,
            departure_city,
            destination_city,
            travel_date,
            seats
        ))

        conn.commit()
        conn.close()

        return redirect("/admin")

    return render_template("booking.html")


@app.route("/admin")
def admin():

    buses = [
        (101, "Cairo -> Giza", 40),
        (202, "Alexandria -> Cairo", 35)
    ]

    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    cur.execute("SELECT * FROM bookings")
    bookings = cur.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        buses=buses,
        bookings=bookings
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)