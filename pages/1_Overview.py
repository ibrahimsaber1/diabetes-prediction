import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Overview", page_icon="📘", layout="wide")
st.title("📘 Dataset Overview & Feature Importance")

@st.cache_data
def load_data():
    # Replace with your path
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

# Overview
st.subheader("Dataset Summary")
if df is not None:
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Rows", f"{len(df):,}")
    with col2: st.metric("Columns", f"{df.shape[1]}")
    with col3: st.metric("Diabetes Rate", f"{(df['diagnosed_diabetes'].mean()*100):.1f}%")
    with col4: st.metric("Avg Age", f"{df['age'].mean():.1f}")

    with st.expander("Preview Data", expanded=False):
        st.dataframe(df.head(10), use_container_width=True)

    with st.expander("Schema & Dtypes", expanded=False):
        dtypes_df = pd.DataFrame({"column": df.columns, "dtype": df.dtypes.astype(str)})
        st.dataframe(dtypes_df, use_container_width=True)

    with st.expander("Basic Statistics (Numerical)", expanded=False):
        st.dataframe(df.select_dtypes(include=[np.number]).describe().T, use_container_width=True)
else:
    st.info("Upload data to data/diabetes_dataset.csv for full overview.")

st.markdown("---")
st.subheader("Feature Importance (from trained XGBoost pipeline)")

model = load_model()
if model is None:
    st.warning("No model found at models/xgb.pkl. Train and save your pipeline to show importances.")
else:
    # Try extracting importances robustly
    clf = None
    try:
        # imblearn pipeline: named_steps might be different (e.g., 'Model' or 'clf')
        clf = model.named_steps.get('Model') or model.named_steps.get('clf') or model.named_steps.get('classifier')
    except Exception:
        clf = None

    if clf is not None and hasattr(clf, "feature_importances_"):
        # Try to get feature names after preprocessing
        try:
            pre = model.named_steps.get('Preprocessing') or model.named_steps.get('preprocessor')
            if hasattr(pre, 'get_feature_names_out'):
                feature_names = pre.get_feature_names_out()
            else:
                feature_names = [f"f{i}" for i in range(len(clf.feature_importances_))]
        except Exception:
            feature_names = [f"f{i}" for i in range(len(clf.feature_importances_))]

        importances = pd.DataFrame({
            "feature": feature_names,
            "importance": clf.feature_importances_
        }).sort_values("importance", ascending=False).head(25)

        fig = px.bar(importances, x="importance", y="feature", orientation="h",
                     title="Top 25 Features by Importance")
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Model does not expose feature_importances_ (or step name mismatch).")
        st.caption("Ensure the classifier is tree-based (e.g., XGBClassifier) and is accessible as 'Model' in the pipeline.")
