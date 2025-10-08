# Diabetes Health Indicators Dataset

* **link >>** https://www.kaggle.com/datasets/mohankrishnathalla/diabetes-health-indicators-dataset

## 1. Overview and Purpose

This dataset contains **100,000 synthesized patient records** designed for comprehensive **diabetes risk prediction and health pattern analysis**. It is a clean, preprocessed, and ML-ready resource for various data science tasks, including:

* **Binary Classification:** Predicting the outcome of `diagnosed_diabetes`.
* **Multiclass Classification:** Determining the `diabetes_stage`.
* **Regression:** Predicting continuous clinical markers like `hba1c` or `diabetes_risk_score`.

The features incorporate **demographic, lifestyle, family history, and clinical measurements** inspired by real-world medical research, making it ideal for training robust healthcare prediction models.

---

## 2. Dataset Summary

| Metric | Value |
| :--- | :--- |
| **Source** | [Kaggle: Diabetes Health Indicators Dataset](https://www.kaggle.com/datasets/mohankrishnathalla/diabetes-health-indicators-dataset) |
| **Total Records (Rows)** | 100,000 |
| **Total Columns** | 31 |
| **Missing Values** | **None** (The dataset is complete and clean) |
| **Data Types** | `int64` (16), `float64` (8), `object` (7) |
| **Memory Usage** | ~23.7 MB |

---

## 3. Data Dictionary (Column Descriptions)

This section details all 31 columns, including their data type, description, and typical range of values.

### A. Demographic and Lifestyle Indicators

| Column | Data Type | Description | Typical Values/Range |
| :--- | :--- | :--- | :--- |
| **age** | `int64` | Age of the patient in years. | 18 – 90 |
| **gender** | `object` | Patient's recorded gender. | 'Male', 'Female', 'Other' |
| **ethnicity** | `object` | Patient's ethnic background. | 'White', 'Hispanic', 'Black', 'Asian', 'Other' |
| **education\_level** | `object` | Highest level of education completed. | 'No formal', 'Highschool', 'Graduate', 'Postgraduate' |
| **income\_level** | `object` | Patient's income category. | 'Low', 'Medium', 'High' |
| **employment\_status** | `object` | Patient's current employment type. | 'Employed', 'Unemployed', 'Retired', 'Student' |
| **smoking\_status** | `object` | Patient's smoking behavior. | 'Never', 'Former', 'Current' |
| **alcohol\_consumption\_per\_week** | `int64` | Number of standard alcoholic drinks consumed per week. | 0 – 30 |
| **physical\_activity\_minutes\_per\_week** | `int64` | Total minutes of physical activity per week. | 0 – 600 |
| **diet\_score** | `float64` | A numerical score representing diet quality (higher is healthier). | 0 – 10 |
| **sleep\_hours\_per\_day** | `float64` | Average number of sleep hours per day. | 3 – 12 |
| **screen\_time\_hours\_per\_day** | `float64` | Average hours spent on screens per day. | 0 – 12 |

### B. Medical History (Binary)

| Column | Data Type | Description | Coding |
| :--- | :--- | :--- | :--- |
| **family\_history\_diabetes** | `int64` | Indicates family history of diabetes. | **0 = No, 1 = Yes** |
| **hypertension\_history** | `int64` | Indicates history of high blood pressure. | **0 = No, 1 = Yes** |
| **cardiovascular\_history** | `int64` | Indicates history of cardiovascular disease. | **0 = No, 1 = Yes** |

### C. Clinical Measurements

| Column | Data Type | Description | Units/Range |
| :--- | :--- | :--- | :--- |
| **bmi** | `float64` | Body Mass Index. | 15 – 45 (kg/m²) |
| **waist\_to\_hip\_ratio** | `float64` | Ratio of waist circumference to hip circumference.  | 0.7 – 1.2 |
| **systolic\_bp** | `int64` | Systolic blood pressure (mmHg). | 90 – 180 (mmHg) |
| **diastolic\_bp** | `int64` | Diastolic blood pressure (mmHg). | 60 – 120 (mmHg) |
| **heart\_rate** | `int64` | Resting heart rate. | 50 – 120 (bpm) |
| **cholesterol\_total** | `int64` | Total serum cholesterol level. | 120 – 300 (mg/dL) |
| **hdl\_cholesterol** | `int64` | High-Density Lipoprotein (HDL) cholesterol level. | 20 – 100 (mg/dL) |
| **ldl\_cholesterol** | `int64` | Low-Density Lipoprotein (LDL) cholesterol level. | 50 – 200 (mg/dL) |
| **triglycerides** | `int64` | Triglyceride level. | 50 – 500 (mg/dL) |
| **glucose\_fasting** | `int64` | Fasting blood glucose level. | 70 – 250 (mg/dL) |
| **glucose\_postprandial** | `int64` | Blood glucose level measured post-meal. | 90 – 350 (mg/dL) |
| **insulin\_level** | `float64` | Blood insulin level. | 2 – 50 (µU/mL) |
| **hba1c** | `float64` | Glycated Hemoglobin A1c (average blood sugar over months). | 4 – 14 (%) |

### D. Target and Calculated Outcome Features

| Column | Data Type | Description | Purpose/Values |
| :--- | :--- | :--- | :--- |
| **diabetes\_risk\_score** | `float64` | A calculated score representing the overall diabetes risk. | 0 – 100 (For Regression) |
| **diabetes\_stage** | `object` | The patient's stage of diabetes. | 'No Diabetes', 'Pre-Diabetes', 'Type 1', 'Type 2', 'Gestational' (For Multiclass Classification) |
| **diagnosed\_diabetes** | `int64` | **Primary Target.** Indicates if the patient has been diagnosed with any form of diabetes. | **0 = No, 1 = Yes** (For Binary Classification) |

---
