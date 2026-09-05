DROP TABLE IF EXISTS sales;

CREATE TABLE sales (
    id              SERIAL PRIMARY KEY,
    region          VARCHAR(100),
    country         VARCHAR(100),
    item_type       VARCHAR(50),
    sales_channel   VARCHAR(20),
    order_priority  VARCHAR(5),
    order_date      DATE,
    order_id        BIGINT,
    ship_date       DATE,
    units_sold      INTEGER,
    unit_price      NUMERIC(10,2),
    unit_cost       NUMERIC(10,2),
    total_revenue   NUMERIC(14,2),
    total_cost      NUMERIC(14,2),
    total_profit    NUMERIC(14,2)
);

CREATE INDEX idx_sales_region ON sales(region);
CREATE INDEX idx_sales_country ON sales(country);
CREATE INDEX idx_sales_item_type ON sales(item_type);
CREATE INDEX idx_sales_order_date ON sales(order_date);

CREATE OR REPLACE VIEW v_sales_full AS
SELECT * FROM sales;
