# emissions_data_processing.py

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set plot styling
plt.style.use('ggplot')
sns.set_theme(style="whitegrid")

# Display all columns
pd.set_option('display.max_columns', None)

def load_data():
    """Load the data from the JSON file"""
    # Get the path to the JSON file
    json_path = Path(__file__).parent.parent / 'resources' / 'sample_emissions_data.json'
    
    # Read the JSON file
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # Convert the data into pandas DataFrames for easier analysis
    facilities_df = pd.DataFrame(data['facilities'])
    
    # Convert emissions data to a more usable format
    emissions_list = []
    for emission in data['emissions_data']:
        facility_id = emission['facility_id']
        year = emission['year']
        for monthly in emission['monthly_emissions']:
            emissions_list.append({
                'facility_id': facility_id,
                'year': year,
                'month': monthly['month'],
                'emissions': monthly['value']
            })
    emissions_df = pd.DataFrame(emissions_list)
    
    # Convert forecasts to DataFrame
    forecasts_list = []
    for forecast in data['forecasts']:
        facility_id = forecast['facility_id']
        for f in forecast['forecasts']:
            forecasts_list.append({
                'facility_id': facility_id,
                'year': f['year'],
                'forecasted_emissions': f['value']
            })
    forecasts_df = pd.DataFrame(forecasts_list)
    
    # Convert regulatory requirements to DataFrames
    credit_limits_df = pd.DataFrame(data['regulatory_requirements']['credit_use_limits'])
    tightening_rates_df = pd.DataFrame(data['regulatory_requirements']['tightening_rates'])
    carbon_prices_df = pd.DataFrame(data['regulatory_requirements']['carbon_prices'])
    
    return {
        'facilities': facilities_df,
        'emissions': emissions_df,
        'forecasts': forecasts_df,
        'credit_limits': credit_limits_df,
        'tightening_rates': tightening_rates_df,
        'carbon_prices': carbon_prices_df
    }

def clean_emissions_data(data):
    """Clean the emissions data using linear interpolation, unit conversion, and duplicate removal"""
    # Convert emissions data to DataFrame
    emissions_df = data['emissions']
    
    # Create a month number mapping for proper sorting
    month_map = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    
    # Create a month number mapping for proper sorting
    all_months = pd.DataFrame([
        (facility_id, year, month_num, month)
        for facility_id in emissions_df['facility_id'].unique()
        for year in emissions_df['year'].unique()
        for month, month_num in month_map.items()
    ], columns=['facility_id', 'year', 'month_num', 'month'])
    
    # Add month number to emissions DataFrame
    emissions_df['month_num'] = emissions_df['month'].map(month_map)
    
    # Sort the data by facility, year, and month
    emissions_df = emissions_df.sort_values(['facility_id', 'year', 'month_num'])
    
    print("=== Data Cleaning Process ===\n")
    
    # 1. Remove duplicate entries
    print("1. Removing duplicate entries...")
    initial_rows = len(emissions_df)
    emissions_df = emissions_df.drop_duplicates(subset=['facility_id', 'year', 'month'], keep='first')
    duplicates_removed = initial_rows - len(emissions_df)
    print(f"Removed {duplicates_removed} duplicate entries")
    
    # 2. Identify values that may need unit conversion
    print("\n2. Analyzing potential unit inconsistencies...")
    facility_stats = emissions_df.groupby('facility_id')['emissions'].agg(['mean', 'std', 'min', 'max'])
    facility_stats['max_min_ratio'] = facility_stats['max'] / facility_stats['min']
    
    # Define thresholds for unit conversion
    mean_threshold = 1000000  # Values above 1 million might be in different units
    ratio_threshold = 2.0     # Max/min ratio above 2 might indicate unit issues
    
    facilities_needing_conversion = facility_stats[
        (facility_stats['mean'] > mean_threshold) | 
        (facility_stats['max_min_ratio'] > ratio_threshold)
    ]
    
    if not facilities_needing_conversion.empty:
        print("\nFacilities that may need unit conversion:")
        print(facilities_needing_conversion)
        
        # Apply unit conversion (example: convert to tCO2e if in kgCO2e)
        for facility_id in facilities_needing_conversion.index:
            if facility_stats.loc[facility_id, 'mean'] > mean_threshold:
                print(f"\nConverting {facility_id} from kgCO2e to tCO2e (dividing by 1000)")
                emissions_df.loc[emissions_df['facility_id'] == facility_id, 'emissions'] /= 1000
    else:
        print("No facilities identified as needing unit conversion")
    
    # 3. Handle missing values using linear interpolation
    print("\n3. Handling missing values with linear interpolation...")
    
    # Merge with original data to identify missing values
    complete_df = all_months.merge(
        emissions_df[['facility_id', 'year', 'month_num', 'emissions']],
        on=['facility_id', 'year', 'month_num'],
        how='left'
    )
    
    # Apply linear interpolation for each facility
    for facility_id in complete_df['facility_id'].unique():
        facility_data = complete_df[complete_df['facility_id'] == facility_id].copy()
        if facility_data['emissions'].isnull().any():
            print(f"\nInterpolating missing values for {facility_id}")
            print("Before interpolation:")
            print(facility_data[facility_data['emissions'].isnull()])
            
            # Perform linear interpolation
            facility_data['emissions'] = facility_data['emissions'].interpolate(method='linear')
            
            print("\nAfter interpolation:")
            print(facility_data[facility_data['emissions'].isnull()])
            
            # Update the main DataFrame
            complete_df.loc[complete_df['facility_id'] == facility_id, 'emissions'] = facility_data['emissions']
    
    # Clean up the final DataFrame
    final_df = complete_df.drop('month_num', axis=1)
    
    # Save the cleaned data
    output_path = Path(__file__).parent.parent / 'resources' / 'cleaned_emissions_data.json'
    
    # Convert back to the original JSON structure
    cleaned_data = {
        'facilities': data['facilities'].to_dict('records'),
        'emissions_data': [],
        'forecasts': data['forecasts'].to_dict('records'),
        'regulatory_requirements': {
            'credit_use_limits': data['credit_limits'].to_dict('records'),
            'tightening_rates': data['tightening_rates'].to_dict('records'),
            'carbon_prices': data['carbon_prices'].to_dict('records')
        }
    }
    
    # Convert the cleaned DataFrame back to the original format
    for facility_id in final_df['facility_id'].unique():
        facility_data = final_df[final_df['facility_id'] == facility_id]
        facility_emissions = {
            'facility_id': facility_id,
            'year': int(facility_data['year'].iloc[0]),  # Convert to Python int
            'monthly_emissions': [
                {
                    'month': row['month'],
                    'value': float(row['emissions'])  # Convert to Python float
                }
                for _, row in facility_data.iterrows()
            ]
        }
        cleaned_data['emissions_data'].append(facility_emissions)
    
    # Save the cleaned data
    with open(output_path, 'w') as f:
        json.dump(cleaned_data, f, indent=2)
    
    print(f"\nCleaned data saved to: {output_path}")
    
    # Print the cleaned data in a readable format
    print("\n=== Cleaned Data Summary ===")
    print("\nMonthly Emissions by Facility:")
    for facility_id in final_df['facility_id'].unique():
        print(f"\nFacility {facility_id}:")
        facility_data = final_df[final_df['facility_id'] == facility_id]
        print(facility_data[['month', 'emissions']].to_string(index=False))
    
    print("\nSummary Statistics by Facility:")
    print(final_df.groupby('facility_id')['emissions'].agg(['count', 'mean', 'std', 'min', 'max']).round(2))
    
    return final_df

def calculate_monthly_emissions(clean_activity_data, emission_factors):
    """Calculate monthly emissions for each facility and create separate graphs"""
    # Create month number mapping for proper sorting
    month_map = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    
    # Since clean_activity_data is already a DataFrame, we can use it directly
    emissions_df = clean_activity_data.copy()
    
    # Add month_num column for sorting
    emissions_df['month_num'] = emissions_df['month'].map(month_map)
    
    # Sort by facility, year, and month
    emissions_df = emissions_df.sort_values(['facility_id', 'year', 'month_num'])
    
    # Define colors for each facility
    colors = ['blue', 'red', 'green']
    
    # Create a separate figure for each facility
    for idx, facility_id in enumerate(emissions_df['facility_id'].unique()):
        # Create a new figure for each facility
        plt.figure(figsize=(12, 6))
        
        # Get data for this facility
        facility_data = emissions_df[emissions_df['facility_id'] == facility_id]
        
        # Create the plot
        plt.plot(facility_data['month'], facility_data['emissions'], 
                marker='o', color=colors[idx], linewidth=2, label=f'Facility {facility_id}')
        
        # Customize the plot
        plt.title(f'Monthly Emissions for Facility {facility_id} (2024)', fontsize=14, pad=20)
        plt.xlabel('Month', labelpad=10)
        plt.ylabel('Emissions (tCO2e)', labelpad=10)
        plt.grid(True)
        plt.legend(loc='upper right')
        
        # Set x-axis ticks to show all months
        plt.xticks(facility_data['month'], rotation=45)
        
        # Add more space at the bottom of the plot
        plt.margins(y=0.2)  # Add 20% padding to y-axis
        
        # Adjust layout
        plt.tight_layout()
        
        # Display the plot
        plt.show()
    
    # Print summary statistics
    print("\nMonthly Emissions Summary by Facility:")
    summary = emissions_df.groupby('facility_id').agg({
        'emissions': ['mean', 'std', 'min', 'max']
    }).round(2)
    print(summary)
    
    return emissions_df

def calculate_annual_emissions(monthly_emissions, regulatory_requirements):
    """Calculate annual emissions and compliance gaps for each facility"""
    # Calculate annual emissions by summing monthly emissions
    annual_emissions = monthly_emissions.groupby('facility_id')['emissions'].sum().reset_index()
    annual_emissions.columns = ['facility_id', 'annual_emissions']
    
    # Get compliance obligations from the data
    compliance_obligations = {
        'fac-001': 2550000,  # From the original data
        'fac-002': 4840000,
        'fac-003': 1530000
    }
    
    # Calculate compliance gaps
    annual_emissions['compliance_obligation'] = annual_emissions['facility_id'].map(compliance_obligations)
    annual_emissions['compliance_gap'] = annual_emissions['compliance_obligation'] - annual_emissions['annual_emissions']
    
    # Print results
    print("\n=== Annual Emissions and Compliance Analysis ===")
    for _, row in annual_emissions.iterrows():
        print(f"\nFacility {row['facility_id']}:")
        print(f"Annual Emissions: {row['annual_emissions']:,.2f} tCO2e")
        print(f"Compliance Obligation: {row['compliance_obligation']:,.2f} tCO2e")
        print(f"Compliance Gap: {row['compliance_gap']:,.2f} tCO2e")
        if row['compliance_gap'] > 0:
            print("Status: Compliant (Emissions below obligation)")
        else:
            print("Status: Non-compliant (Emissions above obligation)")
    
    return annual_emissions

def forecast_compliance_emissions(monthly_emissions):
    """Plot historical emissions and future forecasts from the sample data"""
    # Create month number mapping for proper sorting
    month_map = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
        'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    
    # Get future compliance obligations
    future_obligations = {
        'fac-001': [2422500, 2295000, 2167500, 2040000, 1912500],  # 2025-2029
        'fac-002': [4620000, 4400000, 4180000, 3960000, 3740000],
        'fac-003': [1453500, 1377000, 1300500, 1224000, 1147500]
    }
    
    # Get forecasts from sample data
    sample_forecasts = {
        'fac-001': [3103854, 3011364, 2810559, 3019652, 3018420],  # 2025-2029
        'fac-002': [5100000, 5200000, 5150000, 5300000, 5250000],
        'fac-003': [1550000, 1600000, 1580000, 1620000, 1590000]
    }
    
    # Create a figure with subplots for each facility
    fig, axes = plt.subplots(3, 1, figsize=(15, 15))
    fig.suptitle('Historical Emissions and Forecasts with Compliance Obligations', fontsize=12)
    plt.subplots_adjust(hspace=0.5)  
    
    # Create a dictionary to store compliance gaps
    compliance_gaps = {}
    
    # Process each facility
    for idx, facility_id in enumerate(monthly_emissions['facility_id'].unique()):
        # Get historical data for this facility
        facility_data = monthly_emissions[monthly_emissions['facility_id'] == facility_id].copy()
        facility_data['month_num'] = facility_data['month'].map(month_map)
        facility_data = facility_data.sort_values('month_num')
        
        # Calculate annual totals for historical data
        historical_annual = facility_data.groupby('year')['emissions'].sum()
        
        # Plot historical and forecasted data
        ax = axes[idx]
        # Plot forecasted annual emissions
        forecast_years = list(range(2025, 2030))
        ax.plot(forecast_years, sample_forecasts[facility_id], 
                'r--', label='Forecasted Annual Emissions', marker='s')
        
        # Plot historical annual emissions
        ax.plot(historical_annual.index, historical_annual.values, 
                'b-', label='Historical Annual Emissions', marker='o')
        
        plt.subplots_adjust(hspace=0.5)  
        
        # Plot compliance obligations
        ax.plot(forecast_years, future_obligations[facility_id], 
                'g--', label='Compliance Obligations', marker='^')
        
        # Customize the plot
        ax.set_title(f'Facility {facility_id}', fontsize=11, pad=-1)
        ax.set_xlabel('Year', labelpad=-10)
        ax.set_ylabel('Emissions (tCO2e)')
        ax.grid(True)
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        
        # Store compliance gaps for this facility
        compliance_gaps[facility_id] = []
        
        # Print forecast results and store compliance gaps
        print(f"\n=== Forecast Results for Facility {facility_id} ===")
        print("\nForecasted Annual Emissions:")
        for year, emissions in zip(forecast_years, sample_forecasts[facility_id]):
            print(f"{year}: {emissions:,.2f} tCO2e")
        
        print("\nCompliance Obligations:")
        for year, obligation in zip(forecast_years, future_obligations[facility_id]):
            print(f"{year}: {obligation:,.2f} tCO2e")
        
        print("\nCompliance Gaps:")
        for year, emissions, obligation in zip(forecast_years, sample_forecasts[facility_id], future_obligations[facility_id]):
            gap = obligation - emissions
            status = "Compliant" if gap > 0 else "Non-compliant"
            print(f"{year}: {gap:,.2f} tCO2e ({status})")
            
            # Store the compliance gap data
            compliance_gaps[facility_id].append({
                'year': year,
                'forecasted_emissions': float(emissions),
                'compliance_obligation': float(obligation),
                'compliance_gap': float(gap),
                'status': status
            })
    
    plt.tight_layout()
    plt.show()
    
    # Load the existing cleaned data
    output_path = Path(__file__).parent.parent / 'resources' / 'cleaned_emissions_data.json'
    with open(output_path, 'r') as f:
        cleaned_data = json.load(f)
    
    # Add compliance gaps to the cleaned data
    cleaned_data['compliance_gaps'] = compliance_gaps
    
    # Save the updated data
    with open(output_path, 'w') as f:
        json.dump(cleaned_data, f, indent=2)
    
    print(f"\nCompliance gaps have been saved to {output_path}")
    
    return forecast_years, sample_forecasts, future_obligations

def plot_compliance_gaps():
    """Plot credit requirements for each facility from 2024-2029"""
    # Load the cleaned data with compliance gaps
    output_path = Path(__file__).parent.parent / 'resources' / 'cleaned_emissions_data.json'
    with open(output_path, 'r') as f:
        data = json.load(f)
    
    # Get 2024 compliance obligations
    compliance_obligations_2024 = {
        'fac-001': 2550000,  # From the original data
        'fac-002': 4840000,
        'fac-003': 1530000
    }
    
    # Create a figure with subplots for each facility
    fig, axes = plt.subplots(3, 1, figsize=(15, 15))
    fig.suptitle('Credit Requirements by Facility (2024-2029)', fontsize=14, y=0.95)
    
    # Define colors for each facility
    colors = ['blue', 'red', 'green']
    
    # Create lists to store data for the status plot
    all_years = []
    all_facilities = []
    all_statuses = []
    
    # Process each facility
    for idx, facility_id in enumerate(data['compliance_gaps'].keys()):
        ax = axes[idx]
        
        # Get compliance gaps for this facility
        gaps_data = data['compliance_gaps'][facility_id]
        
        # Calculate 2024 gap from annual emissions
        facility_2024_data = next((item for item in data['emissions_data'] 
                                 if item['facility_id'] == facility_id and item['year'] == 2024), None)
        annual_emissions_2024 = sum(month['value'] for month in facility_2024_data['monthly_emissions']) if facility_2024_data else 0
        gap_2024 = annual_emissions_2024 - compliance_obligations_2024[facility_id]  # Flipped sign
        
        # Combine 2024 with future gaps
        years = [2024] + [gap['year'] for gap in gaps_data]
        gaps = [gap_2024] + [-gap['compliance_gap'] for gap in gaps_data]  # Flipped sign
        
        # Store data for status plot
        all_years.extend(years)
        all_facilities.extend([facility_id] * len(years))
        all_statuses.extend([1 if gap > 0 else 0 for gap in gaps])  # 1 for required, 0 for available
        
        # Create the line plot
        line = ax.plot(years, gaps, color=colors[idx], marker='o', linewidth=2, markersize=8)
        
        # Add value labels above/below each point
        for x, y in zip(years, gaps):
            ax.text(x, y, f'{y:,.0f}',
                   ha='center', va='bottom' if y > 0 else 'top',
                   fontsize=9)
        
        # Add a horizontal line at y=0
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        
        # Customize the plot
        ax.set_title(f'Facility {facility_id}', fontsize=12, pad=10)
        ax.set_xlabel('Year', labelpad=10)
        ax.set_ylabel('Credit Requirements (tCO2e)', labelpad=10)
        ax.grid(True, alpha=0.3)
        
        # Set x-axis ticks to show all years
        ax.set_xticks(years)
        
        # Add more space at the bottom of the plot
        ax.margins(y=0.2)
    
    # Add a legend explaining the credit requirements
    fig.text(1.02, 0.5, 
             'Positive values: Credits Required\n(Emissions > Obligation)\n\nNegative values: Credits Available\n(Emissions < Obligation)',
             ha='left', va='center', fontsize=10, 
             bbox=dict(facecolor='white', edgecolor='gray', alpha=0.8))
    
    # Adjust layout to make room for the legend
    plt.subplots_adjust(right=0.85)
    plt.show()
    
    # Create a separate figure for compliance status with subplots
    status_fig, status_axes = plt.subplots(3, 1, figsize=(12, 12))
    status_fig.suptitle('Compliance Status by Year', fontsize=14, y=1)
    
    # Create a DataFrame for the status data
    status_df = pd.DataFrame({
        'Year': all_years,
        'Facility': all_facilities,
        'Status': all_statuses
    })
    
    # Define colors for each facility
    facility_colors = {
        'fac-001': 'blue',
        'fac-002': 'red',
        'fac-003': 'green'
    }
    
    # Plot status for each facility in its own subplot
    for idx, facility_id in enumerate(data['compliance_gaps'].keys()):
        ax = status_axes[idx]
        
        # Get data for this facility
        facility_data = status_df[status_df['Facility'] == facility_id]
        
        # Create the status plot
        ax.plot(facility_data['Year'], facility_data['Status'],
                color=facility_colors[facility_id], marker='o', linewidth=2, markersize=8)
        
        # Customize the plot
        ax.set_title(f'Facility {facility_id}', fontsize=12, pad=10)
        ax.set_xlabel('Year', labelpad=10)
        ax.set_ylabel('Status', labelpad=10)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(['Compliant', 'Non-compliant'])
        ax.grid(True, alpha=0.3)
        
        # Set x-axis ticks to show all years
        ax.set_xticks(facility_data['Year'])
        
        # Add more space at the bottom of the plot
        ax.margins(y=0.2)
    
    # Adjust layout
    plt.tight_layout()
    plt.show()

def main():
    # Load the data
    data = load_data()
    
    # Print some basic information about the data
    print("\nFacilities:")
    print(data['facilities'].head())
    
    print("\nEmissions Data:")
    print(data['emissions'].head())
    
    print("\nForecasts:")
    print(data['forecasts'].head())
    
    print("\nRegulatory Requirements:")
    print("Credit Use Limits:")
    print(data['credit_limits'])
    print("\nTightening Rates:")
    print(data['tightening_rates'])
    print("\nCarbon Prices:")
    print(data['carbon_prices'])
    
    # Clean the data
    print("\n=== Starting Data Cleaning Process ===")
    cleaned_data = clean_emissions_data(data)
    
    # Calculate and display monthly emissions
    print("\n=== Calculating Monthly Emissions ===")
    monthly_emissions = calculate_monthly_emissions(cleaned_data, None)
    
    # Calculate annual emissions and compliance
    print("\n=== Calculating Annual Emissions and Compliance ===")
    annual_emissions = calculate_annual_emissions(monthly_emissions, None)
    
    # Forecast future emissions
    print("\n=== Forecasting Future Emissions ===")
    forecast_compliance_emissions(monthly_emissions)
    
    # Plot compliance gaps
    print("\n=== Plotting Compliance Gaps ===")
    plot_compliance_gaps()

if __name__ == "__main__":
    main()