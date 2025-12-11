# FAA Wildlife Strike Dashboard – README

This repository contains a Python script that generates an interactive, browser-based dashboard analyzing FAA Wildlife Strike data for the years 2019–2020. The dashboard supports the BSAN 726 Group Project and visualizes trends, species involvement, geographic patterns, and COVID-19 pandemic impacts.

## Project Overview

The included script, FAA_Dashboard_Cleaned.py, loads the cleaned FAA Wildlife Strike dataset, applies time filtering (2019–2020), constructs multiple analytics charts using Plotly, encodes figures into JSON without binary payloads, builds a fully styled dark-themed interactive HTML dashboard, and writes the final dashboard to FAA_Dashboard.html.

## Files

### 1. FAA_Dashboard_Cleaned.py
The main Python script that loads, cleans, analyzes, visualizes, and exports the dashboard.

### 2. FAA_Dashboard_Cleaned.csv
An external cleaned dataset the script reads. This file must be present at the path defined in the script.

### 3. FAA_Dashboard.html
The generated interactive dashboard.

## Requirements

Python packages required:
- pandas
- numpy
- plotly
- json
- base64
- struct

Install dependencies with:

```
pip install pandas numpy plotly
```

## How to Run the Script

1. Ensure the dataset path inside the script matches your local directory:

```
df = pd.read_csv('/path/to/FAA_Dashboard_Cleaned.csv', low_memory=False)
```

2. Run the script:

```
python FAA_Dashboard_Cleaned.py
```

3. After running, you will see a message indicating where the HTML dashboard was saved.

4. Open the HTML file in a browser to explore all visualizations interactively.

## Visualizations Included

The dashboard generates 10 interactive Plotly charts grouped into analytical areas:

### Q1: Pandemic Impact
- Wildlife strikes before vs. during COVID-19 (2019 vs. 2020)
- Monthly trends by pandemic period

### Q2: Temporal and Geographic Patterns
- US geo-scatter map of airport strike counts
- Top states
- Time-of-day strike distribution

### Q3: Species and Damage
- Top 10 wildlife species
- Damage level distribution

### Q4: Aircraft and Operators
- Top aircraft types
- Top airline operators
- Strike counts by phase of flight

## Summary Statistics Calculated

The script computes and displays:
- Total strike count
- Strike counts before vs. during pandemic
- Percent change between years
- Number of unique states, species, aircraft types, and airports

## Dashboard Styling

The HTML uses:
- A modern dark UI theme
- Gradient headers and cards
- Responsive chart layout
- Full-width sections for readability

## Project Context

This dashboard was developed for:

BSAN 726 – Enterprise Data Management  
KU School of Business — Fall 2025

## Output

Running the script produces an HTML dashboard file named:

```
FAA_Dashboard.html
```

Open the file in a browser to interact with the dashboard.

