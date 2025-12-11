# FAA Metrics Dashboard ✈️

BSAN 726 Group Project - University of Kansas

A comprehensive dashboard for visualizing Federal Aviation Administration (FAA) metrics, including KPIs and interactive visualizations for flight operations data.

## Features

- **Key Performance Indicators (KPIs)**
  - Total flights
  - On-time performance percentage
  - Average delay time
  - Cancellation rate
  - Delay and cancellation trends

- **Interactive Visualizations**
  - On-time performance trends
  - Average delay time trends
  - Daily flight operations overview
  - Flight status distribution
  - Delay type analysis (Weather, Carrier, NAS, Security, Late Aircraft)
  - Stacked area charts for delay trends

- **Data Controls**
  - Adjustable historical data range (30-365 days)
  - Configurable analysis period (7-90 days)
  - Data download functionality (CSV export)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Gerald-Jinx-Mouse/FAA_Dashboard_Cleaned.git
cd FAA_Dashboard_Cleaned
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the dashboard using Streamlit:

```bash
streamlit run faa_dashboard.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

## Dashboard Components

### KPI Metrics Section
Displays key performance indicators for the last 30 days:
- Total flights processed
- On-time performance percentage with trend
- Average delay time with trend
- Cancellation rate with trend
- Total delayed and cancelled flights
- Diverted flights count

### Visualizations
1. **On-Time Performance Trend**: Line chart showing on-time percentage over time with target line
2. **Average Delay Time Trend**: Line chart showing average delay minutes
3. **Daily Flight Operations**: Multi-line chart showing total, on-time, delayed, and cancelled flights
4. **Flight Status Distribution**: Pie chart showing current day's flight status breakdown
5. **Delay Type Analysis**: Bar chart and stacked area chart showing delays by category

### Data Table
Optional raw data table view with formatted metrics and CSV download capability

## Dependencies

- `streamlit>=1.28.0` - Dashboard framework
- `pandas>=2.0.0` - Data manipulation
- `numpy>=1.24.0` - Numerical operations
- `plotly>=5.17.0` - Interactive visualizations

## Project Structure

```
FAA_Dashboard_Cleaned/
├── faa_dashboard.py      # Main dashboard application
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## Data

The current implementation uses generated sample data for demonstration purposes. The data includes:
- Daily flight counts
- On-time, delayed, cancelled, and diverted flights
- Delay categories (Weather, Carrier, NAS, Security, Late Aircraft)
- Performance metrics and rates

To use real FAA data, replace the `generate_sample_data()` function with your data loading logic.

## Customization

You can customize the dashboard by:
- Modifying the date ranges in the sidebar
- Adjusting the KPI calculation period
- Adding new visualizations
- Integrating real FAA data sources
- Customizing colors and styling in the CSS section

## Contributing

This is a group project for BSAN 726 at the University of Kansas. For contributions or questions, please contact the project team.

## License

This project is created for educational purposes as part of a university course project.

## Acknowledgments

- University of Kansas - BSAN 726 Course
- Federal Aviation Administration for data metrics inspiration
