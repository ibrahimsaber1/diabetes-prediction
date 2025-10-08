import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Insights", page_icon="📊", layout="wide")
st.title("📊 Key Insights & Questions")

@st.cache_data
def load_data():
    return pd.read_csv("data/diabetes_dataset.csv")

try:
    df = load_data()
except Exception:
    st.error("Could not load data file at data/diabetes_dataset.csv")
    st.stop()

df2 = df.copy()

# Helper mappings
diab_map_short = {0: 'No', 1: 'Yes'}
diab_map_long = {0: "doesn't have diabetes", 1: "have diabetes"}
df2['diagnosed_diabetes_str'] = df2['diagnosed_diabetes'].map(diab_map_short)

st.subheader("1) How prevalent is diagnosed diabetes?")
col1, col2 = st.columns(2)
with col1:
    fig = px.histogram(
        df2, x='diagnosed_diabetes_str', color='diagnosed_diabetes_str',
        title='Prevalence of Diagnosed Diabetes',
        labels={'diagnosed_diabetes_str': 'Status', 'count': 'Count'},
        color_discrete_map={'No': 'green', 'Yes': 'red'}
    )
    fig.update_layout(bargap=0.2, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
with col2:
    df2x = df.copy()
    df2x['diagnosed_diabetes'] = df2x['diagnosed_diabetes'].map(diab_map_long)
    fig = px.pie(
        df2x, names='diagnosed_diabetes',
        title='Overall Percentage of Diagnosed Diabetes',
        color='diagnosed_diabetes',
        color_discrete_map={"doesn't have diabetes": 'green', "have diabetes": 'red'},
        hole=0.45
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("2) How does diabetes vary by gender and smoking status?")
col1, col2 = st.columns(2)
with col1:
    fig = px.histogram(
        df2, x='gender', color='diagnosed_diabetes_str',
        barmode='group',
        title='Diagnosed Diabetes per Gender',
        labels={'diagnosed_diabetes_str': 'Status', 'count': 'Count'},
        color_discrete_map={'No': 'green', 'Yes': 'red'}
    )
    # Set proper category order (capitalize/original labels needed)
    fig.update_xaxes(categoryorder='array', categoryarray=['Male', 'Female', 'Other'])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.pie(
        df, names='smoking_status',
        title='Smoking Status Distribution',
        hole=0.5
    )
    st.plotly_chart(fig, use_container_width=True)

fig = px.histogram(
    df2, x='smoking_status', color='diagnosed_diabetes_str',
    barmode='group',
    title='Diagnosed Diabetes per Smoking Status',
    labels={'diagnosed_diabetes_str': 'Status', 'count': 'Count'},
    color_discrete_map={'No': 'green', 'Yes': 'red'}
)
fig.update_xaxes(categoryorder='array', categoryarray=['Never', 'Former', 'Current'])
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("3) BMI distribution and risk bands")
fig = px.histogram(
    df, x='bmi', nbins=40,
    title='Distribution of BMI with Clinical Thresholds',
    labels={'bmi': 'BMI (kg/m²)', 'count': 'Frequency'}
)
fig.add_vline(x=25.0, line_dash='dash', line_color='gold', annotation_text='Overweight (25.0)', annotation_position='top left')
fig.add_vline(x=30.0, line_dash='dash', line_color='red', annotation_text='Obesity (30.0)', annotation_position='top left')
fig.update_layout(bargap=0.05, showlegend=False)
st.plotly_chart(fig, use_container_width=True)

def bmi_category(bmi):
    if bmi < 18.5: return 'Underweight - bmi < 18.5'
    elif bmi < 25: return 'Normal - bmi < 25'
    elif bmi < 30: return 'Overweight - bmi < 30'
    else: return 'Obese - bmi > 30'

df2['BMI Category'] = df2['bmi'].apply(bmi_category)
fig = px.histogram(
    df2, x='BMI Category', color='diagnosed_diabetes_str',
    barmode='group',
    title='Diabetes Prevalence by BMI Category',
    labels={'diagnosed_diabetes_str': 'Status', 'count': 'Number of Individuals'},
    color_discrete_map={'No': 'green', 'Yes': 'red'}
)
fig.update_xaxes(categoryorder='array', categoryarray=[
    'Underweight - bmi < 18.5', 'Normal - bmi < 25', 'Overweight - bmi < 30', 'Obese - bmi > 30'
])
fig.update_layout(bargap=0.2)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("4) Demographic patterns (ethnicity, education, income, employment)")
cols = [
    ('ethnicity', 'Diabetes Prevalence by Ethnicity', ['White', 'Hispanic', 'Black', 'Asian', 'Other']),
    ('education_level', 'Diabetes Prevalence by Education Level', ['No formal', 'Highschool', 'Graduate', 'Postgraduate']),
    ('income_level', 'Diabetes Prevalence by Income Level', ['Low', 'Lower-Middle', 'Middle', 'Upper-Middle', 'High']),
    ('employment_status', 'Diabetes Prevalence by Employment Status', ['Employed', 'Unemployed', 'Retired', 'Student'])
]
for col, title, order in cols:
    fig = px.histogram(
        df2, x=col, color='diagnosed_diabetes_str',
        barmode='group',
        title=title,
        labels={'diagnosed_diabetes_str': 'Status', 'count': 'Number of Individuals'},
        color_discrete_map={'No': 'green', 'Yes': 'red'}
    )
    fig.update_xaxes(categoryorder='array', categoryarray=order)
    fig.update_layout(bargap=0.2)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("5) Clinical markers vs diabetes")
col1, col2 = st.columns(2)
with col1:
    fig = px.box(
        df2, x='diagnosed_diabetes_str', y='hba1c', color='diagnosed_diabetes_str',
        title='HbA1c by Diabetes Status',
        labels={'diagnosed_diabetes_str': 'Status', 'hba1c': 'HbA1c (%)'},
        color_discrete_map={'No': 'green', 'Yes': 'red'}
    )
    st.plotly_chart(fig, use_container_width=True)
with col2:
    fig = px.box(
        df2, x='diagnosed_diabetes_str', y='glucose_fasting', color='diagnosed_diabetes_str',
        title='Fasting Glucose by Diabetes Status',
        labels={'diagnosed_diabetes_str': 'Status', 'glucose_fasting': 'Fasting Glucose (mg/dL)'},
        color_discrete_map={'No': 'green', 'Yes': 'red'}
    )
    st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(
    df2, x='age', y='hba1c', color='diagnosed_diabetes_str',
    title='Age vs HbA1c (by Diabetes Status)',
    labels={'age': 'Age', 'hba1c': 'HbA1c (%)', 'diagnosed_diabetes_str': 'Diabetes'},
    color_discrete_map={'No': 'green', 'Yes': 'red'},
    opacity=0.5
)
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    fig = px.histogram(
        df2, x='alcohol_consumption_per_week', color='diagnosed_diabetes_str',
        barmode='group', nbins=20,
        title='Alcohol Consumption vs Diabetes',
        labels={'alcohol_consumption_per_week': 'Drinks/week', 'count': 'Patients'},
        color_discrete_map={'No': 'green', 'Yes': 'red'}
    )
    st.plotly_chart(fig, use_container_width=True)
with col2:
    fig = px.histogram(
        df2, x='physical_activity_minutes_per_week', color='diagnosed_diabetes_str',
        nbins=40, barmode='overlay', opacity=0.7,
        title='Physical Activity vs Diabetes',
        labels={'physical_activity_minutes_per_week': 'Min/week', 'count': 'Patients'},
        color_discrete_map={'No': 'green', 'Yes': 'red'}
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("6) Correlation heatmap of key biomarkers")
core_clinical_vars = ['hba1c', 'glucose_fasting', 'insulin_level', 'bmi', 'systolic_bp', 'triglycerides']
corr_matrix = df[core_clinical_vars].corr().round(2)
fig = px.imshow(
    corr_matrix, text_auto=True, color_continuous_scale='cividis',
    title='Correlation Heatmap of Key Clinical Biomarkers'
)
fig.update_layout(xaxis_title='', yaxis_title='', xaxis_showgrid=False, yaxis_showgrid=False)
st.plotly_chart(fig, use_container_width=True)
