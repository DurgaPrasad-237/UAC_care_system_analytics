# 🏥 System Capacity & Care Load Analytics for Unaccompanied Children

> A data analytics framework for monitoring the UAC care system — developed for the U.S. Department of Health and Human Services as part of the Unified Mentor Data Analytics Internship.

---

## 📋 Project Overview

The **Unaccompanied Alien Children (UAC) Program** is a federally mandated initiative under which children apprehended by U.S. Customs and Border Protection (CBP) are transferred to the Department of Health and Human Services (HHS) for medical screening, sheltering, and eventual placement with vetted sponsors.

This project delivers a **centralized healthcare analytics framework** to monitor the UAC care system using daily operational data spanning **January 2023 to December 2025**.

---

## ❗ Problem Statement

Although daily operational data is collected, HHS lacked a centralized analytical framework to continuously assess:

- Total care system load
- Balance between inflow and outflow
- Capacity stress and relief periods
- Sustainability of care delivery over time

---

## 🎯 Objectives

**Primary:**
- Quantify daily and cumulative care load across CBP and HHS
- Identify periods of capacity strain and relief
- Analyze balance between intake, transfers, and discharges

**Secondary:**
- Support healthcare staffing and shelter planning
- Improve situational awareness for policymakers
- Enable data-driven humanitarian response evaluation

---

## 📊 Dataset Description

| Column | Type | Description |
|--------|------|-------------|
| Date | Datetime | Daily reporting date (2023-2025) |
| Children Apprehended (CBP) | Flow | Daily new intake into CBP custody |
| Children in CBP Custody | Stock | Active CBP care load (end-of-day) |
| Children Transferred out of CBP | Flow | Daily transfers from CBP to HHS |
| Children in HHS Care | Stock | Active HHS care load (end-of-day) |
| Children Discharged from HHS | Flow | Daily successful sponsor placements |

> **Stock metrics** = point-in-time snapshot | **Flow metrics** = daily movement count

---

## 🔧 Methodology

### 1. Data Ingestion & Structuring
- Loaded daily time-series data (2023-2025)
- Converted Date to datetime format
- Ensured chronological ordering
- Created complete daily index (identified **355 missing dates**)

### 2. Data Quality & Validation
- Identified and handled missing dates using differentiated imputation
  - Stock columns → forward fill (ffill)
  - Flow columns → set to 0
- Flagged all imputed rows in `data_status` column
- Validated logical constraints:
  - Transfers ≤ CBP Custody → **86 violations found**
  - Discharges ≤ HHS Care → **0 violations**
- Applied advanced morning count validation → reduced to **3 genuine anomalies**

### 3. Derived Healthcare Capacity Metrics

| Metric | Formula | Purpose |
|--------|---------|---------|
| Total System Load | CBP Custody + HHS Care | System-wide daily burden |
| Net Daily Intake | Transfers - Discharges | Daily pressure vs relief |
| Care Load Growth Rate | pct_change() of Total Load | Day-over-day % change |
| Backlog Indicator | cumsum() of Net Daily Intake | Cumulative care pressure |
| Discharge Offset Ratio | Discharges / Transfers | Load relief efficiency |

### 4. Trend & Temporal Analysis
- Daily, weekly, and monthly care load trends
- Identification of 4 distinct high-load periods
- Early vs late timeline comparison (2023 vs 2025)

### 5. Pressure & Stress Identification
- 7-day and 14-day rolling averages
- Variability analysis
- Detection of prolonged strain windows

---

## 📈 Key Performance Indicators

| KPI | Value | Interpretation |
|-----|-------|----------------|
| Total Children Under Care | **6,251** avg/day | System-wide daily burden |
| Net Intake Pressure | **-29.96** avg/day | System relieving ~30 children/day |
| Care Load Volatility Index | **2,922.85** | High instability — load ranged 2,000 to 11,500 |
| Backlog Accumulation Rate | **-32,212** cumulative | Net backlog fully cleared |
| Discharge Offset Ratio | **1.35** | 135 discharges per 100 transfers |

---

## 🔍 Key Findings

- System load **peaked at ~11,500 children** in late 2023 and **declined 80%** to ~2,000 by mid-2025
- **355 missing dates (33%)** represent the most critical data quality issue
- **4 high-load periods** identified — longest being **161 consecutive days**
- **HHS discharge ratio of 1.35** confirms effective sponsor placement
- System remains **vulnerable to surge conditions**

---

## 🗂️ Project Structure

```
UAC_Project/
│
├── UAC_Analysis.ipynb          # Main Jupyter Notebook (full analysis)
├── app.py                      # Streamlit Dashboard
├── uac_cleaned.csv             # Final cleaned dataset
├── uac_data.csv                # Raw original data
├── requirements.txt            # Python dependencies
├── UAC_Research_Paper.docx     # Full research paper
├── UAC_Executive_Summary.docx  # Executive summary for stakeholders
└── README.md                   # Project documentation
```

---

## 🖥️ Streamlit Dashboard

The interactive dashboard includes:

- **KPI Summary Cards** — 5 live KPIs updating with filters
- **System Load Overview** — with 7-day and 14-day rolling averages
- **CBP vs HHS Comparison** — side-by-side load tracking
- **Net Intake & Backlog Trends** — pressure vs relief analysis
- **Date Range Selector** — filter by any date range
- **Time Granularity Filter** — Daily / Weekly / Monthly view
- **Metric Toggles** — show/hide specific chart elements

### Run Locally

```bash
# Clone the repository
git clone https://github.com/your-username/uac-analytics.git
cd uac-analytics

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

---

## 📦 Requirements

```
streamlit
pandas
matplotlib
seaborn
numpy
```

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## 📁 Deliverables

| Deliverable | Description |
|-------------|-------------|
| `UAC_Analysis.ipynb` | Full EDA, data cleaning, metrics, KPIs |
| `app.py` | Interactive Streamlit dashboard |
| `UAC_Research_Paper.docx` | 10-page research paper with findings |
| `UAC_Executive_Summary.docx` | 2-page summary for government stakeholders |

---

## 🏛️ About

**Program:** Unified Mentor Data Analytics Internship

**Client:** U.S. Department of Health and Human Services

**Analysis Period:** January 2023 — December 2025

**Report Date:** April 2026

---

## 📜 References
 
- U.S. Department of Health and Human Services — UAC Program Data

