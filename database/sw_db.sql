SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

-- Drop all tables if they exist

DROP TABLE IF EXISTS costumes;
DROP TABLE IF EXISTS themes;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS costume_orders;

-- Table structure for costumes table

CREATE TABLE costumes
(
    costume_id int AUTO_INCREMENT NOT NULL,
    costume_name varchar(150) NOT NULL,
    price decimal(18,2) NOT NULL,
    costume_description varchar(750) NOT NULL,
    theme_id int NOT NULL, 
    PRIMARY KEY (costume_id),
    FOREIGN KEY (theme_id) REFERENCES themes(theme_id) ON DELETE RESTRICT
);

-- Table structure for themes table

CREATE TABLE themes
(
	theme_id int AUTO_INCREMENT NOT NULL,
    theme_description varchar(150) NOT NULL,
    PRIMARY KEY (theme_id)
);

-- Table structure for inventory table

CREATE TABLE inventory
(
	inventory_id int AUTO_INCREMENT NOT NULL,
    stock int DEFAULT NULL,
    inventory_description varchar(150) NOT NULL,
    costume_id int DEFAULT NULL,
    PRIMARY KEY (inventory_id),
    FOREIGN KEY (costume_id) REFERENCES costumes(costume_id) ON DELETE CASCADE
);

-- Table structure for companies table

CREATE TABLE companies
(
	company_id int AUTO_INCREMENT NOT NULL,
    company_name varchar(150) NOT NULL,
    phone varchar(20) NOT NULL,
    email varchar(50) NOT NULL,
    PRIMARY KEY (company_id)
);

-- Table structure for orders table

CREATE TABLE orders
(
	order_id int AUTO_INCREMENT NOT NULL,
    order_date date NOT NULL,
    total decimal(18,2) NOT NULL,
    order_status varchar(50) NOT NULL,
    company_id int NOT NULL,
    PRIMARY KEY (order_id),
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

-- Table structure for costume_orders intersection table

CREATE TABLE costume_orders
(
	costume_order_id int AUTO_INCREMENT NOT NULL,
    order_id int NOT NULL,
	costume_id int NOT NULL,
    qty_ordered int NOT NULL,
    PRIMARY KEY (costume_order_id),
	FOREIGN KEY (costume_id) REFERENCES costumes(costume_id) ON DELETE RESTRICT,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE
);

-- Data for costumes table

INSERT INTO `costumes` (`costume_name`, `price`, `costume_description`, `theme_id`) VALUES
('Spooky Vampire', '450.00', 'Thirsty for some blood? This adult vampire costume...', 1),
('Dark Witch ', '500.00', 'This beautiful celestial witch costume will have you casting spells...', 2),
('Dark Knight', '600.00', 'Protect Gotham City from the forces of Evil and the deadly Joker...', 3);

-- Data for themes table
 
INSERT INTO `themes` (`theme_description`) VALUES
('Vampire'),
('Witch'),
('Superhero');

-- Data for inventory table

INSERT INTO `inventory` (`stock`, `inventory_description`, `costume_id`) VALUES
(500, 'aisle 1', 1),
(1000, 'aisle 2', 2),
(1200, 'aisle 3', 3);

-- Data for companies table

INSERT INTO `companies` (`company_name`, `phone`, `email`) VALUES
('Halloween 4 U', '123-467-1224', 'halloweenforyou@gmail.com'),
('Buy Costumes', '123-789-4556', 'buycostumes@gmail.com'),
('Halloween 2 Go', '123-777-8889', 'halloween2go@gmail.com');

-- Data for orders table

INSERT INTO `orders` (`order_date`, `total`, `order_status`, `company_id`) VALUES
('2020-10-20', '27500.00', 'delivered', 1),
('2022-10-03', '11250.00', 'in transit', 2),
('2022-05-03', '34200.00', 'in transit', 1);

-- Data for costume_orders intersection table

INSERT INTO `costume_orders` (`order_id`, `costume_id`, `qty_ordered`) VALUES
(2, 1, 25),
(3, 1, 36),
(1, 2, 55),
(3, 3, 30);

SET FOREIGN_KEY_CHECKS=1;
COMMIT;