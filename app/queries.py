import pandas as pd


def build_filter(region, country, item_type, channel):
    clauses = []
    if region and region != "Todos":
        clauses.append(f"region = '{region}'")
    if country and country != "Todos":
        clauses.append(f"country = '{country}'")
    if item_type and item_type != "Todos":
        clauses.append(f"item_type = '{item_type}'")
    if channel and channel != "Todos":
        clauses.append(f"sales_channel = '{channel}'")
    return f"WHERE {' AND '.join(clauses)}" if clauses else ""


def get_regions(engine):
    return pd.read_sql("SELECT DISTINCT region FROM sales ORDER BY region", engine)["region"].tolist()


def get_countries(engine):
    return pd.read_sql("SELECT DISTINCT country FROM sales ORDER BY country", engine)["country"].tolist()


def get_item_types(engine):
    return pd.read_sql("SELECT DISTINCT item_type FROM sales ORDER BY item_type", engine)["item_type"].tolist()


def get_channels(engine):
    return pd.read_sql("SELECT DISTINCT sales_channel FROM sales ORDER BY sales_channel", engine)["sales_channel"].tolist()


def get_kpis(engine, where):
    sql = f"""
        SELECT
            COUNT(*) AS num_ordenes,
            SUM(units_sold) AS unidades_vendidas,
            SUM(total_revenue) AS ingreso_total,
            SUM(total_profit) AS ganancia_total
        FROM sales
        {where}
    """
    return pd.read_sql(sql, engine).iloc[0]


def revenue_by_region(engine, where):
    sql = f"""
        SELECT region, SUM(total_revenue) AS ingreso_total
        FROM sales
        {where}
        GROUP BY region
        ORDER BY ingreso_total DESC
    """
    return pd.read_sql(sql, engine)


def profit_by_item_type(engine, where):
    sql = f"""
        SELECT item_type, SUM(total_profit) AS ganancia_total
        FROM sales
        {where}
        GROUP BY item_type
        ORDER BY ganancia_total DESC
    """
    return pd.read_sql(sql, engine)


def orders_by_priority(engine, where):
    sql = f"""
        SELECT order_priority, COUNT(*) AS num_ordenes
        FROM sales
        {where}
        GROUP BY order_priority
    """
    return pd.read_sql(sql, engine)


def channel_split(engine, where):
    sql = f"""
        SELECT sales_channel, COUNT(*) AS num_ordenes
        FROM sales
        {where}
        GROUP BY sales_channel
    """
    return pd.read_sql(sql, engine)


def revenue_over_time(engine, where):
    sql = f"""
        SELECT DATE_TRUNC('month', order_date) AS mes, SUM(total_revenue) AS ingreso_total
        FROM sales
        {where}
        GROUP BY mes
        ORDER BY mes
    """
    return pd.read_sql(sql, engine)


def top_countries(engine, where):
    sql = f"""
        SELECT country, SUM(total_revenue) AS ingreso_total
        FROM sales
        {where}
        GROUP BY country
        ORDER BY ingreso_total DESC
        LIMIT 10
    """
    return pd.read_sql(sql, engine)
