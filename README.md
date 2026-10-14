# AI-S-O-C-I-U-S

<p align="center">
  <strong>Intelligent Financial Market Sentiment & Automated Trading Signal Intelligence Engine</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-22c55e?style=for-the-badge&logo=github&logoColor=white" alt="Status" />
  <img src="https://img.shields.io/badge/Python-3.10+-18181B?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Power_BI-Interactive_Dashboard-18181B?style=for-the-badge&logo=powerbi&logoColor=white" alt="Power BI" />
  <img src="https://img.shields.io/badge/License-MIT-18181B?style=for-the-badge" alt="License" />
</p>

---

## Overview

**AI-S-O-C-I-U-S** (System for Optimization of Capital, Intelligence, Uncertainty & Signals) is an end-to-end quantitative market intelligence platform that unifies real-time financial news sentiment extraction with time-series technical indicators to synthesize actionable trading signals and portfolio risk analytics.

The system extracts unstructured financial discourse using automated scraping and NLP processing, generates sentiment scores and LLM-grounded trading signals, and feeds structured telemetry directly into a production-grade Microsoft Power BI business intelligence dashboard (`.pbix`).

---

## Tech Stack

<p align="center">
  <img src="https://img.shields.io/badge/Python-18181B?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Power_BI-18181B?style=for-the-badge&logo=powerbi&logoColor=white" alt="Power BI" />
  <img src="https://img.shields.io/badge/Pandas-18181B?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/NLTK-18181B?style=for-the-badge&logo=python&logoColor=white" alt="NLTK" />
  <img src="https://img.shields.io/badge/BeautifulSoup4-18181B?style=for-the-badge&logo=python&logoColor=white" alt="BeautifulSoup4" />
</p>

---

## Architecture & Data Flow

```
Financial Feeds & News APIs
            │
            ▼
[Data Extraction & Web Ingestion]  (requests, beautifulsoup4)
            │
            ▼
[NLP Sentiment Analyzer]          (NLTK VADER / Transformer Scoring)
            │
            ▼
[LLM Signal Synthesizer]          (generate_signals_llm.py)
            │
            ▼
[Time-Series Data Consolidation]   (stock_signals_daily.csv, stock_sentiment_daily.csv)
            │
            ▼
[Interactive Power BI Dashboard]  (AI S-O-C-I-U-S.pbix)
```

---

## Key Features

- **Automated News Scraping & Text Parsing**: Scrapes financial news portals and press releases to build structured sentiment corpora.
- **LLM-Powered Signal Generation**: Analyzes contextual nuances in financial headlines and statements to synthesize Bullish, Bearish, or Neutral trading signals with confidence ratings.
- **Quantitative Market Data Merging**: Aligns sentiment scores against OHLCV historical pricing data to evaluate correlation between market sentiment shifts and price momentum.
- **Power BI Visual Analytics**: Pre-configured interactive `.pbix` dashboard with customizable filters for equities, sentiment trajectories, and portfolio risk distribution.

---

## Repository Structure

```
AI-S-O-C-I-U-S/
├── AI S-O-C-I-U-S.pbix          # Interactive Microsoft Power BI dashboard
├── fetch_and_predict.py         # Financial data ingestion and price prediction pipeline
├── generate_signals_llm.py      # LLM reasoning pipeline for trading signals
├── stock_data.csv               # Processed asset pricing dataset
├── stock_data_historical.csv    # Historical OHLCV baseline dataset
├── stock_sentiment_daily.csv    # Computed daily sentiment telemetry
├── stock_signals_daily.csv      # Generated daily trading signals and confidence
├── requirements.txt             # Python package dependencies
└── README.md
```

---

## Quickstart

### 1. Prerequisites
* Python 3.10+
* Microsoft Power BI Desktop (for inspecting the `.pbix` report)

### 2. Environment Setup
```bash
git clone https://github.com/prannesshkva/AI-S-O-C-I-U-S.git
cd AI-S-O-C-I-U-S
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Generate Daily Signals
```bash
python generate_signals_llm.py
python fetch_and_predict.py
```

### 4. Visualize Results
Open `AI S-O-C-I-U-S.pbix` in Microsoft Power BI Desktop and click **Refresh** to load the newly computed CSV telemetry.

---

## Author

* **Architect**: [Prannessh KVA](https://github.com/prannesshkva)
* **Focus**: Quantitative AI, Algorithmic Financial Intelligence, and Data Engineering

---

## License

This project is licensed under the MIT License.
