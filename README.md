# Hospitality Analytics – Hotel Performance Dashboard

## 1. Project Overview

Hospitality Analytics is a data analytics project designed to analyse hotel performance across multiple locations over a five-year period (2022–2026).

The project uses dimensional modelling, Python-based synthetic data generation, MySQL for data storage and aggregation, and Streamlit for interactive KPI visualisation.

The dashboard helps users monitor hotel performance, identify trends and understand business metrics through interactive filters and charts.

## 2. Project Objectives

- Design and implement a dimensional data model.
- Generate five years of realistic synthetic hospitality data.
- Store and manage data using MySQL.
- Create SQL aggregate tables for business KPIs.
- Connect Python to MySQL using SQLAlchemy.
- Build an interactive dashboard using Streamlit.
- Interpret business trends and variations through an inference report.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data generation and database connectivity |
| Pandas | Data manipulation and analysis |
| Faker | Synthetic data generation |
| NumPy | Numerical operations |
| MySQL | Database storage and SQL aggregation |
| SQLAlchemy | Python–MySQL connectivity |
| Streamlit | Interactive dashboard |
| Plotly | Data visualisation |

## 4. Project Structure

```text
Hospitality_Analytics/
│
├── dashboard/
│   ├── app.py
│   └── db_connection.py
│
├── data/
│   └── Generated CSV files (not included in GitHub)
│
├── docs/
│   └── inference_report.md
│
├── sql/
│   ├── create_tables.sql
│   └── aggregate_tables.sql
│
├── create_database.py
├── generate_data.py
├── load_data.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 5. Database Design

The project follows a dimensional modelling approach.

### Dimension Tables

- `dim_hotel` – Hotel information and location.
- `dim_room` – Room details and hotel association.
- `dim_guest` – Guest information.
- `dim_employee` – Employee information and department.
- `dim_date` – Calendar attributes and seasonal classification.

### Fact Tables

- `fact_room_night` – Room availability, occupancy and revenue.
- `fact_guest_feedback` – Guest satisfaction ratings.
- `fact_employee_movement` – Employee joining and exit events.

### Aggregate Tables

| Aggregate Table | Purpose |
|---|---|
| `agg_monthly_hotel_performance` | Monthly occupancy, ADR and RevPAR |
| `agg_monthly_guest_satisfaction` | Monthly guest satisfaction |
| `agg_annual_employee_turnover` | Annual employee turnover |
| `agg_annual_hotel_kpi` | Consolidated annual hotel KPIs |

## 6. Key Performance Indicators

1. **Occupancy Rate**

   Occupied Room Nights / Available Room Nights × 100

2. **Average Daily Rate (ADR)**

   Total Room Revenue / Occupied Room Nights

3. **Revenue Per Available Room (RevPAR)**

   Total Room Revenue / Available Room Nights

4. **Guest Satisfaction Score**

   Average of guest satisfaction ratings.

5. **Employee Turnover Rate**

   Employee Exits / Average Employee Count × 100

## 7. Dataset Information

- Period: 2022–2026
- Number of hotels: 10
- Number of cities: 5
- Number of guests: 1,000
- Number of employees: 311
- Number of rooms: 413
- Room-night records: 754,138
- Guest feedback records: 5,000
- Employee movement records: 361

The dataset is synthetically generated using Python and Faker.

The complete year 2026 is simulated, including dates after the actual data-generation date.

## 8. Setup and Execution

### Step 1: Clone the Repository

```bash
git clone <your-github-repository-url>
cd Hospitality_Analytics
```

### Step 2: Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Database Credentials

Create a local `.env` file using the example configuration:

```bash
cp .env.example .env
```

Update the database credentials in `.env` with your local MySQL details.

Do not upload `.env` to GitHub.

### Step 5: Create the Database

```bash
python create_database.py
```

This creates the `hospitality_analytics` database if it does not already exist.

### Step 6: Create Database Tables

Execute the SQL script below using MySQL Workbench:

```text
sql/create_tables.sql
```

This creates the dimension and fact tables.

### Step 7: Generate Synthetic Data

```bash
python generate_data.py
```

This generates the CSV datasets inside the `data/` directory.

### Step 8: Load Data into MySQL

```bash
python load_data.py
```

The dimension tables are loaded before the fact tables to satisfy foreign key constraints.

Run this data-loading step once against an empty set of tables. The script appends records and is not designed for repeated loading into populated tables.

### Step 9: Create Aggregate Tables

Execute the following SQL script using MySQL Workbench:

```text
sql/aggregate_tables.sql
```

This creates the four aggregate tables required for KPI analysis and dashboard reporting.

### Step 10: Run the Dashboard

```bash
streamlit run dashboard/app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## 9. Dashboard Features

The Streamlit dashboard provides:

- City selection.
- Hotel selection.
- Year and month filters.
- Five KPI summary cards.
- Monthly occupancy trends.
- Monthly ADR and RevPAR trends.
- Guest satisfaction analysis.
- Annual employee turnover analysis.

## 10. Business Insights

The inference report is available at:

`docs/inference_report.md`

It explains annual KPI trends, possible seasonal influences, business observations, recommendations and dataset limitations.

## 11. Assumptions and Limitations

- All records are synthetically generated and do not represent actual hotel operations.
- Seasonal variations are based on qualitative project guidance.
- The complete year 2026 is simulated.
- Employee joining and exit dates are generated synthetically.
- The employee dataset does not include an opening workforce from before 2022, which affects turnover interpretation.
- Annual summaries may not reveal monthly or hotel-level variations.