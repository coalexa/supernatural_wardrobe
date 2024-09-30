# Citation for the code/routes/functions in app.py:
# Date: 10/27/2022
# Adapted from: GitHub Flask Starter App
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py

from flask import Flask, render_template, json, redirect, request
from flask_mysqldb import MySQL
from datetime import datetime
import os
import database.db_connector as db

app = Flask(__name__)
db_connection = db.connect_to_database()

# reconnect to database
db_connection.ping(True)

# ----------------------------------- ROUTES -----------------------------------

# --------------------------------- HOME PAGE ----------------------------------

@app.route('/')
def root():
    return render_template("main.j2")

# --------------------------------- COSTUMES ROUTE ----------------------------------

@app.route('/costumes', methods=["GET", "POST"])
def costumes():
    # get costumes data to send back to template to display
    if request.method == "GET":
        # mySQL query to get all costumes
        query = "SELECT costume_id AS ID, costume_name AS Name, price AS 'Price Per Unit', costume_description AS Description, themes.theme_description AS Theme \
                 FROM costumes INNER JOIN themes ON costumes.theme_id = themes.theme_id \
                 ORDER BY costume_id ASC"
        data = db.execute_query(db_connection, query).fetchall()

        # mySQL query to get theme id/theme description for dropdown menu
        query2 = "SELECT theme_id, theme_description FROM themes"
        theme_data = db.execute_query(db_connection, query2).fetchall()

        # render costumes page passing costumes/themes data to table template and dropdown
        return render_template("costumes.j2", data=data, themes=theme_data)

    # insert a costume into costumes entity
    if request.method == "POST":
        # fire off if user presses the 'Add Costume' button
        if request.form.get("Add_Costume"):
            # grab user form inputs
            costume_name = request.form["costume_name"]
            price = request.form["price"]
            costume_description = request.form["costume_description"]
            theme_id = request.form["theme_id"]
                
            # mySQL query to insert a new costume into costumes with the user form inputs
            query = "INSERT INTO costumes (costume_name, price, costume_description, theme_id) VALUES (%s,%s,%s,%s)"
            db.execute_query(db_connection, query, (costume_name, price, costume_description, theme_id))

            # redirect back to costumes page
            return redirect('/costumes')

# --------------------------------- EDIT COSTUMES ----------------------------------

@app.route("/edit_costume/<int:id>", methods=["GET", "POST"])
def edit_costume(id):
    if request.method == "GET":
        # mySQL query to grab the info of the costume with the passed id
        query = "SELECT costume_id, costume_name, price, costume_description, themes.theme_description, costumes.theme_id \
                 FROM costumes INNER JOIN themes ON costumes.theme_id = themes.theme_id WHERE costume_id = %s" % (id)
        data = db.execute_query(db_connection, query).fetchall()

        # mySQL query to get theme id/theme description for dropdown menu
        query2 = "SELECT theme_id, theme_description FROM themes"
        themes_data = db.execute_query(db_connection, query2).fetchall()

        # render edit_costumes page passing costumes/theme data to the edit_costumes template
        return render_template("edit_costumes.j2", data=data, themes=themes_data)

    # update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Costume' button
        if request.form.get("Edit_Costume"):
            # grab user form inputs
            costume_id = request.form["costume_id"]
            costume_name = request.form["costume_name"]
            price = request.form["price"]
            costume_description = request.form["costume_description"]
            theme_id = request.form["theme_id"]

            # mySQL query to update the attributes of a costume with the passed id and user form inputs
            query = "UPDATE costumes SET costumes.costume_name = %s, costumes.price = %s, costumes.costume_description = %s, costumes.theme_id = %s WHERE costumes.costume_id = %s"
            db.execute_query(db_connection, query, (costume_name, price, costume_description, theme_id, costume_id))

            # redirect back to costumes page after executing the update query
            return redirect('/costumes')

# --------------------------------- DELETE COSTUMES ----------------------------------

@app.route('/delete_costume/<int:id>')
def delete_costumes(id):
    try:
        # mySQL query to delete a costume with the passed id
        query = "DELETE FROM costumes WHERE costume_id = '%s'"
        db.execute_query(db_connection, query, (id,))

        # redirect back to costumes page
        return redirect('/costumes')

    # if the costume cannot be deleted because it's associated with an order, redirect to costumes page without deleting
    finally:
        return redirect('/costumes')

# --------------------------------- SEARCH COSTUMES ----------------------------------

@app.route('/search_costumes', methods=["POST"])
def search_costumes():
    # grab user form input
    search_costume = request.form["search_costume"]

    # mySQL query to obtain all attributes where costume name or theme description match user form
    query = "SELECT costume_id AS ID, costume_name AS Name, price AS Price, costume_description AS Description, themes.theme_description AS Theme \
             FROM costumes INNER JOIN themes ON costumes.theme_id = themes.theme_id \
             WHERE costume_name LIKE %s OR themes.theme_description LIKE %s ORDER BY costume_id ASC"
    search_data = db.execute_query(db_connection, query, ("%" + search_costume + "%", "%" + search_costume + "%")).fetchall()

    # render costumes page passing all matching search results to table template
    return render_template("costumes.j2", data=search_data)

# --------------------------------- THEMES ROUTE ----------------------------------

@app.route('/themes', methods=["GET", "POST"])
def themes():
    # get themes data to send back to template to display
    if request.method == "GET":
        # mySQL query to get all themes
        query = "SELECT theme_id AS ID, theme_description AS Description FROM themes ORDER BY theme_id ASC"
        data = db.execute_query(db_connection, query).fetchall()

        # render themes page passing themes data to table template
        return render_template("themes.j2", data=data)

    # insert a theme into themes entity
    if request.method == "POST":
        # fire off if user presses the 'Add Theme' button
        if request.form.get("Add_Theme"):
            # grab user form input
            theme_description = request.form["theme_description"]
                
            # mySQL query to insert a new theme into themes with the user form inputs
            query = "INSERT INTO themes (theme_description) VALUES (%s)"
            db.execute_query(db_connection, query, (theme_description,))

            # redirect back to themes page
            return redirect('/themes')

# --------------------------------- DELETE THEMES ----------------------------------

@app.route('/delete_theme/<int:id>')
def delete_themes(id):
    # try to delete theme with passed id from table
    try:
        # mySQL query to delete a theme with the passed id
        query = "DELETE FROM themes WHERE theme_id = '%s'"
        db.execute_query(db_connection, query, (id,))

        # redirect back to themes page
        return redirect('/themes')

    # if the theme cannot be deleted because it's in another table, redirect to themes page without deleting
    finally:
        return redirect('/themes')

# --------------------------------- INVENTORY ROUTE ----------------------------------

@app.route('/inventory', methods=["GET", "POST"])
def inventory():
    # get inventory data to send back to template to display
    if request.method == "GET":
        # mySQL query to get all inventory
        query = "SELECT inventory_id AS ID, stock AS Stock, inventory_description AS Description, costumes.costume_name AS 'Costume Name' \
                 FROM inventory LEFT JOIN costumes ON inventory.costume_id = costumes.costume_id \
                 ORDER BY inventory_id ASC"
        data = db.execute_query(db_connection, query).fetchall()

        # mySQL query to get costume id/costume name for dropdown menu
        query2 = "SELECT costume_id, costume_name FROM costumes"
        costume_data = db.execute_query(db_connection, query2).fetchall()

        # render inventory page passing inventory/costumes data to table template and dropdown
        return render_template("inventory.j2", data=data, costumes=costume_data)

    # insert an item into the inventory entity
    if request.method == "POST":
        # fire off if user presses the 'Add Inventory' button
        if request.form.get("Add_Inventory"):
            # grab user form inputs
            stock = request.form["stock"]
            inventory_description = request.form["inventory_description"]
            costume_id = request.form["costume_id"]
                
            # account for null stock
            if stock == "" or stock == "0":
                # mySQL query to insert an item into inventory with null stock and user form inputs
                query = "INSERT INTO inventory (inventory_description, costume_id) VALUES (%s,%s);"
                db.execute_query(db_connection, query, (inventory_description, costume_id))

            # no null inputs
            else:
                # mySQL query to insert an item into inventory with the user form inputs
                query2 = "INSERT INTO inventory (stock, inventory_description, costume_id) VALUES (%s,%s,%s);"
                db.execute_query(db_connection, query2, (stock, inventory_description, costume_id))

            # redirect back to inventory page
            return redirect('/inventory')

# --------------------------------- EDIT INVENTORY ----------------------------------

@app.route("/edit_inventory/<int:id>", methods=["GET", "POST"])
def edit_inventory(id):
    if request.method == "GET":
        # mySQL query to grab the info of the inventory with our passed id
        query = "SELECT inventory_id, stock, inventory_description, costumes.costume_name, inventory.costume_id \
                 FROM inventory LEFT JOIN costumes ON inventory.costume_id = costumes.costume_id WHERE inventory_id = %s" % (id)
        data = db.execute_query(db_connection, query).fetchall()

        # mySQL query to get costume id/costume theme for dropdown menu
        query2 = "SELECT costume_id, costume_name FROM costumes"
        costumes_data = db.execute_query(db_connection, query2).fetchall()
        
        # render edit_inventory page passing inventory/costumes data to the edit_inventory template
        return render_template("edit_inventory.j2", data=data, costumes=costumes_data)

    # update functionality
    if request.method == "POST": 
        # fire off if user clicks the 'Edit Inventory' button
        if request.form.get("Edit_Inventory"): 
            # grab user form inputs
            inventory_id = request.form["inventory_id"]
            stock = request.form["stock"]
            inventory_description = request.form["inventory_description"]
            costume_id = request.form["costume_id"]
           
            # account for null costume id and stock
            if (costume_id == "0") and (stock == "" or stock == "0"):
                query = "UPDATE inventory SET inventory.stock = NULL, inventory.inventory_description = %s, inventory.costume_id = NULL \
                         WHERE inventory.inventory_id = %s"
                db.execute_query(db_connection, query, (inventory_description, inventory_id))

            # account for null costume id
            elif costume_id == "0":
                # mySQL query to update the attributes of inventory with the passed id and user form inputs
                query2 = "UPDATE inventory SET inventory.stock = %s, inventory.inventory_description = %s, inventory.costume_id = NULL \
                          WHERE inventory.inventory_id = %s"
                db.execute_query(db_connection, query2, (stock, inventory_description, inventory_id))

            # account for null stock
            elif stock == "" or stock == "0":
                # mySQL query to update the attributes of inventory with the passed id and user form inputs
                query3 = "UPDATE inventory SET inventory.stock = NULL, inventory.inventory_description = %s, inventory.costume_id = %s \
                          WHERE inventory.inventory_id = %s"
                db.execute_query(db_connection, query3, (inventory_description, costume_id, inventory_id))

            # no null inputs
            else:
                # mySQL query to update the attributes of inventory with the passed id
                query4 = "UPDATE inventory SET inventory.stock = %s, inventory.inventory_description = %s, inventory.costume_id = %s WHERE inventory.inventory_id = %s"
                db.execute_query(db_connection, query4, (stock, inventory_description, costume_id, inventory_id))
           
            # redirect back to inventory page after executing the update query
            return redirect('/inventory')

# --------------------------------- DELETE INVENTORY ----------------------------------

@app.route('/delete_inventory/<int:id>')
def delete_inventory(id):
    # mySQL query to delete inventory with the passed id
    query = "DELETE FROM inventory WHERE inventory_id = '%s';"
    db.execute_query(db_connection, query, (id,))

    # redirect back to inventory page
    return redirect('/inventory')

# --------------------------------- SEARCH INVENTORY ----------------------------------

@app.route('/search_inventory', methods=["POST"])
def search_inventory():
    # grab user form input
    search_inventory = request.form["search_inventory"]

    # mySQL query to obtain all attributes where costume name matches user form
    query = "SELECT inventory_id AS ID, stock AS Stock, inventory_description AS Description, costumes.costume_name AS 'Costume Name' \
             FROM inventory INNER JOIN costumes ON inventory.costume_id = costumes.costume_id \
             WHERE costumes.costume_name LIKE %s ORDER BY inventory_id ASC"
    search_data = db.execute_query(db_connection, query, ("%" + search_inventory + "%",)).fetchall()

    # render inventory page passing all matching search results to table template
    return render_template("inventory.j2", data=search_data)

# --------------------------------- COMPANIES ROUTE ----------------------------------

@app.route('/companies', methods=["GET", "POST"])
def companies():
    # get companies data to send back to template to display
    if request.method == "GET":
        # mySQL query to get all companies 
        query = "SELECT company_id AS ID, company_name AS Name, phone AS Phone, email AS Email \
                 FROM companies ORDER BY company_id ASC"
        data = db.execute_query(db_connection, query).fetchall()

        # render companies page passing companies data to table template
        return render_template("companies.j2", data=data)

    # insert a company into companies entity
    if request.method == "POST":
        # fire off if use presses the 'Add Company' button
        if request.form.get("Add_Company"):
            # grab user form inputs
            company_name = request.form["company_name"]
            phone = request.form["phone"]
            email = request.form["email"]

            #  , mySQL query to insert a new company into companies with the user form inputs
            query = "INSERT INTO companies (company_name, phone, email) VALUES (%s,%s,%s)"
            db.execute_query(db_connection, query, (company_name, phone, email))

            # redirect back to companies page
            return redirect('/companies')

# --------------------------------- EDIT COMPANIES ----------------------------------

@app.route("/edit_company/<int:id>", methods=["GET", "POST"])
def edit_company(id):
    if request.method == "GET":
        # mySQL query to grab the info of the company with the passed id
        query = "SELECT company_id, company_name, phone, email \
                 FROM companies WHERE companies.company_id = %s" % (id)
        data = db.execute_query(db_connection, query).fetchall()
       
        # mySQL query to get company id/company name for dropdown menu
        query2 = "SELECT company_id, company_name FROM companies"
        company_data = db.execute_query(db_connection, query2).fetchall()

        # render edit_companies page passing companies data to the edit_companies template
        return render_template("edit_companies.j2", data=data, companies=company_data)

    # update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Company' button
        if request.form.get("Edit_Company"):
            # grab user form inputs
            company_id = request.form["company_id"]
            company_name = request.form["company_name"]
            phone = request.form["phone"]
            email = request.form["email"]

            # mySQL query to update attributes of a company with the passed if and user form inputs
            query = "UPDATE companies SET companies.company_name = %s, companies.phone = %s, companies.email = %s WHERE companies.company_id = %s"
            db.execute_query(db_connection, query, (company_name, phone, email, company_id))

            # redirect back to companies page after executing the update query
            return redirect('/companies')

# --------------------------------- SEARCH COMPANIES ----------------------------------

@app.route('/search_companies', methods=["POST"])
def search_companies():
    # grab user form input
    search_company = request.form["search_company"]

    # mySQL query to obtain all attributes where company name matches user form
    query = "SELECT company_id AS ID, company_name AS Name, phone AS Phone, email AS Email \
             FROM companies WHERE companies.company_name LIKE %s ORDER BY company_id ASC"
    search_data = db.execute_query(db_connection, query, ("%" + search_company + "%",)).fetchall()

    # render companies page passing all matching search results to table template
    return render_template("companies.j2", data=search_data)

# --------------------------------- ORDERS ROUTE ----------------------------------

@app.route('/orders', methods=["GET", "POST"])
def orders():
    # get orders data to send back to template to display
    if request.method == "GET":
        # mySQL query to get all orders
        query = "SELECT order_id AS ID, order_date AS 'Order Date', total AS Total, order_status AS 'Order Status', companies.company_name AS 'Company Name' \
                 FROM orders INNER JOIN companies ON orders.company_id = companies.company_id \
                 ORDER BY order_id ASC"
        data = db.execute_query(db_connection, query).fetchall()

        # mySQL query to get company id/company description for dropdown menu
        query2 = "SELECT company_id, company_name FROM companies"
        company_data = db.execute_query(db_connection, query2).fetchall()

        # mySQL query to get costume id/costume name for dropdown menu
        query3 = "SELECT costume_id, costume_name FROM costumes"
        costume_data = db.execute_query(db_connection, query3).fetchall()

        # render orders page passing orders/companies/costumes data to table template and dropdown
        return render_template("orders.j2", data=data, companies=company_data, costumes=costume_data)

    # insert an order into orders entity
    if request.method == "POST":
        # fire off if user presses the 'Add Order' button
        if request.form.get("Add_Order"):
            # grab user form input
            company_id = request.form["company_id"]

            # Citation for the following code:
            # Date: 11/29/2022
            # Copied from: Tutorials Point
            # Source URL: https://www.tutorialspoint.com/How-to-insert-date-object-in-MySQL-using-Python#:~:text=To%20insert%20a%20date%20in,datetime%20module's%20strftime%20formatting%20function.
            current_date = datetime.now()
            formatted_date = current_date.strftime('%Y-%m-%d')

            # mySQL query to insert a new order into orders with the user form input
            query = "INSERT INTO orders (order_date, total, order_status, company_id) VALUES (%s,%s,%s,%s)"
            db.execute_query(db_connection, query, (formatted_date, '0.00', 'pending', company_id))

            # redirect back to orders page
            return redirect('/orders')

# --------------------------------- EDIT ORDERS ----------------------------------

@app.route("/update_order_status/<int:id>", methods=["GET", "POST"])
def update_order_status(id):
    if request.method == "GET":
        # mySQL query to grab the info of the order with the passed id
        query = "SELECT order_id, order_date, total, order_status, companies.company_name, orders.company_id \
                 FROM orders INNER JOIN companies ON orders.company_id = companies.company_id WHERE order_id = %s" % (id)
        data = db.execute_query(db_connection, query).fetchall()

        # mySQL query to get order data using the passed id
        query2 = "SELECT * FROM orders WHERE order_id = %s" % (id)
        order_data = db.execute_query(db_connection, query2).fetchone()

        # check order status, if it's not delivered or canceled then render edit template
        if order_data['order_status'] == 'pending' or order_data['order_status'] == 'in transit':
            # render edit_orders page passing our query data to the edit_orders template
            return render_template("edit_orders.j2", data=data)

        # redirect back to orders page
        return redirect('/orders')

    # update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Update' button
        if request.form.get("Update_Order_Status"):
            # grab user form inputs
            order_id = request.form["order_id"]
            order_status = request.form["order_status"]

            # mySQL query to update the attributes of an order with the passed if and user form inputs
            query = "UPDATE orders SET orders.order_status = %s WHERE orders.order_id = %s"
            db.execute_query(db_connection, query, (order_status, order_id))

            # redirect back to orders page after we execute the update query
            return redirect('/orders')

# --------------------------------- COSTUME ORDERS ROUTE ----------------------------------

@app.route('/costume_orders', methods=["GET", "POST"])
def costume_orders():
    # get costume orders data to send back to template to display
    if request.method == "GET":
        # mySQL query to get all costume orders
        query = "SELECT costume_order_id AS ID, order_id AS 'Order ID', costumes.costume_name AS 'Costume Name', qty_ordered AS Quantity \
                 FROM costume_orders INNER JOIN costumes ON costume_orders.costume_id = costumes.costume_id \
                 ORDER BY costume_order_id ASC"
        data = db.execute_query(db_connection, query).fetchall()

        # mySQL query to get order id for dropdown menu
        query2 = "SELECT order_id FROM orders ORDER BY order_id ASC"
        order_data = db.execute_query(db_connection, query2).fetchall()

        # mySQL query to get costume id/costume name for dropdown menu
        query3 = "SELECT costume_id, costume_name FROM costumes"
        costume_data = db.execute_query(db_connection, query3).fetchall()

        # render costumes page passing costume orders/orders/costumes data to table template and dropdown menus
        return render_template("costume_orders.j2", data=data, orders=order_data, costumes=costume_data)

    # insert a costume order into costume orders entity and update corresponding row in orders entity
    if request.method == "POST":
        # fire off if user presses the 'Add Costume' button
        if request.form.get("Add_Costume"):
            # grab user form inputs
            order_id = request.form["order_id"]
            costume_id = request.form["costume_id"]
            qty_ordered = request.form["qty_ordered"]

            # mySQL query to get order data using order id
            query = "SELECT * FROM orders WHERE order_id = %s"
            order_data = db.execute_query(db_connection, query, (order_id,)).fetchone()
                
            # check order status, if it's not delivered or canceled then update costume orders and orders entities
            if order_data['order_status'] == 'pending' or order_data['order_status'] == 'in transit':
                # mySQL query to insert a new costume order into costume orders with the user form inputs
                query2 = "INSERT INTO costume_orders (order_id, costume_id, qty_ordered) VALUES (%s,%s,%s)"
                db.execute_query(db_connection, query2, (order_id, costume_id, qty_ordered))

                # mySQL query to get costume data using costume id
                query3 = "SELECT * FROM costumes WHERE costume_id = %s"
                costume_data = db.execute_query(db_connection, query3, (costume_id,)).fetchone()

                # mySQL query to update total in orders table using costume price and qty ordered
                query4 = "UPDATE orders SET total = total + (%s * %s) WHERE order_id = %s"
                db.execute_query(db_connection, query4, (qty_ordered, costume_data['price'], order_id))

            # redirect back to costume orders page
            return redirect('/costume_orders')

# --------------------------------- EDIT COSTUME ORDERS ----------------------------------

@app.route("/edit_costume_order/<int:id>", methods=["GET", "POST"])
def edit_costume_order(id):
    if request.method == "GET":
        # mySQL query to grab the info of the order with the passed id
        query = "SELECT costume_order_id, order_id, costumes.costume_name, qty_ordered, costume_orders.costume_id \
                 FROM costume_orders INNER JOIN costumes ON costume_orders.costume_id = costumes.costume_id WHERE costume_order_id = %s" % (id)
        data = db.execute_query(db_connection, query).fetchall()

        # mySQL query to get all data from costume orders where id matches the passed id
        query2 = "SELECT * FROM costume_orders WHERE costume_order_id = %s" % (id)
        costume_order_data = db.execute_query(db_connection, query2).fetchone()

        # mySQL query to get order data using order id from costume orders entity
        query3 = "SELECT * FROM orders WHERE order_id = %s"
        status_data = db.execute_query(db_connection, query3, (costume_order_data['order_id'],)).fetchone()

        # mySQL query to get costume id/costume name for dropdown menu
        query4 = "SELECT costume_id, costume_name FROM costumes"
        costume_data = db.execute_query(db_connection, query4).fetchall()

        # mySQL query to get order id for dropdown menu
        query5 = "SELECT order_id FROM orders ORDER BY order_id ASC"
        order_data = db.execute_query(db_connection, query5).fetchall()

        # check order status, if it's not delivered or canceled then render edit template using query data
        if status_data['order_status'] == 'pending' or status_data['order_status'] == 'in transit':
            return render_template("edit_costume_orders.j2", data=data, costumes=costume_data, orders=order_data)

        # redirect back to costume orders page
        return redirect('/costume_orders')

    # update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit' button
        if request.form.get("Edit_Costume_Order"):
            # grab user form inputs
            costume_order_id = request.form["costume_order_id"]
            order_id = request.form["order_id"]
            costume_id = request.form["costume_id"]
            qty_ordered = int(request.form["qty_ordered"])

            # mySQL query to get all data from costume orders where id matches the passed id
            query = "SELECT * FROM costume_orders WHERE costume_orders.costume_order_id = %s" % (id)
            costume_order_data = db.execute_query(db_connection, query).fetchone()
            original_qty = int(costume_order_data['qty_ordered'])

            # mySQL query to update the attributes of a costume order with the passed id and user form inputs
            query2 = "UPDATE costume_orders SET costume_orders.qty_ordered = %s WHERE costume_orders.costume_order_id = %s"
            db.execute_query(db_connection, query2, (qty_ordered, costume_order_id))

            # mySQL query to get costume data using costume id
            query3 = "SELECT * FROM costumes WHERE costume_id = %s"
            costume_data = db.execute_query(db_connection, query3, (costume_id,)).fetchone()

            # math to get quantity amount for updating orders entity
            new_qty = abs(original_qty - qty_ordered)

            # subtract to orders total if quantity decreased
            if qty_ordered < original_qty:
                # mySQL query to update total for orders entity using new quantity and costume price
                query4 = "UPDATE orders SET total = total - (%s * %s) WHERE order_id = %s"
                db.execute_query(db_connection, query4, (new_qty, costume_data['price'], order_id))

            # add to orders total if quantity increased
            elif qty_ordered > original_qty:
                # mySQL query to update total for orders entity using new quantity and costume price
                query4 = "UPDATE orders SET total = total + (%s * %s) WHERE order_id = %s"
                db.execute_query(db_connection, query4, (new_qty, costume_data['price'], order_id))

            # in case someone adds same quantity amount, redirect and don't update orders entity
            else:
                return redirect('/costume_orders')

            # redirect back to orders page after we execute the update query
            return redirect('/costume_orders')

# --------------------------------- DELETE COSTUME ORDERS ----------------------------------

@app.route('/delete_costume_order/<int:id>')
def delete_costume_order(id):
    # mySQL query to get costume orders data with the passed id
    query = "SELECT * FROM costume_orders WHERE costume_order_id = %s" % (id)
    costume_order_data = db.execute_query(db_connection, query).fetchone()

    # mySQL query to get orders data with order id from costume orders
    query2 = "SELECT * FROM orders WHERE order_id = %s"
    status_data = db.execute_query(db_connection, query2, (costume_order_data['order_id'],)).fetchone()

    # mySQL query to get costumes data with costume id from costume orders
    query3 = "SELECT * FROM costumes WHERE costume_id = %s"
    costume_data = db.execute_query(db_connection, query3, (costume_order_data['costume_id'],)).fetchone()

    # check order status, if it's not delivered or canceled then proceed with delete and update orders entity
    if status_data['order_status'] == 'pending' or status_data['order_status'] == 'in transit':
        # mySQL query to delete a costume order with the passed id
        query4 = "DELETE FROM costume_orders WHERE costume_order_id = '%s'"
        db.execute_query(db_connection, query4, (id,))

        # mySQL query to update orders entity 
        query5 = "UPDATE orders SET total = total - (%s * %s) WHERE order_id = %s"
        db.execute_query(db_connection, query5, (costume_order_data['qty_ordered'], costume_data['price'], costume_order_data['order_id']))

    # redirect back to costume orders page after executing the delete and update queries
    return redirect('/costume_orders')


# Listener
if __name__ == "__main__":
    app.run(port=49275, debug=True)