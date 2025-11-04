import sqlite3
import calendar
import locale

from flask import Flask, render_template, g, jsonify, request, redirect, url_for

locale.setlocale(locale.LC_ALL, "fr_FR")

DATABASE = 'groceries.db'

app = Flask(__name__)

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
    cur = get_db().cursor()
    cur.execute('SELECT rowid, "date" FROM lists WHERE archived = FALSE ORDER BY "date" DESC;')
    data = cur.fetchall()
    lists = []
    for i in data:
        lists.append({ "id": i[0], "date": i[1] })
    return render_template("index.html", lists=lists)

@app.get("/alleys")
def alleys():
    cur = get_db().cursor()
    cur.execute("""SELECT a.rowid, a.name, ao."order"
                FROM alleys a 
                LEFT JOIN alleys_orders ao ON ao.alley_id = a.rowid 
                order by ao."order" asc;""")
    data = cur.fetchall()
    alleys = []
    for i in data:
        alleys.append({ "id": i[0], "name": i[1], "order": "" if i[2] is None else i[2] })
    return render_template("alleys.html", alleys=alleys)

@app.route("/alleys/add", methods=["GET", "POST"])
def alleys_add():
    """Add new alley"""
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
            cur.execute('INSERT INTO alleys_orders (alley_id, "order") VALUES (?, ?)',
                        (item["alley_id"],item["order"],))
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
    cur.execute("DELETE FROM alleys_orders WHERE alley_id = ?", (id,))
    cur.connection.commit()
    cur.execute("UPDATE products set alley_id = NULL WHERE alley_id = ?", (id,))
    cur.connection.commit()
    return "",204

@app.get("/products")
def products():
    cur = get_db().cursor()
    cur.execute("""SELECT p.rowid, p.name, a.name
                FROM products p 
                LEFT JOIN alleys a ON a.rowid = p.alley_id 
                ORDER BY p.name ASC;""")
    data = cur.fetchall()
    products = []
    for i in data:
        products.append({ "id": i[0], "name": i[1], "alley": "" if i[2] is None else i[2] })

    return render_template("products.html", products=products)

@app.route("/products/add", methods=["GET", "POST"])
def products_add():
    if request.method == "POST":
        product = request.form["product"]
        alley_id = request.form["alley_id"]

        if product is None or product == "":
            return "", 400

        cur = get_db().cursor()
        cur.execute("INSERT INTO products (name, alley_id) VALUES (?, ?)",
                    (product.upper(), alley_id,))
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
def products_edit(id):
    if request.method == "POST":
        product_id = request.form["product_id"]
        product = request.form["product"]
        alley_id = request.form["alley_id"]

        if product is None or product == "":
            return "", 400
        
        cur = get_db().cursor()
        cur.execute("UPDATE products SET name = ?, alley_id = ? where rowid = ?;", (product.upper(), alley_id, product_id))
        cur.connection.commit()

        return redirect(url_for('products'))
    
    cur = get_db().cursor()
    cur.execute("SELECT rowid, name, alley_id FROM products where rowid = ?;", (id,))
    data = cur.fetchone()
    product = { "id": data[0], "name": data[1], "alley_id": data[2] }
    
    cur = get_db().cursor()
    cur.execute("SELECT rowid, name FROM alleys order by name asc;")
    data = cur.fetchall()
    alleys = []
    for i in data:
        alleys.append({ "id": i[0], "name": i[1] })
    
    return render_template("products/edit.html", alleys=alleys, product=product)

@app.route("/lists/add", methods=["GET", "POST"])
def lists_add():
    if request.method == "POST":
        date = request.form["date"]
        cur = get_db().cursor()
        cur.execute('INSERT INTO lists ("date") VALUES (?)', (date,))
        cur.connection.commit()
        return redirect(url_for("lists_edit", id=cur.lastrowid))
    
    return render_template("lists/add.html")

@app.get("/lists/<int:id>")
def lists_edit(id):
    cur = get_db().cursor()
    cur.execute('SELECT rowid, "date" FROM lists WHERE rowid = ?;', (id,))
    data = cur.fetchone()
    if data is None:
        return "", 404 
    
    list = { "id": data[0], "date": data[1] }

    cur = get_db().cursor()
    cur.execute('select p.name, p.rowid from products p join lists_products lp on lp.products_id = p.rowid where lp.list_id = ? order by p.name;', (id,))
    data = cur.fetchall()
    products = []
    for i in data:
        products.append({ "name": i[0], "id": i[1] })

    return render_template("lists/edit.html", list=list, products=products)

@app.get("/products/search")
def products_search():
    query = request.args.get('q')
    cur = get_db().cursor()
    cur.execute("SELECT rowid, name FROM products where name LIKE ? order by name asc LIMIT 10;", (query + "%",))
    data = cur.fetchall()
    result = []
    for i in data:
       result.append({ "id": i[0], "name": i[1] })
    return jsonify(result)

@app.post("/lists/add-product")
def lists_add_product():
    body = request.get_json()
    cur = get_db().cursor()
    cur.execute('INSERT INTO lists_products (list_id, products_id) VALUES (?, ?)', (body["list_id"],body["products_id"],))
    cur.connection.commit()
    return "", 201

@app.delete("/lists/<int:list_id>/delete-product/<int:product_id>")
def lists_delete_product(list_id, product_id):
    cur = get_db().cursor()
    cur.execute('DELETE FROM lists_products WHERE list_id = ? and products_id = ?', (list_id,product_id,))
    cur.connection.commit()
    return "", 204

@app.get("/lists/start/<int:id>")
def lists_start(id):
    cur = get_db().cursor()
    cur.execute("""select a.name, p.name
from lists_products lp 
join products p ON p.rowid = lp.products_id 
join alleys a ON a.rowid = p.alley_id 
left join alleys_orders ao ON ao.alley_id = a.rowid
where lp.list_id = ?
order by ao."order";""", (id,))
    data = cur.fetchall()
    
    list = {}
    for i in data:
        val = list.get(i[0])

        if val is None:
            list[i[0]] = []
            list[i[0]].append(i[1])
            continue 

        val.append(i[1])
    return render_template("lists/start.html", list=list)

@app.put("/lists/archive/<int:id>")
def lists_archive(id):
    cur = get_db().cursor()
    cur.execute('UPDATE lists SET archived = TRUE where rowid = ?', (id,))
    cur.connection.commit()
    return "", 204

@app.get("/meals")
def meals():
    cur = get_db().cursor()
    cur.execute("select day, day_part, meal from meals;")
    data = cur.fetchall()

    week_days = list(calendar.day_name)
    meals = {}
    current_day = ""
    tmp = {}
    for i in data:
        day = week_days[i[0]]
  
        if current_day == day:
            meals[day] = tmp | { i[1]: "" if i[2] is None else i[2] } 
            continue

        tmp = { i[1]: i[2] } 
        current_day = day

    for day, meal in meals.items():
        print(day, meal)

    return render_template("meals.html", meals=meals)

@app.put("/meals/edit")
def meals_edit():
    week_days = list(calendar.day_name)
    body = request.get_json()
    day_idx = week_days.index(body["day"])
    day_part = body["dayPart"]
    meal = body["meal"]

    cur = get_db().cursor()
    cur.execute('UPDATE meals SET meal = ? where day = ? AND day_part = ?;', (meal, day_idx, day_part,))
    cur.connection.commit()

    return "", 204

if __name__ == '__main__':
    app.run(debug=True)
    