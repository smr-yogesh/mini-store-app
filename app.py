from flask import Flask, render_template, url_for, request, redirect
from sql_connection import get_sql_connection

app = Flask(__name__)

connection = get_sql_connection()

@app.route('/')
def home():
    cursor = connection.cursor()
    cursor.execute("SELECT products_id, products.name, products.unit_price, uom.uom_name FROM products join uom on uom.uom_id = products.uom_id;")
    data = cursor.fetchall()

    return render_template('home.html', data = data)

@app.route('/add_product', methods=["POST"])
def add_product():
    uom_id = request.form['uom_id']
    name = request.form['name']
    unit_price = request.form['Unit Price']
    
    cursor = connection.cursor()
    cursor.execute("insert into products (uom_id, name, unit_price) values (%s, %s, %s);", (uom_id, name, unit_price))
    connection.commit()

    return redirect(url_for('home'))

@app.route('/update', methods=["POST"])
def update():
    id = request.form['id']
    name = request.form['name']
    
    cursor = connection.cursor()
    cursor.execute("""
                    UPDATE PRODUCTS 
                    SET NAME = %s
                    WHERE PRODUCTS_ID = %s
                """, (name, id))
    connection.commit()

    return redirect(url_for('home'))


@app.route('/delete/<id>', methods=["GET"])
def delete(id):
    cursor = connection.cursor()
    cursor.execute("""
                    DELETE FROM PRODUCTS 
                    WHERE PRODUCTS_ID= %s;
                """, (id,))
    connection.commit()

    return redirect(url_for('home'))


@app.errorhandler(404)
def page_not_found(error):  
    return render_template('page_not_found.html'), 404

@app.errorhandler(500)
def page_not_found(error):  
    return render_template('not-found-500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)