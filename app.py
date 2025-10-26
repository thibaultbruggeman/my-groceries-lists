import sqlite3

from flask import Flask, render_template, g, jsonify, request, redirect, url_for
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

# Views
@app.get("/")
def home():
    return render_template("index.html")

@app.get("/alleys")
def alleys():
    cur = get_db().cursor()
    cur.execute('SELECT a.rowid, a.name, ao."order" FROM alleys a LEFT JOIN alleys_orders ao ON ao.alley_id = a.rowid order by ao."order" asc;')
    data = cur.fetchall()
    alleys = []
    for i in data:
            alleys.append({ "id": i[0], "name": i[1], "order": "" if i[2] is None else i[2] })
    return render_template("alleys.html", alleys=alleys)

@app.route("/alleys/add", methods=["GET", "POST"])
def alleys_add():
    if request.method == "POST":
        alley = request.form["alley"]

        if alley is None or alley == "":
            return "", 400
    
        cur = get_db().cursor()
        cur.execute("INSERT INTO alleys (name) VALUES (?)", (alley.upper(),))
        cur.connection.commit()

        return redirect(url_for('alleys'))
    return render_template("alleys/add.html")

@app.route("/alleys/order", methods=["GET", "POST"])
def alleys_order():
    if request.method == "POST":
        body = request.get_json()
        cur = get_db().cursor()
        cur.execute("DELETE FROM alleys_orders;")
        cur.connection.commit()
        for item in body:
            cur.execute('INSERT INTO alleys_orders (alley_id, "order") VALUES (?, ?)', (item["alley_id"],item["order"],))
            cur.connection.commit()
        return "", 201

    cur = get_db().cursor()
    cur.execute("SELECT rowid, name FROM alleys")
    data = cur.fetchall()
    alleys = []
    for i in data:
            alleys.append({ "id": i[0], "name": i[1] })

    return render_template("alleys/order.html", alleys=alleys)

@app.delete("/alleys/delete/<int:id>")
def alleys_delete(id):
    cur = get_db().cursor()
    cur.execute("DELETE FROM alleys WHERE rowid = ?", (id,))
    cur.connection.commit()
    return "",204

@app.get("/products") 
def products():
    cur = get_db().cursor()
    cur.execute("SELECT p.rowid, p.name, a.name FROM products p LEFT JOIN alleys a ON a.rowid = p.alley_id ORDER BY p.name ASC;")
    data = cur.fetchall()
    products = []
    for i in data:
        products.append({ "id": i[0], "name": i[1], "alley": i[2] })

    return render_template("products.html", products=products)

@app.route("/products/add", methods=["GET", "POST"]) 
def products_add():
    if request.method == "POST":
        product = request.form["product"]
        alley_id = request.form["alley_id"]

        if product is None or product == "":
            return "", 400
        
        cur = get_db().cursor()
        cur.execute("INSERT INTO products (name, alley_id) VALUES (?, ?)", (product.upper(), alley_id,))
        cur.connection.commit()

        return redirect(url_for('products'))
    
    cur = get_db().cursor()
    cur.execute("SELECT rowid, name FROM alleys order by name asc;")
    data = cur.fetchall()
    alleys = []
    for i in data:
            alleys.append({ "id": i[0], "name": i[1] })
    
    return render_template("products/add.html", alleys=alleys)

@app.route("/products/<int:id>", methods=["GET", "POST"]) 
def products_edit():
    if request.method == "POST":
        product = request.form["product"]
        alley_id = request.form["alley_id"]

        if product is None or product == "":
            
            return "", 400
        
        cur = get_db().cursor()
        cur.execute("INSERT INTO products (name, alley_id) VALUES (?, ?)", (product.upper(), alley_id,))
        cur.connection.commit()

        return redirect(url_for('products'))
    
    cur = get_db().cursor()
    cur.execute("SELECT rowid, name FROM alleys order by name asc;")
    data = cur.fetchall()
    alleys = []
    for i in data:
            alleys.append({ "id": i[0], "name": i[1] })
    
    return render_template("products/add.html", alleys=alleys)

if __name__ == '__main__':
    app.run(debug=True)