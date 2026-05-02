# Transaction Fraud Detection

A data science project to predict whether a financial transaction is fraudulent using machine learning.

---

## 1.0 Business Problem

The **Blocker Fraud Company** specialises in detecting fraud in financial transactions made through mobile devices. The company offers a service called **"Blocker Fraud"** which guarantees the blocking of fraudulent transactions.

The business model is performance-based — the company is paid only when it correctly identifies fraud. To acquire customers quickly, the company has adopted an aggressive strategy:

| Outcome | Revenue / Cost |
|---|---|
| Transaction correctly detected as **fraud** | Company receives **25%** of the transaction value |
| Transaction flagged as fraud but is **legitimate** | Company receives **5%** of the transaction value |
| Transaction flagged as **legitimate** but is actually **fraud** | Company **returns 100%** of the value to the customer |

This means the company's profitability depends entirely on the precision and recall of its fraud detection model. A highly accurate model generates strong revenue; a poor model results in significant losses from reimbursements.

---

## 2.0 Business Assumptions

- Fraud prevention is the implementation of a strategy to detect fraudulent transactions and prevent financial damage to both customers and the institution.
- Financial fraud occurs through both digital and physical channels, and investment in security continues to grow.
- The dataset covers **1,000,000 transactions** from **January 2022 to December 2024** across 50,000 unique accounts.
- The fraud rate is **1.71%** — a heavily imbalanced classification problem.
- Model evaluation prioritises **PR-AUC** (Precision-Recall AUC) over ROC-AUC, as PR-AUC is more informative under class imbalance.

---

## 3.0 Solution Strategy

The solution is a complete data science pipeline across five notebooks:

**Step 01 — Exploratory Data Analysis (`01_EDA.ipynb`)**
Load and inspect all five raw data sources. Analyse class distribution, temporal trends, transaction amounts, fraud rates by device type and merchant category, behavioural feature distributions, and fraud ring network structure.

**Step 02 — Feature Engineering (`02_Feature Engineering.ipynb`)**
Engineer new features including `log_amount`, `is_night`, `account_age_bucket`, `is_unusual_spend`, `is_high_velocity`, and `txn_to_limit_ratio`. Merge account profile dimensions. Produce two processed datasets: one for linear models (one-hot encoded, 40 features) and one for tree models (label-encoded, 28 features).

**Step 03 — Logistic Regression Baseline (`03_Logistic Regression Baseline.ipynb`)**
Train a regularised logistic regression model with `class_weight="balanced"` to handle the fraud imbalance. Establish a PR-AUC baseline and identify the most predictive features via model coefficients.

**Step 04 — Tree Models (`04_Tree_Model.ipynb`)**
Train XGBoost and LightGBM on the label-encoded dataset. Handle imbalance via `scale_pos_weight` and `is_unbalance=True` respectively. Use PR-AUC-guided early stopping. Tune classification threshold to maximise F1.

**Step 05 — Model Comparison (`05_Model_Comparison.ipynb`)**
Load saved predictions from all three models. Compare PR-AUC, ROC-AUC, classification reports at optimal threshold, precision-recall curves, and confusion matrices in one consolidated view.

---

## 4.0 Top 3 Data Insights

**Insight 1 — Fraud rate spikes significantly during night hours (midnight to 5 AM)**
While transaction volume is lowest overnight, the fraud rate is disproportionately high during these hours. This pattern motivated the `is_night` engineered feature.

**Insight 2 — IP risk score is the strongest individual predictor of fraud**
Among all features, `ip_risk_score` had the highest positive coefficient in the logistic regression model (2.108), far ahead of `card_present` (1.361) and `log_amount` (1.235). High-risk IP addresses are a reliable signal.

**Insight 3 — A small subset of accounts drives the majority of fraud**
The Pareto analysis of account profiles shows that fraud is highly concentrated — a minority of accounts are responsible for a disproportionate share of all fraudulent transactions, suggesting account-level risk profiling is a valuable detection layer.

---

## 5.0 Machine Learning Applied

All models were trained on data from **2022–2023** and evaluated on **2024** (temporal split to prevent data leakage).

| Model | PR-AUC | ROC-AUC |
|---|---|---|
| Logistic Regression (baseline) | 0.7064 | 0.9741 |
| XGBoost | 0.8257 | 0.9897 |
| LightGBM | **0.8274** | 0.9895 |

Tree models improved PR-AUC by **+0.12** over the logistic regression baseline by capturing non-linear feature interactions.

---

## 6.0 Machine Learning Performance

The best model was **LightGBM**, evaluated at its optimal classification threshold (0.962):

| Metric | Legitimate | Fraud |
|---|---|---|
| Precision | 0.99 | **0.83** |
| Recall | 1.00 | **0.70** |
| F1-score | 1.00 | **0.76** |

At this threshold, the model correctly identifies **70% of all fraud cases** with **83% precision** — meaning 83 out of every 100 flagged transactions are genuine fraud.

---

## 7.0 Dataset

| File | Rows | Description |
|---|---|---|
| `transactions.csv` | 1,000,000 | Core transaction records with labels |
| `account_profiles.csv` | 50,000 | Account-level risk and behavioural stats |
| `fraud_patterns.csv` | 7 | Descriptive stats per fraud pattern type |
| `network_edges.csv` | 7,411 | Account-to-account connection graph (fraud rings) |
| `time_series_stats.csv` | 26,280 | Hourly aggregated transaction and fraud stats |

---

## 8.0 Project Structure

```
Transaction Fraud Detection Project/
├── Data/
│   ├── Raw/                   # Original source files
│   └── Processed/             # Engineered datasets, train/test splits, saved predictions
├── Notebooks/
│   ├── 01_EDA.ipynb
│   ├── 02_Feature Engineering.ipynb
│   ├── 03_Logistic Regression Baseline.ipynb
│   ├── 04_Tree_Model.ipynb
│   └── 05_Model_Comparison.ipynb
```

---

## 9.0 Conclusions

The heavily imbalanced nature of the dataset (1.71% fraud rate) required careful handling throughout — from class weighting in model training to using PR-AUC as the primary metric and tuning the classification threshold rather than relying on the default 0.5.

LightGBM achieved the best PR-AUC of **0.8274**, representing a **17% relative improvement** over the logistic regression baseline. The model is well-suited for deployment in the Blocker Fraud business model, where high precision directly reduces the cost of false positives and strong recall maximises revenue from correctly detected fraud.

---

## 10.0 Next Steps

- Calculate business impact (revenue, loss, net profit) using actual transaction amounts from the test set.
- Apply oversampling (SMOTE) or undersampling techniques and measure effect on PR-AUC.
- Incorporate network features from `network_edges.csv` (fraud ring membership, connection count) into the model.
- Perform hyperparameter tuning on LightGBM using Optuna or Bayesian optimisation.
- Build a deployment API (FastAPI or Flask) to serve real-time predictions.
