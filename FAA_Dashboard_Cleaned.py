#!/usr/bin/env python3
"""
FAA Wildlife Strike Data Visualization - Interactive HTML Report
BSAN 726 Group Project

Run this script to generate an interactive HTML dashboard.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import numpy as np
import base64
import struct

# Load the cleaned data
df = pd.read_csv('/Users/jacob/Documents/GitHub/KU/1. Fall 2025/3. BSAN 726/0. GrpProj-Refl/0. Group Projects/1. Assignments/3. GrpProjUpdFinal/My Work/Py/FAA_Dashboard_Cleaned.csv', low_memory=False)

# Filter to 2019-2020
df = df[(df['YEAR'] >= 2019) & (df['YEAR'] <= 2020)]

# Create PANDEMIC column (Before = 2019, During = 2020)
df['PANDEMIC'] = df['YEAR'].apply(lambda x: 'Before' if x == 2019 else 'During')

# Create YEAR_MONTH column for time series
df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
df['YEAR_MONTH'] = df['DATE'].dt.to_period('M').astype(str)


def decode_bdata(bdata, dtype):
    """Decode Plotly's binary encoded data to a list"""
    raw_bytes = base64.b64decode(bdata)

    # Map Plotly dtype to struct format
    dtype_map = {
        'i1': 'b',   # int8
        'u1': 'B',   # uint8
        'i2': 'h',   # int16
        'u2': 'H',   # uint16
        'i4': 'i',   # int32
        'u4': 'I',   # uint32
        'f4': 'f',   # float32
        'f8': 'd',   # float64
    }

    fmt = dtype_map.get(dtype, 'f8')  # default to float64
    size = struct.calcsize(fmt)
    count = len(raw_bytes) // size
    values = struct.unpack('<' + fmt * count, raw_bytes)
    return list(values)


def convert_to_serializable(obj):
    """Recursively convert binary-encoded data and numpy types to plain JSON"""
    if isinstance(obj, dict):
        # Check for Plotly's binary encoding format and decode it
        if 'bdata' in obj and 'dtype' in obj:
            return decode_bdata(obj['bdata'], obj['dtype'])
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif pd.isna(obj):
        return None
    else:
        return obj


def fig_to_json_clean(fig):
    """Convert figure to clean JSON with plain arrays (no binary encoding)"""
    # Get the figure dict and decode all binary data
    fig_dict = fig.to_dict()
    clean_dict = convert_to_serializable(fig_dict)
    return json.dumps(clean_dict)

# =============================================================================
# APPLY DARK THEME TO ALL FIGURES
# =============================================================================
dark_layout = dict(
    paper_bgcolor='rgba(30, 58, 95, 0)',
    plot_bgcolor='rgba(30, 58, 95, 0)',
    font=dict(color='#eee', size=12),
    margin=dict(t=60, b=80, l=100, r=40),
    height=400
)

# =============================================================================
# CREATE FIGURES
# =============================================================================

# 1. Pandemic Comparison
pandemic_counts = df['PANDEMIC'].value_counts().reset_index()
pandemic_counts.columns = ['Period', 'Count']
fig1 = px.bar(pandemic_counts, x='Period', y='Count',
              color='Period',
              color_discrete_map={'Before': '#2ecc71', 'During': '#e74c3c'},
              title='Wildlife Strikes: Before vs During Pandemic (2019-2020)')
fig1.update_layout(showlegend=False, **dark_layout)

# 2. Monthly Trends
monthly = df.groupby(['YEAR_MONTH', 'PANDEMIC']).size().reset_index(name='Count')
fig2 = px.line(monthly, x='YEAR_MONTH', y='Count', color='PANDEMIC',
               markers=True,
               title='Monthly Wildlife Strikes (2019-2020)',
               color_discrete_map={'Before': '#2ecc71', 'During': '#e74c3c'})
fig2.update_xaxes(tickangle=45)
fig2.update_layout(**dark_layout)

# 3. Top 10 States
top_states = df['STATE'].value_counts().head(10).reset_index()
top_states.columns = ['State', 'Count']
fig3 = px.bar(top_states, x='Count', y='State', orientation='h',
              color='Count', color_continuous_scale='Blues',
              title='Top 10 States by Wildlife Strikes')
fig3.update_layout(yaxis={'categoryorder': 'total ascending'}, **dark_layout)

# 4. Top 10 Species
top_species = df['SPECIES'].value_counts().head(10).reset_index()
top_species.columns = ['Species', 'Count']
fig4 = px.bar(top_species, x='Count', y='Species', orientation='h',
              color='Count', color_continuous_scale='Oranges',
              title='Top 10 Species Involved in Wildlife Strikes')
fig4.update_layout(yaxis={'categoryorder': 'total ascending'}, **dark_layout)

# 5. Damage Level Distribution
damage_counts = df['DAMAGE_LEVEL'].value_counts().reset_index()
damage_counts.columns = ['Damage Level', 'Count']
fig5 = px.bar(damage_counts, x='Damage Level', y='Count',
              color='Damage Level',
              color_discrete_map={'N': '#2ecc71', 'M': '#f1c40f', 'M?': '#e67e22', 'S': '#e74c3c', 'D': '#8e44ad'},
              title='Distribution of Damage Levels (N=None, M=Minor, S=Substantial, D=Destroyed)')
fig5.update_layout(**dark_layout)

# 6. Time of Day
time_counts = df['TIME_OF_DAY'].value_counts().reset_index()
time_counts.columns = ['Time of Day', 'Count']
fig6 = px.pie(time_counts, values='Count', names='Time of Day',
              title='Wildlife Strikes by Time of Day',
              color_discrete_sequence=px.colors.qualitative.Set2)
fig6.update_layout(**dark_layout)

# 7. Top Operators
top_operators = df['OPERATOR'].value_counts().head(10).reset_index()
top_operators.columns = ['Operator', 'Count']
fig7 = px.bar(top_operators, x='Count', y='Operator', orientation='h',
              color='Count', color_continuous_scale='Teal',
              title='Top 10 Operators by Wildlife Strikes')
fig7.update_layout(yaxis={'categoryorder': 'total ascending'}, **dark_layout)

# 8. Phase of Flight
phase_counts = df['PHASE_OF_FLIGHT'].value_counts().head(8).reset_index()
phase_counts.columns = ['Phase', 'Count']
fig8 = px.bar(phase_counts, x='Phase', y='Count',
              color='Count', color_continuous_scale='Reds',
              title='Wildlife Strikes by Phase of Flight')
fig8.update_xaxes(tickangle=45)
fig8.update_layout(**dark_layout)

# 9. Top Aircraft Types (replacing Cost by Species - cost data not in cleaned file)
top_aircraft = df['AIRCRAFT'].value_counts().head(10).reset_index()
top_aircraft.columns = ['Aircraft', 'Count']
fig9 = px.bar(top_aircraft, x='Count', y='Aircraft', orientation='h',
              color='Count', color_continuous_scale='Reds',
              title='Top 10 Aircraft Types Involved in Wildlife Strikes')
fig9.update_layout(yaxis={'categoryorder': 'total ascending'}, **dark_layout)

# 10. Geographic Map (if lat/long available)
df_map = df.dropna(subset=['AIRPORT_LATITUDE', 'AIRPORT_LONGITUDE'])
airport_strikes = df_map.groupby(['AIRPORT', 'AIRPORT_LATITUDE', 'AIRPORT_LONGITUDE', 'STATE']).size().reset_index(name='Strikes')
fig10 = px.scatter_geo(airport_strikes,
                       lat='AIRPORT_LATITUDE',
                       lon='AIRPORT_LONGITUDE',
                       size='Strikes',
                       color='Strikes',
                       hover_name='AIRPORT',
                       hover_data=['STATE', 'Strikes'],
                       color_continuous_scale='YlOrRd',
                       title='Geographic Distribution of Wildlife Strikes',
                       scope='usa')
fig10.update_layout(**dark_layout)
fig10.update_geos(bgcolor='rgba(0,0,0,0)', lakecolor='#1e3a5f', landcolor='#2d4a6f')

# =============================================================================
# CALCULATE SUMMARY STATS
# =============================================================================
total_records = len(df)
before_count = len(df[df['PANDEMIC'] == 'Before'])
during_count = len(df[df['PANDEMIC'] == 'During'])
pct_change = ((during_count - before_count) / before_count * 100)
unique_states = df['STATE'].nunique()
unique_species = df['SPECIES'].nunique()
unique_aircraft = df['AIRCRAFT'].nunique()
unique_airports = df['AIRPORT'].nunique()

# =============================================================================
# GENERATE CLEAN JSON FOR EACH CHART (no binary encoding)
# =============================================================================
chart1_json = fig_to_json_clean(fig1)
chart2_json = fig_to_json_clean(fig2)
chart3_json = fig_to_json_clean(fig3)
chart4_json = fig_to_json_clean(fig4)
chart5_json = fig_to_json_clean(fig5)
chart6_json = fig_to_json_clean(fig6)
chart7_json = fig_to_json_clean(fig7)
chart8_json = fig_to_json_clean(fig8)
chart9_json = fig_to_json_clean(fig9)
chart10_json = fig_to_json_clean(fig10)

# =============================================================================
# BUILD HTML
# =============================================================================
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FAA Wildlife Strike Analysis - BSAN 726 Group Project</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            min-height: 100vh;
        }}
        .header {{
            background: linear-gradient(90deg, #0f3460 0%, #533483 100%);
            padding: 30px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            max-width: 1400px;
            margin: 0 auto;
        }}
        .card {{
            background: linear-gradient(145deg, #1e3a5f 0%, #2d4a6f 100%);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
            transition: transform 0.3s ease;
        }}
        .card:hover {{
            transform: translateY(-5px);
        }}
        .card h3 {{
            font-size: 0.9em;
            text-transform: uppercase;
            opacity: 0.8;
            margin-bottom: 10px;
        }}
        .card .value {{
            font-size: 2em;
            font-weight: bold;
            color: #00d9ff;
        }}
        .card.negative .value {{
            color: #ff6b6b;
        }}
        .card.positive .value {{
            color: #51cf66;
        }}
        .section {{
            padding: 20px 30px;
            max-width: 1400px;
            margin: 0 auto;
        }}
        .section h2 {{
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #533483;
        }}
        .chart-container {{
            background: #1e3a5f;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
            min-height: 450px;
        }}
        .chart-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 30px;
        }}
        .footer {{
            text-align: center;
            padding: 30px;
            background: #0f3460;
            margin-top: 50px;
        }}
        @media (max-width: 768px) {{
            .chart-row {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>FAA Wildlife Strike Analysis</h1>
        <p>BSAN 726 Group Project | 2019-2020 Data Analysis</p>
    </div>

    <div class="summary-cards">
        <div class="card">
            <h3>Total Strikes</h3>
            <div class="value">{total_records:,}</div>
        </div>
        <div class="card">
            <h3>Before Pandemic (2019)</h3>
            <div class="value">{before_count:,}</div>
        </div>
        <div class="card">
            <h3>During Pandemic (2020)</h3>
            <div class="value">{during_count:,}</div>
        </div>
        <div class="card negative">
            <h3>Change</h3>
            <div class="value">{pct_change:.1f}%</div>
        </div>
        <div class="card">
            <h3>States</h3>
            <div class="value">{unique_states}</div>
        </div>
        <div class="card">
            <h3>Species</h3>
            <div class="value">{unique_species}</div>
        </div>
        <div class="card">
            <h3>Aircraft Types</h3>
            <div class="value">{unique_aircraft}</div>
        </div>
        <div class="card">
            <h3>Airports</h3>
            <div class="value">{unique_airports}</div>
        </div>
    </div>

    <div class="section">
        <h2>Q1: Pandemic Impact Analysis</h2>
        <div class="chart-row">
            <div class="chart-container"><div id="chart1"></div></div>
            <div class="chart-container"><div id="chart2"></div></div>
        </div>
    </div>

    <div class="section">
        <h2>Q2: Temporal & Spatial Patterns</h2>
        <div class="chart-container"><div id="chart10"></div></div>
        <div class="chart-row">
            <div class="chart-container"><div id="chart3"></div></div>
            <div class="chart-container"><div id="chart6"></div></div>
        </div>
    </div>

    <div class="section">
        <h2>Q3: Species & Damage Analysis</h2>
        <div class="chart-row">
            <div class="chart-container"><div id="chart4"></div></div>
            <div class="chart-container"><div id="chart5"></div></div>
        </div>
    </div>

    <div class="section">
        <h2>Q4: Aircraft & Operator Analysis</h2>
        <div class="chart-row">
            <div class="chart-container"><div id="chart9"></div></div>
            <div class="chart-container"><div id="chart7"></div></div>
        </div>
        <div class="chart-container"><div id="chart8"></div></div>
    </div>

    <div class="footer">
        <p>BSAN 726: Enterprise Data Management | KU School of Business | Fall 2025</p>
        <p>Data Source: FAA Wildlife Strike Database (wildlife.faa.gov)</p>
    </div>

    <script>
        // Chart data (clean JSON, no binary encoding)
        var chart1_data = {chart1_json};
        var chart2_data = {chart2_json};
        var chart3_data = {chart3_json};
        var chart4_data = {chart4_json};
        var chart5_data = {chart5_json};
        var chart6_data = {chart6_json};
        var chart7_data = {chart7_json};
        var chart8_data = {chart8_json};
        var chart9_data = {chart9_json};
        var chart10_data = {chart10_json};

        // Render all charts
        var config = {{responsive: true}};
        Plotly.newPlot('chart1', chart1_data.data, chart1_data.layout, config);
        Plotly.newPlot('chart2', chart2_data.data, chart2_data.layout, config);
        Plotly.newPlot('chart3', chart3_data.data, chart3_data.layout, config);
        Plotly.newPlot('chart4', chart4_data.data, chart4_data.layout, config);
        Plotly.newPlot('chart5', chart5_data.data, chart5_data.layout, config);
        Plotly.newPlot('chart6', chart6_data.data, chart6_data.layout, config);
        Plotly.newPlot('chart7', chart7_data.data, chart7_data.layout, config);
        Plotly.newPlot('chart8', chart8_data.data, chart8_data.layout, config);
        Plotly.newPlot('chart9', chart9_data.data, chart9_data.layout, config);
        Plotly.newPlot('chart10', chart10_data.data, chart10_data.layout, config);
    </script>
</body>
</html>
"""

# Save HTML file
output_path = '/Users/jacob/Documents/GitHub/KU/1. Fall 2025/3. BSAN 726/0. GrpProj-Refl/0. Group Projects/1. Assignments/3. GrpProjUpdFinal/My Work/Py/FAA_Dashboard.html'
with open(output_path, 'w') as f:
    f.write(html_content)

print(f"Dashboard saved to: {output_path}")
print("Open this file in your browser to view the interactive dashboard!")
