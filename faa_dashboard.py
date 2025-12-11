"""
FAA Dashboard - KPI and Visuals for FAA Metrics
A Streamlit-based dashboard for visualizing Federal Aviation Administration metrics
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="FAA Metrics Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .kpi-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 1rem;
        color: #666;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def generate_sample_data(num_days=90):
    """
    Generate sample FAA flight data for demonstration
    
    Args:
        num_days: Number of days of data to generate
    
    Returns:
        DataFrame with sample flight data
    """
    np.random.seed(42)
    dates = pd.date_range(end=datetime.now(), periods=num_days, freq='D')
    
    data = {
        'date': dates,
        'total_flights': np.random.randint(40000, 50000, num_days),
        'on_time_flights': np.random.randint(30000, 40000, num_days),
        'delayed_flights': np.random.randint(5000, 10000, num_days),
        'cancelled_flights': np.random.randint(100, 1000, num_days),
        'diverted_flights': np.random.randint(50, 300, num_days),
        'avg_delay_minutes': np.random.uniform(15, 45, num_days),
        'weather_delays': np.random.randint(1000, 3000, num_days),
        'carrier_delays': np.random.randint(1500, 3500, num_days),
        'nas_delays': np.random.randint(500, 1500, num_days),
        'security_delays': np.random.randint(50, 200, num_days),
        'late_aircraft_delays': np.random.randint(1000, 2500, num_days),
    }
    
    df = pd.DataFrame(data)
    
    # Calculate derived metrics
    df['on_time_percentage'] = (df['on_time_flights'] / df['total_flights']) * 100
    df['cancellation_rate'] = (df['cancelled_flights'] / df['total_flights']) * 100
    df['delay_rate'] = (df['delayed_flights'] / df['total_flights']) * 100
    
    return df

def calculate_kpis(df):
    """
    Calculate Key Performance Indicators from the data
    
    Args:
        df: DataFrame with flight data
    
    Returns:
        Dictionary with KPI values
    """
    latest_data = df.tail(30)  # Last 30 days
    previous_data = df.iloc[-60:-30]  # Previous 30 days
    
    kpis = {
        'total_flights': latest_data['total_flights'].sum(),
        'on_time_percentage': latest_data['on_time_percentage'].mean(),
        'avg_delay_minutes': latest_data['avg_delay_minutes'].mean(),
        'cancellation_rate': latest_data['cancellation_rate'].mean(),
        'total_delayed': latest_data['delayed_flights'].sum(),
        'total_cancelled': latest_data['cancelled_flights'].sum(),
    }
    
    # Calculate trends (comparison with previous period)
    kpis['on_time_trend'] = latest_data['on_time_percentage'].mean() - previous_data['on_time_percentage'].mean()
    kpis['delay_trend'] = latest_data['avg_delay_minutes'].mean() - previous_data['avg_delay_minutes'].mean()
    kpis['cancellation_trend'] = latest_data['cancellation_rate'].mean() - previous_data['cancellation_rate'].mean()
    
    return kpis

def main():
    """
    Main function to run the FAA Dashboard
    """
    # Header
    st.markdown('<h1 class="main-header">✈️ FAA Metrics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("### Federal Aviation Administration - Flight Operations KPIs and Analytics")
    st.markdown("---")
    
    # Sidebar controls
    st.sidebar.header("Dashboard Controls")
    st.sidebar.markdown("### Data Settings")
    
    num_days = st.sidebar.slider(
        "Historical Data Range (Days)",
        min_value=30,
        max_value=365,
        value=90,
        step=30
    )
    
    date_range = st.sidebar.slider(
        "Analysis Period (Days)",
        min_value=7,
        max_value=90,
        value=30,
        step=7
    )
    
    # Generate data
    df = generate_sample_data(num_days)
    df_filtered = df.tail(date_range)
    
    # Calculate KPIs
    kpis = calculate_kpis(df)
    
    # Display KPIs
    st.markdown("## 📊 Key Performance Indicators (Last 30 Days)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Flights",
            value=f"{int(kpis['total_flights']):,}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="On-Time Performance",
            value=f"{kpis['on_time_percentage']:.1f}%",
            delta=f"{kpis['on_time_trend']:.1f}%"
        )
    
    with col3:
        st.metric(
            label="Avg Delay Time",
            value=f"{kpis['avg_delay_minutes']:.1f} min",
            delta=f"{kpis['delay_trend']:.1f} min",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            label="Cancellation Rate",
            value=f"{kpis['cancellation_rate']:.2f}%",
            delta=f"{kpis['cancellation_trend']:.2f}%",
            delta_color="inverse"
        )
    
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric(
            label="Total Delayed Flights",
            value=f"{int(kpis['total_delayed']):,}"
        )
    
    with col6:
        st.metric(
            label="Total Cancelled",
            value=f"{int(kpis['total_cancelled']):,}"
        )
    
    with col7:
        st.metric(
            label="Delay Rate",
            value=f"{df_filtered['delay_rate'].mean():.1f}%"
        )
    
    with col8:
        st.metric(
            label="Diverted Flights",
            value=f"{int(df_filtered['diverted_flights'].sum()):,}"
        )
    
    st.markdown("---")
    
    # Visualizations
    st.markdown("## 📈 Flight Operations Trends")
    
    # Trend Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # On-time performance trend
        fig1 = px.line(
            df_filtered,
            x='date',
            y='on_time_percentage',
            title='On-Time Performance Trend',
            labels={'on_time_percentage': 'On-Time %', 'date': 'Date'}
        )
        fig1.update_traces(line_color='#2ecc71')
        fig1.add_hline(y=80, line_dash="dash", line_color="red", 
                      annotation_text="Target: 80%")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Average delay time trend
        fig2 = px.line(
            df_filtered,
            x='date',
            y='avg_delay_minutes',
            title='Average Delay Time Trend',
            labels={'avg_delay_minutes': 'Avg Delay (minutes)', 'date': 'Date'}
        )
        fig2.update_traces(line_color='#e74c3c')
        st.plotly_chart(fig2, use_container_width=True)
    
    # Flight Operations Overview
    st.markdown("## 🛫 Flight Operations Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Daily flight operations
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=df_filtered['date'],
            y=df_filtered['total_flights'],
            name='Total Flights',
            line=dict(color='#3498db', width=2)
        ))
        fig3.add_trace(go.Scatter(
            x=df_filtered['date'],
            y=df_filtered['on_time_flights'],
            name='On-Time',
            line=dict(color='#2ecc71', width=2)
        ))
        fig3.add_trace(go.Scatter(
            x=df_filtered['date'],
            y=df_filtered['delayed_flights'],
            name='Delayed',
            line=dict(color='#f39c12', width=2)
        ))
        fig3.add_trace(go.Scatter(
            x=df_filtered['date'],
            y=df_filtered['cancelled_flights'],
            name='Cancelled',
            line=dict(color='#e74c3c', width=2)
        ))
        fig3.update_layout(
            title='Daily Flight Operations',
            xaxis_title='Date',
            yaxis_title='Number of Flights',
            hovermode='x unified'
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # Flight status distribution (pie chart)
        latest_day = df_filtered.iloc[-1]
        flight_status = {
            'On-Time': latest_day['on_time_flights'],
            'Delayed': latest_day['delayed_flights'],
            'Cancelled': latest_day['cancelled_flights'],
            'Diverted': latest_day['diverted_flights']
        }
        
        fig4 = px.pie(
            values=list(flight_status.values()),
            names=list(flight_status.keys()),
            title=f'Flight Status Distribution ({latest_day["date"].strftime("%Y-%m-%d")})',
            color_discrete_sequence=['#2ecc71', '#f39c12', '#e74c3c', '#9b59b6']
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    # Delay Analysis
    st.markdown("## ⏱️ Delay Type Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Delay types breakdown
        delay_types = {
            'Weather': df_filtered['weather_delays'].sum(),
            'Carrier': df_filtered['carrier_delays'].sum(),
            'NAS': df_filtered['nas_delays'].sum(),
            'Security': df_filtered['security_delays'].sum(),
            'Late Aircraft': df_filtered['late_aircraft_delays'].sum()
        }
        
        fig5 = px.bar(
            x=list(delay_types.keys()),
            y=list(delay_types.values()),
            title='Total Delays by Type',
            labels={'x': 'Delay Type', 'y': 'Number of Delays'},
            color=list(delay_types.keys()),
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        # Delay types trend
        fig6 = go.Figure()
        fig6.add_trace(go.Scatter(x=df_filtered['date'], y=df_filtered['weather_delays'], 
                                  name='Weather', stackgroup='one'))
        fig6.add_trace(go.Scatter(x=df_filtered['date'], y=df_filtered['carrier_delays'], 
                                  name='Carrier', stackgroup='one'))
        fig6.add_trace(go.Scatter(x=df_filtered['date'], y=df_filtered['nas_delays'], 
                                  name='NAS', stackgroup='one'))
        fig6.add_trace(go.Scatter(x=df_filtered['date'], y=df_filtered['security_delays'], 
                                  name='Security', stackgroup='one'))
        fig6.add_trace(go.Scatter(x=df_filtered['date'], y=df_filtered['late_aircraft_delays'], 
                                  name='Late Aircraft', stackgroup='one'))
        fig6.update_layout(
            title='Delay Types Trend (Stacked)',
            xaxis_title='Date',
            yaxis_title='Number of Delays',
            hovermode='x unified'
        )
        st.plotly_chart(fig6, use_container_width=True)
    
    # Data table
    st.markdown("## 📋 Raw Data")
    
    if st.checkbox("Show Raw Data"):
        st.dataframe(
            df_filtered.style.format({
                'on_time_percentage': '{:.2f}%',
                'cancellation_rate': '{:.2f}%',
                'delay_rate': '{:.2f}%',
                'avg_delay_minutes': '{:.2f}'
            }),
            use_container_width=True
        )
    
    # Download data option
    st.markdown("---")
    st.markdown("### 💾 Download Data")
    
    csv = df_filtered.to_csv(index=False)
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name=f"faa_metrics_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 1rem;'>
            <p>FAA Metrics Dashboard | University of Kansas - BSAN 726 Group Project</p>
            <p>Data is generated for demonstration purposes</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
