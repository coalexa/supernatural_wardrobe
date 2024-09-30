-- %s will be replaced with user input

/****************************************************************************/
---------------------------------- costumes ---------------------------------
/****************************************************************************/

-- Select all from costumes and change theme_id FK to theme_description to make it more user friendly
SELECT costume_id AS ID, costume_name AS Name, price AS 'Price Per Unit', costume_description AS Description, themes.theme_description AS Theme
FROM costumes INNER JOIN themes ON costumes.theme_id = themes.theme_id
ORDER BY costume_id ASC;

-- Select all costume ids and costume names from costumes
SELECT costume_id, costume_name FROM costumes

-- Add a costume to the costumes table
INSERT INTO costumes (costume_name, price, costume_description, theme_id)
VALUES ('%s', '%s', '%s', '%s');

-- Update costume
UPDATE costumes SET costumes.costume_name = '%s', costumes.price = '%s', costumes.costume_description = '%s', costumes.theme_id = '%s'
WHERE costume_id = '%s'

-- Delete costume
DELETE FROM costumes WHERE costume_id = '%s';

-- Search query for costume names/theme description
SELECT costume_id AS ID, costume_name AS Name, price AS Price, costume_description AS Description, themes.theme_description AS Theme
FROM costumes INNER JOIN themes ON costumes.theme_id = themes.theme_id
WHERE costume_name LIKE '%s' OR themes.theme_description LIKE '%s' ORDER BY costume_id ASC;

-- Select all from costumes where id matches user input
SELECT * FROM costumes WHERE costume_id = '%s';

/****************************************************************************/
---------------------------------- themes -----------------------------------
/****************************************************************************/

-- Select all theme ids and descriptions from themes
SELECT theme_id, theme_description FROM themes;

-- Select all themes from themes, order by ascending theme id
SELECT theme_id AS ID, theme_description AS Description FROM themes ORDER BY theme_id ASC;

-- Add a theme in the themes table
INSERT INTO themes (theme_description)
VALUES ('%s');

-- Delete theme
DELETE FROM themes WHERE theme_id = '%s';

/****************************************************************************/
---------------------------------- inventory --------------------------------
/****************************************************************************/

-- Select all inventory from inventory and change costume id FK to costume name
SELECT inventory_id AS ID, stock AS Stock, inventory_description AS Description, costumes.costume_name AS 'Costume Name'
FROM inventory LEFT JOIN costumes ON inventory.costume_id = costumes.costume_id
ORDER BY inventory_id ASC;

-- Add an item in the inventory table
INSERT INTO inventory (stock, inventory_description, costume_id)
VALUES ('%s', '%s', '%s');

-- Add an item into inventory table with null stock
INSERT INTO inventory (inventory_description, costume_id) 
VALUES ('%s','%s');

-- Update inventory table (null costume id and stock)
UPDATE inventory SET inventory.stock = NULL, inventory.inventory_description = %s, inventory.costume_id = NULL
WHERE inventory.inventory_id = '%s';

-- Update inventory table (null costume id)
UPDATE inventory SET inventory.stock = %s, inventory.inventory_description = %s, inventory.costume_id = NULL
WHERE inventory.inventory_id = '%s';
   
-- Update inventory table (null stock)
UPDATE inventory SET inventory.stock = NULL, inventory.inventory_description = '%s', inventory.costume_id = '%s'
WHERE inventory.inventory_id = '%s';

-- Update inventory table (no null inputs)
UPDATE inventory SET inventory.stock = '%s', inventory.inventory_description = '%s', inventory.costume_id = '%s' 
WHERE inventory.inventory_id = '%s';

-- Search query for inventory
SELECT inventory_id AS ID, stock AS Stock, inventory_description AS Description, costumes.costume_name AS 'Costume Name'
FROM inventory INNER JOIN costumes ON inventory.costume_id = costumes.costume_id
WHERE costumes.costume_name LIKE '%s' ORDER BY inventory_id ASC;

-- Delete inventory
DELETE FROM inventory WHERE inventory_id = '%s';

/****************************************************************************/
---------------------------------- companies --------------------------------
/****************************************************************************/

-- Select all companies in the companies table
SELECT company_id AS ID, company_name AS Name, phone AS Phone, email AS Email
FROM companies ORDER BY company_id ASC;

-- Add a company in the companies table
INSERT INTO companies (company_name, phone, email)
VALUES ('%s', '%s', '%s');

-- Update companies
UPDATE companies SET companies.company_name = '%s', companies.phone = '%s', companies.email = '%s',
WHERE company_id = '%s';

-- Search query for companies
SELECT company_id AS ID, company_name AS Name, phone AS Phone, email AS Email
FROM companies WHERE companies.company_name LIKE '%s' ORDER BY company_id ASC;

/****************************************************************************/
------------------------------------ orders ---------------------------------
/****************************************************************************/

-- Select all orders in the orders table and change company id FK to company name
SELECT order_id AS ID, order_date AS 'Order Date', total AS Total, order_status AS 'Order Status', companies.company_name AS 'Company Name'
FROM orders INNER JOIN companies ON orders.company_id = companies.company_id
ORDER BY order_id ASC;

-- Add an order in the orders table
INSERT INTO orders (order_date, total, order_status)
VALUES ('%s', '%s', '%s');

-- Update order status
UPDATE orders SET order_status = '%s'
WHERE order_id = '%s';

-- Select all from orders where id matches user input
SELECT * FROM orders WHERE order_id = '%s';

/****************************************************************************/
-------------------------------- costume orders -----------------------------
/****************************************************************************/

-- Select all costume orders from costume orders and change costume id FK to costume name
SELECT costume_order_id AS ID, order_id AS 'Order ID', costumes.costume_name AS 'Costume Name', qty_ordered AS Quantity
FROM costume_orders INNER JOIN costumes ON costume_orders.costume_id = costumes.costume_id
ORDER BY costume_order_id ASC;

-- Insert into costume orders
INSERT INTO costume_orders (order_id, costume_id, qty_ordered) 
VALUES ('%s','%s','%s');

-- Update orders table total after inserting into costume orders table
UPDATE orders SET total = total + ('%s' * '%s') WHERE order_id = '%s';
UPDATE orders SET total = total - ('%s' * '%s') WHERE order_id = '%s';

-- Update quantity in costume orders table
UPDATE costume_orders SET costume_orders.qty_ordered = '%s'
WHERE costume_orders.costume_order_id = '%s';

-- Delete from costume orders
DELETE FROM costume_orders WHERE costume_order_id = '%s'