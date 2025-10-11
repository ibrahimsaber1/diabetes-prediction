import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Insights", page_icon="", layout="wide")
st.title(" Key Insights & Questions")

@st.cache_data
def load_data():
    return pd.read_csv("data/diabetes_dataset.csv")

try:
    df = load_data()
except Exception:
    st.error("Could not load data file at data/diabetes_dataset.csv")
    st.stop()

df2 = df.copy()
df2['diagnosed_diabetes_str'] = df2['diagnosed_diabetes'].map({0: 'No', 1: 'Yes'})

tab_demo, tab_history, tab_clinical = st.tabs([
    " Demographics & Lifestyle",
    " Medical History ",
    " Clinical Measurements"
])

# ============== DEMOGRAPHICS & LIFESTYLE ==============
with tab_demo:
    st.subheader("Prevalence and Demographic Patterns")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(
            df2, x='diagnosed_diabetes_str', color='diagnosed_diabetes_str',
            title='Prevalence of Diagnosed Diabetes',
            labels={'diagnosed_diabetes_str': 'Status', 'count': 'Count'},
            color_discrete_map={'No': 'green', 'Yes': 'red'}
        )
        fig.update_layout(bargap=0.2, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        pie_df = df.copy()
        pie_df['diagnosed_diabetes'] = pie_df['diagnosed_diabetes'].map({
            0: "doesn't have diabetes", 1: "have diabetes"
        })
        fig = px.pie(
            pie_df, names='diagnosed_diabetes',
            title='Overall Percentage of Diagnosed Diabetes',
            color='diagnosed_diabetes',
            color_discrete_map={"doesn't have diabetes": 'green', "have diabetes": 'red'},
            hole=0.45
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Gender & Smoking")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(
            df2, x='gender', color='diagnosed_diabetes_str',
            barmode='group',
            title='Diagnosed Diabetes per Gender',
            labels={'diagnosed_diabetes_str': 'Status', 'count': 'Count'},
            color_discrete_map={'No': 'green', 'Yes': 'red'}
        )
        fig.update_xaxes(categoryorder='array', categoryarray=['Male', 'Female', 'Other'])
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.pie(df, names='smoking_status', title='Smoking Status Distribution', hole=0.5)
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

    st.subheader("BMI and Lifestyle Indicators")
    # BMI distribution with thresholds
    fig = px.histogram(
        df, x='bmi', nbins=40,
        title='Distribution of BMI with Clinical Thresholds',
        labels={'bmi': 'BMI (kg/m²)', 'count': 'Frequency'}
    )
    fig.add_vline(x=25.0, line_dash='dash', line_color='gold', annotation_text='Overweight (25.0)')
    fig.add_vline(x=30.0, line_dash='dash', line_color='red', annotation_text='Obesity (30.0)')
    fig.update_layout(bargap=0.05, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # BMI categories prevalence
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
        labels={'diagnosed_diabetes_str': 'Status', 'count': 'Individuals'},
        color_discrete_map={'No': 'green', 'Yes': 'red'}
    )
    fig.update_xaxes(categoryorder='array', categoryarray=[
        'Underweight - bmi < 18.5', 'Normal - bmi < 25', 'Overweight - bmi < 30', 'Obese - bmi > 30'
    ])
    st.plotly_chart(fig, use_container_width=True)

    # Alcohol and Physical Activity vs Diabetes
    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(
            df2, x='alcohol_consumption_per_week', color='diagnosed_diabetes_str',
            barmode='group', nbins=20,
            title='Alcohol Consumption vs Diabetes',
            labels={'alcohol_consumption_per_week': 'Drinks/week', 'count': 'Patients'},
            color_discrete_map={'No': 'green', 'Yes': 'red'}
        )
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.histogram(
            df2, x='physical_activity_minutes_per_week', color='diagnosed_diabetes_str',
            nbins=40, barmode='overlay', opacity=0.7,
            title='Physical Activity vs Diabetes',
            labels={'physical_activity_minutes_per_week': 'Min/week', 'count': 'Patients'},
            color_discrete_map={'No': 'green', 'Yes': 'red'}
        )
        st.plotly_chart(fig, use_container_width=True)
# People counts lines: Drinks/week (left) and Physical Activity (right)
    st.subheader("Population Distributions (Counts)")
    c1, c2 = st.columns(2)

    with c1:
        # Alcohol: people count vs drinks/week
        alcohol_counts = (
            df2['alcohol_consumption_per_week']
            .value_counts(dropna=False)
            .sort_index()
            .reset_index()
        )
        alcohol_counts.columns = ['drinks_per_week', 'n_people']
        alcohol_counts['drinks_per_week'] = pd.to_numeric(alcohol_counts['drinks_per_week'], errors='coerce')
        alcohol_counts = alcohol_counts.dropna(subset=['drinks_per_week'])

        fig = px.line(
            alcohol_counts,
            x='drinks_per_week',
            y='n_people',
            title='People vs Drinks per Week',
            labels={'drinks_per_week': 'Drinks/week', 'n_people': 'Number of People'}
        )
        fig.update_traces(mode='lines+markers')
        fig.update_layout(xaxis=dict(dtick=1))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        # Physical Activity: people count vs minutes/week
        activity_counts = (
            df2['physical_activity_minutes_per_week']
            .value_counts(dropna=False)
            .sort_index()
            .reset_index()
        )
        activity_counts.columns = ['minutes_per_week', 'n_people']
        activity_counts['minutes_per_week'] = pd.to_numeric(activity_counts['minutes_per_week'], errors='coerce')
        activity_counts = activity_counts.dropna(subset=['minutes_per_week'])

        # If the minute range is large and too spiky, you can bin for readability:
        # bins = list(range(0, 1001, 50)) + [df2['physical_activity_minutes_per_week'].max()]
        # activity_counts = (
        #     df2.assign(_bin=pd.cut(df2['physical_activity_minutes_per_week'], bins=bins, right=False))
        #       .groupby('_bin', as_index=False)
        #       .size()
        #       .rename(columns={'_bin': 'minutes_bin', 'size': 'n_people'})
        # )

        fig = px.line(
            activity_counts,
            x='minutes_per_week',
            y='n_people',
            title='People vs Physical Activity (min/week)',
            labels={'minutes_per_week': 'Minutes/week', 'n_people': 'Number of People'}
        )
        fig.update_traces(mode='lines+markers')
        # Optional: set tick spacing if range is big (e.g., every 50 or 100 minutes)
        # fig.update_layout(xaxis=dict(dtick=50))
        st.plotly_chart(fig, use_container_width=True)

    # New: Sleep & Screen Time distributions by diabetes
    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(
            df2, x='sleep_hours_per_day', color='diagnosed_diabetes_str',
            barmode='overlay', nbins=24, opacity=0.7,
            title='Sleep Hours per Day by Diabetes Status',
            labels={'sleep_hours_per_day': 'Hours/day', 'count': 'Patients'},
            color_discrete_map={'No': 'green', 'Yes': 'red'}
        )
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.histogram(
            df2, x='screen_time_hours_per_day', color='diagnosed_diabetes_str',
            barmode='overlay', nbins=24, opacity=0.7,
            title='Screen Time per Day by Diabetes Status',
            labels={'screen_time_hours_per_day': 'Hours/day', 'count': 'Patients'},
            color_discrete_map={'No': 'green', 'Yes': 'red'}
        )
        st.plotly_chart(fig, use_container_width=True)

    # Demographic: Ethnicity, Education, Income, Employment
    st.subheader("Demographic Patterns")
    config = [
        ('ethnicity', 'Diabetes Prevalence by Ethnicity', ['White', 'Hispanic', 'Black', 'Asian', 'Other']),
        ('education_level', 'Diabetes Prevalence by Education Level', ['No formal', 'Highschool', 'Graduate', 'Postgraduate']),
        ('income_level', 'Diabetes Prevalence by Income Level', ['Low', 'Lower-Middle', 'Middle', 'Upper-Middle', 'High']),
        ('employment_status', 'Diabetes Prevalence by Employment Status', ['Employed', 'Unemployed', 'Retired', 'Student'])
    ]
    for col, title, order in config:
        fig = px.histogram(
            df2, x=col, color='diagnosed_diabetes_str',
            barmode='group',
            title=title,
            labels={'diagnosed_diabetes_str': 'Status', 'count': 'Individuals'},
            color_discrete_map={'No': 'green', 'Yes': 'red'}
        )
        fig.update_xaxes(categoryorder='array', categoryarray=order)
        st.plotly_chart(fig, use_container_width=True)

# ============== MEDICAL HISTORY  ==============
with tab_history:
    st.subheader("Family & Comorbidities")
    # Family history, Hypertension, Cardiovascular — prevalence by diabetes
    for col in ['family_history_diabetes', 'hypertension_history', 'cardiovascular_history']:
        fig = px.histogram(
            df2, x=col, color='diagnosed_diabetes_str',
            barmode='group', category_orders={col: [0, 1]},
            title=f'{col.replace("_", " ").title()} vs Diabetes Diagnosis',
            labels={col: f'{col} (0=No, 1=Yes)', 'diagnosed_diabetes_str': 'Status', 'count': 'Patients'},
            color_discrete_map={'No': 'green', 'Yes': 'red'}
        )
        st.plotly_chart(fig, use_container_width=True)


# ============== CLINICAL MEASUREMENTS ==============
with tab_clinical:
    st.subheader("Glucose & HbA1c")
    c1, c2 = st.columns(2)
    with c1:
        fig = px.box(
            df2, x='diagnosed_diabetes_str', y='hba1c', color='diagnosed_diabetes_str',
            title='HbA1c by Diabetes Status',
            labels={'diagnosed_diabetes_str': 'Status', 'hba1c': 'HbA1c (%)'},
            color_discrete_map={'No': 'green', 'Yes': 'red'}
        )
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.box(
            df2, x='diagnosed_diabetes_str', y='glucose_fasting', color='diagnosed_diabetes_str',
            title='Fasting Glucose by Diabetes Status',
            labels={'diagnosed_diabetes_str': 'Status', 'glucose_fasting': 'Fasting Glucose (mg/dL)'},
            color_discrete_map={'No': 'green', 'Yes': 'red'}
        )
        st.plotly_chart(fig, use_container_width=True)

    # Age vs HbA1c scatter
    fig = px.scatter(
        df2, x='age', y='hba1c', color='diagnosed_diabetes_str',
        title='Age vs HbA1c (by Diabetes Status)',
        labels={'age': 'Age', 'hba1c': 'HbA1c (%)', 'diagnosed_diabetes_str': 'Diabetes'},
        color_discrete_map={'No': 'green', 'Yes': 'red'},
        opacity=0.5
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Other Clinical Indicators")
    # Vitals/lipids distributions by diabetes
    grid = [
        ('systolic_bp', 'Systolic BP'),
        ('diastolic_bp', 'Diastolic BP'),
        ('bmi', 'BMI'),
        ('cholesterol_total', 'Total Cholesterol'),
        ('hdl_cholesterol', 'HDL'),
        ('ldl_cholesterol', 'LDL'),
        ('triglycerides', 'Triglycerides'),
        ('insulin_level', 'Insulin')
    ]
    for i in range(0, len(grid), 2):
        c1, c2 = st.columns(2)
        for col, label in grid[i:i+2]:
            with (c1 if col == grid[i][0] else c2):
                fig = px.histogram(
                    df2, x=col, color='diagnosed_diabetes_str',
                    barmode='overlay', opacity=0.6, nbins=40,
                    title=f'{label} Distribution by Diabetes Status',
                    labels={col: label, 'diagnosed_diabetes_str': 'Status'},
                    color_discrete_map={'No': 'green', 'Yes': 'red'}
                )
                st.plotly_chart(fig, use_container_width=True)

    st.subheader("Correlation heatmap of key biomarkers")
    core_clinical_vars = ['hba1c', 'glucose_fasting', 'insulin_level', 'bmi', 'systolic_bp', 'triglycerides']
    corr_matrix = df[core_clinical_vars].corr().round(2)
    fig = px.imshow(
        corr_matrix, text_auto=True, color_continuous_scale='cividis',
        title='Correlation Heatmap of Key Clinical Biomarkers'
    )
    fig.update_layout(xaxis_title='', yaxis_title='', xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig, use_container_width=True)
