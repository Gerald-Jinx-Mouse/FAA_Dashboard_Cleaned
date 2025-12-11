"""
Test script to verify FAA Dashboard functionality
This script tests the core functions without running the full Streamlit app
"""

import sys
import faa_dashboard

def test_data_generation():
    """Test sample data generation"""
    print("Testing data generation...")
    
    # Test with default 90 days
    df = faa_dashboard.generate_sample_data(90)
    assert len(df) == 90, f"Expected 90 rows, got {len(df)}"
    
    # Test with different sizes
    for days in [30, 60, 180, 365]:
        df = faa_dashboard.generate_sample_data(days)
        assert len(df) == days, f"Expected {days} rows, got {len(df)}"
    
    print("✓ Data generation tests passed")
    return df

def test_data_consistency(df):
    """Test that generated data is internally consistent"""
    print("Testing data consistency...")
    
    for i in range(len(df)):
        row = df.iloc[i]
        
        # Test flight totals
        total = row['total_flights']
        components = (row['on_time_flights'] + row['delayed_flights'] + 
                     row['cancelled_flights'] + row['diverted_flights'])
        assert abs(total - components) <= 1, \
            f"Row {i}: Flight totals inconsistent (total={total}, sum={components})"
        
        # Test delay types
        delayed = row['delayed_flights']
        delay_sum = (row['weather_delays'] + row['carrier_delays'] + 
                    row['nas_delays'] + row['security_delays'] + 
                    row['late_aircraft_delays'])
        assert abs(delayed - delay_sum) <= 1, \
            f"Row {i}: Delay types inconsistent (delayed={delayed}, sum={delay_sum})"
    
    print("✓ Data consistency tests passed")

def test_kpi_calculation():
    """Test KPI calculations"""
    print("Testing KPI calculations...")
    
    # Test with normal dataset
    df = faa_dashboard.generate_sample_data(90)
    kpis = faa_dashboard.calculate_kpis(df)
    
    required_keys = [
        'total_flights', 'on_time_percentage', 'avg_delay_minutes',
        'cancellation_rate', 'total_delayed', 'total_cancelled',
        'on_time_trend', 'delay_trend', 'cancellation_trend'
    ]
    
    for key in required_keys:
        assert key in kpis, f"Missing KPI: {key}"
    
    # Test with small dataset (edge case)
    df_small = faa_dashboard.generate_sample_data(30)
    kpis_small = faa_dashboard.calculate_kpis(df_small)
    assert len(kpis_small) == len(required_keys), "KPI calculation failed for small dataset"
    
    # Test with very small dataset
    df_tiny = faa_dashboard.generate_sample_data(10)
    kpis_tiny = faa_dashboard.calculate_kpis(df_tiny)
    assert len(kpis_tiny) == len(required_keys), "KPI calculation failed for tiny dataset"
    
    print("✓ KPI calculation tests passed")

def test_metrics_ranges():
    """Test that metrics are within reasonable ranges"""
    print("Testing metric ranges...")
    
    df = faa_dashboard.generate_sample_data(90)
    
    # Test percentages are between 0 and 100
    assert (df['on_time_percentage'] >= 0).all() and (df['on_time_percentage'] <= 100).all()
    assert (df['cancellation_rate'] >= 0).all() and (df['cancellation_rate'] <= 100).all()
    assert (df['delay_rate'] >= 0).all() and (df['delay_rate'] <= 100).all()
    
    # Test counts are non-negative
    assert (df['total_flights'] >= 0).all()
    assert (df['on_time_flights'] >= 0).all()
    assert (df['delayed_flights'] >= 0).all()
    assert (df['cancelled_flights'] >= 0).all()
    
    print("✓ Metric range tests passed")

def main():
    """Run all tests"""
    print("=" * 60)
    print("FAA Dashboard Test Suite")
    print("=" * 60)
    
    try:
        df = test_data_generation()
        test_data_consistency(df)
        test_kpi_calculation()
        test_metrics_ranges()
        
        print("\n" + "=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        print("\nThe FAA Dashboard is ready to use!")
        print("Run: streamlit run faa_dashboard.py")
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
