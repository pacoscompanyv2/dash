import os
import streamlit as st
from sqlalchemy import create_engine


def get_engine():
    host = os.getenv("DB_HOST") or st.secrets.get("DB_HOST", "db")
    port = os.getenv("DB_PORT") or st.secrets.get("DB_PORT", "5432")
    name = os.getenv("DB_NAME") or st.secrets.get("DB_NAME", "salesdb")
    user = os.getenv("DB_USER") or st.secrets.get("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD") or st.secrets.get("DB_PASSWORD", "postgres")

    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"
    return create_engine(url)


@st.cache_resource
def get_connection():
    return get_engine()
