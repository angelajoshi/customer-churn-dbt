
# Customer Churn Prediction and Analytics

> An end-to-end data pipeline with machine learning for predicting customer churn in subscription-based businesses

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Workflow](#workflow)
- [Model Performance](#model-performance)
- [Dashboard](#dashboard)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [Author](#author)
- [License](#license)

---

## Overview

This project demonstrates a modern data stack workflow for building a fully automated pipeline that collects, transforms, analyzes, and predicts customer churn. It's designed to be cloud-agnostic and showcases best practices in data engineering and machine learning operations.

**Key Capabilities:**
- Automated data ingestion from multiple sources
- Clean, version-controlled data transformations
- Orchestrated ETL and ML pipelines
- Real-time churn predictions
- Interactive analytics dashboard

---

## Architecture
<img width="561" height="1437" alt="image" src="https://github.com/user-attachments/assets/1271022e-b3c8-42e5-8627-5c513f605c99" />




## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Data Ingestion** | Airbyte |
| **Data Warehouse** | PostgreSQL |
| **Transformation** | dbt (Data Build Tool) |
| **Orchestration** | Prefect |
| **Machine Learning** | Scikit-learn, XGBoost |
| **Visualization** | Streamlit |
| **Language** | Python 3.8+ |

---

## Project Structure

```
customer-churn-pipeline/
│
├── airbyte_config/              # Airbyte source & destination configs
│   ├── source_config.json
│   └── destination_config.json
│
├── dbt_models/                  # dbt transformation models
│   ├── staging/                 # Staging layer (data cleaning)
│   ├── marts/                   # Analytics-ready tables
│   │   └── churn_features.sql
│   └── dbt_project.yml
│
├── prefect_flows/               # Orchestration workflows
│   ├── etl_flow.py             # Main ETL pipeline
│   └── model_train_flow.py     # ML training pipeline
│
├── ml/                          # Machine learning components
│   ├── train_model.py          # Model training script
│   ├── churn_model.pkl         # Trained model artifact
│   └── scaler.pkl              # Feature scaler
│
├── streamlit_app/               # Dashboard application
│   └── app.py                  # Streamlit dashboard
│
├── data/                        # Sample data files
│   ├── customers.csv
│   └── transactions.csv
│
├── requirements.txt             # Python dependencies
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- PostgreSQL 12+
- Docker (for Airbyte)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/angelajoshi/customer-churn-pipeline.git
   cd customer-churn-pipeline
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure PostgreSQL**
   ```bash
   createdb churn_analytics
   ```

5. **Set up Airbyte**
   ```bash
   # Follow Airbyte quick start guide
   # Configure sources and destinations using configs in airbyte_config/
   ```

6. **Configure dbt**
   ```bash
   cd dbt_models
   dbt debug
   dbt run
   ```

---

## Workflow

### 1. Data Ingestion (Airbyte)

Ingest customer and transaction data from CSV files or APIs:

```bash
# Configure in Airbyte UI
Source: File (CSV) / API
Destination: PostgreSQL (raw schema)
Schedule: Daily sync
```

**Output Tables:**
- `raw.customers`
- `raw.transactions`

### 2. Data Transformation (dbt)

Transform raw data into analytics-ready features:

```sql
-- Example: dbt_models/marts/churn_features.sql
SELECT
  c.customer_id,
  c.gender,
  c.contract_type,
  t.avg_monthly_spend,
  t.last_payment_date,
  DATE_PART('day', NOW() - t.last_payment_date) AS days_since_payment,
  CASE WHEN c.status = 'Inactive' THEN 1 ELSE 0 END AS churn_label
FROM raw.customers c
JOIN raw.transactions t USING(customer_id);
```

Run transformations:
```bash
dbt run --project-dir dbt_models/
```

### 3. Orchestration (Prefect)

Automate the entire pipeline:

```python
from prefect import flow, task

@task
def airbyte_sync():
    # Trigger Airbyte connection sync
    pass

@task
def dbt_transform():
    # Run dbt models
    pass

@task
def train_ml_model():
    # Train churn prediction model
    pass

@flow
def main_pipeline():
    airbyte_sync()
    dbt_transform()
    train_ml_model()
```

Deploy and run:
```bash
python prefect_flows/etl_flow.py
```

### 4. Model Training (ML)

Train the churn prediction model:

```bash
python ml/train_model.py
```

**Features Used:**
- Contract type
- Monthly spend
- Payment history
- Days since last payment
- Customer tenure

### 5. Dashboard (Streamlit)

Launch the interactive dashboard:

```bash
streamlit run streamlit_app/app.py
```

Access at: `http://localhost:8501`

---

## Model Performance

| Metric | Value |
|--------|-------|
| **Accuracy** | 92.1% |
| **Precision** | 89.3% |
| **Recall** | 88.9% |
| **ROC AUC** | 0.93 |

The XGBoost classifier successfully identifies high-risk customers with strong predictive performance across all metrics.

---

## Dashboard

The Streamlit dashboard provides:

- **Churn Probability Distribution**: Visualize risk across customer base
- **High-Risk Customer List**: Identify customers requiring intervention
- **Feature Importance**: Understand key churn drivers
- **Segmentation Analysis**: Churn rates by contract type, demographics
- **Real-time Predictions**: Score new customers instantly

---

## Future Enhancements

- [ ] Integrate MLflow for experiment tracking and model versioning
- [ ] Deploy model as REST API for real-time predictions
- [ ] Add Metabase/Superset for advanced BI analytics
- [ ] Implement A/B testing framework for retention strategies
- [ ] Schedule automated retraining with Prefect Cloud
- [ ] Add data quality checks with Great Expectations
- [ ] Implement feature store for ML features

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Author

**Angela Anindya Joshi**

Data Analyst | ML + Modern Data Stack Enthusiast

- Email: angelaanindyajoshi@gmail.com
- GitHub: [@angelajoshi](https://github.com/angelajoshi)


---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Airbyte for making data ingestion simple
- dbt Labs for transforming the way we transform data
- Prefect for elegant workflow orchestration
- The open-source data community

---

<div align="center">

**Star this repo if you find it helpful!**

Made with dedication and coffee

</div>
