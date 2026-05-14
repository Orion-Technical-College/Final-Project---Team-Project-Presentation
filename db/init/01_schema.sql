-- Canonical OTC IA510 shared dataset (batch-copy to MP2, MP3, MP4, MP7, MP8 templates).
-- Any change here must be rolled out to all embedding repos in one coordinated change-set.

CREATE TABLE CUSTOMER (
    CustomerID INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    CompanyName VARCHAR(100) NOT NULL,
    ContactName VARCHAR(100),
    Email VARCHAR(150) UNIQUE NOT NULL,
    Region VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE SUPPLIER (
    SupplierID INT PRIMARY KEY,
    SupplierName VARCHAR(100) NOT NULL,
    ContactName VARCHAR(100),
    Email VARCHAR(150),
    PaymentTerms VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE SALES_REP (
    SalesRepID INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(150),
    Region VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE WAREHOUSE (
    WarehouseID VARCHAR(10) PRIMARY KEY,
    WarehouseName VARCHAR(100),
    City VARCHAR(50),
    State VARCHAR(50),
    CapacityUnits INT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE PRODUCT (
    ProductID INT PRIMARY KEY,
    SKU VARCHAR(50) UNIQUE NOT NULL,
    ProductName VARCHAR(100) NOT NULL,
    Category VARCHAR(50),
    ListPrice NUMERIC(10, 2) NOT NULL CHECK (ListPrice >= 0),
    SupplierID INT NOT NULL,
    CONSTRAINT fk_product_supplier
        FOREIGN KEY (SupplierID)
        REFERENCES SUPPLIER(SupplierID),
        created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE ORDERS (
    OrderID INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    CustomerID INT NOT NULL,
    SalesRepID INT NOT NULL,
    WarehouseID VARCHAR(10) NOT NULL,
    OrderDate DATE DEFAULT CURRENT_DATE,
    Status VARCHAR(30) DEFAULT 'NEW',
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (CustomerID)
        REFERENCES CUSTOMER(CustomerID),
    CONSTRAINT fk_orders_salesrep
        FOREIGN KEY (SalesRepID)
        REFERENCES SALES_REP(SalesRepID),
    CONSTRAINT fk_orders_warehouse
        FOREIGN KEY (WarehouseID)
        REFERENCES WAREHOUSE(WarehouseID),
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE ORDER_LINE (
    OrderLineID INT PRIMARY KEY,
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity > 0),
    UnitPrice NUMERIC(10,2),
    CONSTRAINT fk_orderline_order
        FOREIGN KEY (OrderID)
        REFERENCES ORDERS(OrderID) ON DELETE CASCADE,
    CONSTRAINT fk_orderline_product
        FOREIGN KEY (ProductID)
        REFERENCES PRODUCT(ProductID),
        created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE INVENTORY (
    InventoryID INT PRIMARY KEY,
    ProductID INT NOT NULL,
    WarehouseID VARCHAR(10) NOT NULL,
    QuantityOnHand INT,
    ReorderPoint INT,
    LastRestockedDate DATE,
    CONSTRAINT fk_inventory_product
        FOREIGN KEY (ProductID)
        REFERENCES PRODUCT(ProductID),
    CONSTRAINT fk_inventory_warehouse
        FOREIGN KEY (WarehouseID)
        REFERENCES WAREHOUSE(WarehouseID),
    CONSTRAINT uq_inventory_product_warehouse
        UNIQUE (ProductID, WarehouseID),
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_orders_customer ON ORDERS (CustomerID);
CREATE INDEX idx_order_lines_order ON ORDER_LINE (OrderID);
CREATE INDEX idx_order_lines_product ON ORDER_LINE (ProductID);
CREATE INDEX idx_inventory_product_warehouse ON INVENTORY (ProductID, WarehouseID);
CREATE INDEX idx_product_supplier ON PRODUCT (SupplierID);