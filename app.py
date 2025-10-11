import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Diabetes Health Dashboard", page_icon="", layout="wide")

# Header: Image + Title
header_path = Path("assets/header.png")  # Place a banner image here
col_img, col_title = st.columns([1, 3])
with col_img:
    if header_path.exists():
        st.image(str(header_path), use_container_width=True)
with col_title:
    st.title(" Diabetes Health Dashboard")
    st.write("Explore the dataset, visualize key insights, and run a personalized diabetes prediction using the trained model.")

st.markdown("---")
st.header(" Dataset Overview & Feature Importance")

@st.cache_data
def load_data():
    # Ensure your CSV is located here or adjust the path
    df = pd.read_csv("data/diabetes_dataset.csv")
    return df

@st.cache_resource
def load_model():
    try:
        return joblib.load("models/xgb.pkl")
    except Exception:
        return None

df = None
try:
    df = load_data()
except Exception:
    st.warning("Could not load data from data/diabetes_dataset.csv. Overview will be limited.")

# Overview KPIs and metadata
st.subheader("Dataset Summary")
if df is not None:
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.metric("Rows", f"{len(df):,}")
    with k2: st.metric("Columns", f"{df.shape[1]}")
    with k3: 
        try:
            st.metric("Diabetes Rate", f"{(df['diagnosed_diabetes'].mean()*100):.1f}%")
        except Exception:
            st.metric("Diabetes Rate", "N/A")
    with k4: 
        try:
            st.metric("Avg Age", f"{df['age'].mean():.1f}")
        except Exception:
            st.metric("Avg Age", "N/A")

    with st.expander("Preview Data", expanded=False):
        st.dataframe(df.head(10), use_container_width=True)

    with st.expander("Schema & Dtypes", expanded=False):
        dtypes_df = pd.DataFrame({"column": df.columns, "dtype": df.dtypes.astype(str)})
        st.dataframe(dtypes_df, use_container_width=True)

    with st.expander("Basic Statistics (Numerical)", expanded=False):
        st.dataframe(df.select_dtypes(include=[np.number]).describe().T, use_container_width=True)
else:
    st.info("Upload data to data/diabetes_dataset.csv for full overview.")
