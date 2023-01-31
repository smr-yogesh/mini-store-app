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



@app.route('/order', methods=["GET", "POST"])
def order():
    
    if request.method == "POST":
        cursor = connection.cursor()

        customer_name_ = request.form['Customer Name']
        total_ = request.form["Total"]
        date_ = request.form["Date"]

        cursor.execute("""INSERT INTO ORDERS (customer_name, total, date)
                          VALUES (%s, %s, %s);""", (customer_name_, total_, date_))

        connection.commit()
        
        return redirect(url_for('order'))

    else:
        cursor = connection.cursor()
        cursor.execute(""" SELECT * FROM ORDERS """)
        orders = cursor.fetchall()

        return render_template('order.html', data=orders)


@app.route('/deleteorder/<id>', methods=["GET"])
def delete_order(id):
    cursor = connection.cursor()
    cursor.execute("""
                    DELETE FROM ORDERS 
                    WHERE ORDER_ID= %s;
                """, (id,))
    connection.commit()

    return redirect(url_for('order'))


@app.route('/orderdetail', methods=["GET"])
def order_detail():
   
    cursor = connection.cursor()
    cursor.execute(""" 
                        SELECT 
                                PRODUCTS.PRODUCTS_ID, PRODUCTS.NAME, PRODUCTS.UNIT_PRICE, AMOUNT, TOTAL_PRICE
                            FROM
                                ORDER_DETAILS
                            RIGHT JOIN PRODUCTS ON PRODUCTS.PRODUCTS_ID = ORDER_DETAILS.PRODUCT_ID
                            LEFT JOIN ORDERS ON ORDERS.ORDER_ID = ORDER_DETAILS.ORDER_ID 
                  """)
    order_detail_ = cursor.fetchall() 
        
    return render_template('order.html', orderdetail=order_detail_)

  
    



# run controller
if __name__ == "__main__":
    app.run(debug=True)





""""
# Error page
@app.errorhandler(404)
def page_not_found(error):  
    return render_template('page_not_found.html'), 404

@app.errorhandler(500)
def page_not_found(error):  
    return render_template('not-found-500.html'), 500

"""