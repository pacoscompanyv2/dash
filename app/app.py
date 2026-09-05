import streamlit as st
import plotly.express as px
from db import get_connection
import queries as q

st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")

engine = get_connection()

st.title("Sales Analytics Dashboard")

st.sidebar.header("Filtros")
region = st.sidebar.selectbox("Región", ["Todos"] + q.get_regions(engine))
country = st.sidebar.selectbox("País", ["Todos"] + q.get_countries(engine))
item_type = st.sidebar.selectbox("Tipo de producto", ["Todos"] + q.get_item_types(engine))
channel = st.sidebar.selectbox("Canal de venta", ["Todos"] + q.get_channels(engine))

where = q.build_filter(region, country, item_type, channel)

kpis = q.get_kpis(engine, where)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Órdenes", f"{int(kpis['num_ordenes']):,}")
col2.metric("Unidades vendidas", f"{int(kpis['unidades_vendidas'] or 0):,}")
col3.metric("Ingreso total", f"${float(kpis['ingreso_total'] or 0):,.2f}")
col4.metric("Ganancia total", f"${float(kpis['ganancia_total'] or 0):,.2f}")

st.divider()

c1, c2 = st.columns(2)

with c1:
    st.subheader("Ingreso por región")
    df = q.revenue_by_region(engine, where)
    fig = px.bar(df, x="region", y="ingreso_total")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Ganancia por tipo de producto")
    df = q.profit_by_item_type(engine, where)
    fig = px.bar(df, x="item_type", y="ganancia_total")
    st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    st.subheader("Órdenes por prioridad")
    df = q.orders_by_priority(engine, where)
    fig = px.pie(df, names="order_priority", values="num_ordenes")
    st.plotly_chart(fig, use_container_width=True)

with c4:
    st.subheader("Canal de venta")
    df = q.channel_split(engine, where)
    fig = px.pie(df, names="sales_channel", values="num_ordenes")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Ingreso a través del tiempo")
df = q.revenue_over_time(engine, where)
fig = px.line(df, x="mes", y="ingreso_total")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Top 10 países por ingreso")
df = q.top_countries(engine, where)
fig = px.bar(df, x="country", y="ingreso_total")
st.plotly_chart(fig, use_container_width=True)
