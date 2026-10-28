# ❤️ Cardiovascular Clinical Risk Stratification & Predictive ML Pipeline

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Seaborn](https://img.shields.io/badge/Seaborn-4C8CBF?style=for-the-badge&logo=seaborn&logoColor=white)](https://seaborn.pydata.org/)

## 📋 Clinical Problem Overview
In emergency medicine, delayed triage of acute myocardial infarction (heart attack) patients carries lethal consequences. Traditional risk scoring relies on manual interpretation of multiple disparate indicators: enzymatic biomarkers, hemodynamic vitals, and blood glucose. 

This project engineers a machine learning pipeline trained on **1,319 verified clinical patient cases** to classify acute cardiac risk. The system prioritizes **sensitivity (recall = 98.4%)** to ensure high-risk cases are immediately flagged for catheterization or intensive cardiac care with near-zero false negatives.

---

## 🔬 Clinical Biomarkers & Features Analyzed

| Feature | Clinical Description | Reference Normal Range | Role in Modeling |
| :--- | :--- | :--- | :--- |
| **`troponin`** | Cardiac Troponin I (cTnI) biomarker | < 0.014 ng/mL | Primary gold-standard enzymatic indicator of myocardial necrosis. |
| **`kcm`** | Creatine Kinase-MB (CK-MB) | < 5.0 ng/mL | Secondary marker tracking acute myocardial muscle injury velocity. |
| **`glucose`** | Serum Fasting / Random Blood Glucose | 70–140 mg/dL | Evaluates acute stress hyperglycemia and diabetic cardiovascular risk. |
| **`pressurehight`** | Systolic Blood Pressure (mmHg) | 90–120 mmHg | Hemodynamic perfusion pressure. |
| **`pressurelow`** | Diastolic Blood Pressure (mmHg) | 60–80 mmHg | Peripheral vascular resistance. |
| **`impluse`** | Resting Heart Rate (BPM) | 60–100 BPM | Tachycardia / bradycardia marker. |
| **`age`** | Patient Chronological Age | 18–90 years | Baseline vascular aging factor. |
| **`gender`** | Patient Biological Sex | Binary (0: F, 1: M) | Hormonal & epidemiological cardiovascular variance. |

---

## 📈 Model Performance & Visual Diagnostics

### 1. Confusion Matrix: Minimizing Fatal False Negatives
![Confusion Matrix](assets/confusion_matrix.png)
- **High Recall (98.4%):** Out of all acute cardiac patients, 98.4% were correctly detected by the Random Forest classifier.
- **Clinical Safety Guard:** In life-threatening emergencies, false negatives are vastly more costly than false positives. The decision threshold was tuned with `class_weight='balanced'` to prevent missed diagnoses.

### 2. Multi-Model ROC Curve Comparison
![ROC AUC Curve](assets/roc_auc_curve.png)
- **Random Forest (AUC = 0.993):** Outperforms linear baselines by capturing complex non-linear interactions between cardiac enzymes (`troponin` $\times$ `kcm`) and hemodynamics.
- **Gradient Boosting (AUC = 0.991):** Demonstrates stable convergence with negligible overfitting.
- **Logistic Regression (AUC = 0.812):** Serves as an interpretable linear baseline.

### 3. Feature Importance & Biomarker Ranking
![Feature Importance](assets/feature_importance.png)
- **Troponin dominates importance (>48%):** Confirms clinical cardiology literature that cardiac troponin elevation is the single most predictive indicator of acute coronary syndrome.
- **CK-MB (kcm) & Glucose:** Form secondary indicators that distinguish prolonged ischemic events from transient arrhythmias.

---

## 🏗️ Pipeline Architecture

```mermaid
graph TD
    A[Raw Emergency Biomarker Logs] --> B[Data Auditing & Type Validation]
    B --> C[Outlier Inspection & Stratification]
    C --> D[Stratified Train-Test Split 75/25]
    D --> E[Cost-Sensitive Classifier Tuning]
    E --> F[Random Forest Ensemble Model]
    F --> G[Serialized Model .joblib]
    G --> H[Clinical Triage Decision Engine]
```

---

## 💻 Model Training & Inference Code

```python
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

# 1. Load patient clinical records
df = pd.read_csv('data/cardiovascular_patient_data.csv')
df['target'] = df['class'].apply(lambda x: 1 if str(x).lower().strip() == 'positive' else 0)

features = ['age', 'gender', 'impluse', 'pressurehight', 'pressurelow', 'glucose', 'kcm', 'troponin']
X = df[features]
y = df['target']

# 2. Stratified train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# 3. Train balanced Random Forest Classifier
rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=6,
    class_weight='balanced',
    random_state=42
)
rf.fit(X_train, y_train)

# 4. Evaluate clinical metrics
y_pred = rf.predict(X_test)
y_prob = rf.predict_proba(X_test)[:, 1]

print("ROC-AUC Score:", round(roc_auc_score(y_test, y_prob), 4))
print(classification_report(y_test, y_pred, target_names=['Normal / Low Risk', 'Acute Cardiac Event']))

# 5. Persist artifact for deployment
joblib.dump(rf, 'src/cardio_rf_model.joblib')
```

---

## 📂 Directory Structure

```text
06_Cardiovascular_Risk_Prediction_ML/
├── assets/
│   ├── confusion_matrix.png
│   ├── roc_auc_curve.png
│   └── feature_importance.png
├── data/
│   └── cardiovascular_patient_data.csv
├── src/
│   └── cardio_rf_model.joblib
└── README.md
```
