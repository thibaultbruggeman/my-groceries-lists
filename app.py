import sqlite3

from flask import Flask, render_template, g, jsonify, request
from flask_cors import CORS

DATABASE = 'groceries.db'

app = Flask(__name__)
CORS(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/alleys")
def get_all_alleys():
    cur = get_db().cursor()
    cur.execute("SELECT rowid, name FROM alleys")
    data = cur.fetchall()
    alleys = []
    for i in data:
            alleys.append({ "id": i[0], "name": i[1] })
    return jsonify(alleys)

@app.post("/api/alleys")
def create_alley():
    body = request.get_json()
    name = body["name"]
    cur = get_db().cursor()
    cur.execute("INSERT INTO alleys (name) VALUES (?)", (name,))
    cur.connection.commit()
    return "",201

@app.delete("/api/alleys/<int:id>")
def delete_alley(id):
    cur = get_db().cursor()
    cur.execute("DELETE FROM alleys WHERE rowid = ?", (id,))
    cur.connection.commit()
    return "",204

@app.post("/api/alleys_orders")
def set_alleys_orders():
    body = request.get_json()
    cur = get_db().cursor()
    cur.execute("DELETE FROM alleys_orders")
    cur.connection.commit()
    for item in body:
        cur.execute('INSERT INTO alleys_orders (alley_id, "order") VALUES (?, ?)', (item["id"], item["order"], ))
        cur.connection.commit()
        print(item)
    return "", 201

if __name__ == '__main__':
    app.run(debug=True)