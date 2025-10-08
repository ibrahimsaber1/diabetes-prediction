import streamlit as st

st.set_page_config(page_title="Diabetes Health Dashboard", page_icon="🏥", layout="wide")

st.title("🏥 Diabetes Health Dashboard")
st.write(
    "Explore the dataset, visualize key insights, and run a personalized diabetes prediction using the trained model."
)

st.markdown("### Navigation")
st.write("Use the left sidebar to switch between pages:")
st.write("- Overview: Dataset and feature importance")
st.write("- Insights: Key questions answered with plots")
st.write("- Prediction: Interactive prediction and guidance")

# st.markdown("---")
# st.success("Tip: Make sure your trained pipeline exists at models/xgb.pkl before using the Prediction page.")
