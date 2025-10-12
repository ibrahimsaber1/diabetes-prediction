# Diabetes Health Analytics Dashboard
## Demo


https://github.com/user-attachments/assets/47a805f5-076b-4b0c-a5c3-309a7e341990




An end-to-end, production-ready Streamlit application for analyzing diabetes health indicators and predicting diagnosed_diabetes using a trained XGBoost pipeline. The app provides:

- A polished, multi-page dashboard (Overview, Insights, Prediction)
- Clear visual analytics answering key questions about prevalence and risk factors
- An interactive prediction form that returns class and probability, with tailored guidance

## Features

- Overview
  - Dataset summary (rows, columns, diabetes prevalence, average age)
  - Schema, dtypes, and numerical statistics
  - Feature importance (from XGBoost pipeline) with top features visualization
- Insights
  - Prevalence of diabetes (bar and pie charts)
  - Diabetes vs gender and smoking status
  - BMI distribution with clinical thresholds and category risk view
  - Demographic patterns (ethnicity, education, income, employment)
  - Clinical markers (HbA1c, fasting glucose) by diabetes status
  - Correlation heatmap of key biomarkers
- Prediction
  - Loads saved pipeline models/xgb.pkl
  - Collects 25+ inputs (demographics, lifestyle, vitals, labs)
  - Predicts class and probability; shows a gauge and tailored advice
  - Friendly, supportive UX and success/education messages

## Quick Start

1) Clone and prepare environment
- Create a virtual environment and install dependencies:
```
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

2) Add required files
- Place the trained pipeline at:
```
models/xgb.pkl
```
- Place the dataset CSV at:
```
data/diabetes_health_indicators.csv
```

3) Run
- Launch the app:
```
streamlit run app.py
```
- Use the sidebar to navigate between Overview, Insights, and Prediction pages.

## Training and Saving the Model

- Train an XGBoost-based pipeline with preprocessing and SMOTE inside a cross-validated pipeline.
- Save it as follows:
```python
import joblib
joblib.dump(xgb_pipeline, "models/xgb.pkl")
```
- Ensure your pipeline’s ColumnTransformer expects the exact feature names used in the Prediction page input (see 3_Prediction.py build_input function). Align names 1-to-1 with your training schema.

## Input Schema (Prediction Page)

The prediction form collects these features (adjust according to your training schema):
- Demographics & lifestyle: age, gender, ethnicity, education_level, income_level, employment_status, smoking_status, alcohol_consumption_per_week, physical_activity_minutes_per_week, diet_score, sleep_hours_per_day, screen_time_hours_per_day
- Medical history: family_history_diabetes, hypertension_history, cardiovascular_history
- Anthropometrics & clinical: bmi, waist_to_hip_ratio, systolic_bp, diastolic_bp, heart_rate
- Lipids: cholesterol_total, hdl_cholesterol, ldl_cholesterol, triglycerides
- Glycemic markers: glucose_fasting, glucose_postprandial, insulin_level, hba1c

Important:
- Exclude leakage features if predicting diagnosed_diabetes (e.g., diabetes_stage, diabetes_risk_score), unless you designed a different target.

## Encoding & Preprocessing Recommendations

- Scale numerical features with StandardScaler
- One-hot encode nominal categories (gender, ethnicity, employment_status)
- Use OrdinalEncoder for genuine ordinal categories (education_level, income_level, smoking_status) if trained that way, otherwise one-hot is safe
- Put all preprocessing inside the Pipeline to prevent leakage
- Apply SMOTE inside the pipeline, after preprocessing and within CV folds

## Model Choices

From benchmarking:
- Top performers: LightGBM, XGBoost, RandomForest (Test F1 around 0.93 in strong setups)
- XGBoost chosen for deployment due to the balance of accuracy, stability, and feature importance interpretability
- Start hyperparameter tuning with:
  - n_estimators, max_depth, learning_rate, subsample, colsample_bytree, min_child_weight, reg_lambda, reg_alpha, tree_method='hist'

## Notes on Data Leakage

- Remove target-like columns (diabetes_stage) and risk composites (diabetes_risk_score) when predicting diagnosed_diabetes
- Ensure SMOTE and all preprocessing steps are inside the CV pipeline
- Use StratifiedKFold with shuffling for robust estimates
- Validate with DummyClassifier to sanity-check performance lift

## Requirements

See requirements.txt:
- streamlit, pandas, numpy, plotly, scikit-learn, imblearn, xgboost, joblib

## Customization

- Adjust Overview to show more metadata or profiling
- Extend Insights with additional clinical charts (e.g., LDL/HDL ratios, BP categories)
- Add download buttons for filtered data or charts
- Integrate model explainability (SHAP) if desired
- Internationalize labels and messages for different locales

## Disclaimers

- This tool is for educational and decision-support purposes; it does not replace professional medical diagnosis or treatment.
- Always consult healthcare providers for clinical decisions and personalized care plans.

## Acknowledgments

- Built with Streamlit and Plotly for fast, interactive analytics
- XGBoost pipeline for robust, high-performing tabular classification
- Inspired by standard diabetes risk indicators and clinical thresholds
