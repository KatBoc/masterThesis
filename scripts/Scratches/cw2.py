import plotly.graph_objects as go
import pandas as pd

# Load your data
data = pd.read_csv('../../Data/CW_HistoricalEmissions_ClimateWatch.csv')  # Replace with your actual CSV file path

# Melt the data for easier plotting
data_melted = data.melt(id_vars=['Country', 'Source', 'Sector', 'Gas'],
                        value_vars=[str(year) for year in range(1990, 2022)],
                        var_name='Year', value_name='Value')

# Convert 'Year' to integer
data_melted['Year'] = data_melted['Year'].astype(int)

# Create a figure
fig = go.Figure()

# Add traces for each sector and country combination
sectors = data_melted['Sector'].unique()
countries = data_melted['Country'].unique()

# Add a trace for each sector and country combination
for sector in sectors:
    for country in countries:
        df_filtered = data_melted[(data_melted['Sector'] == sector) & (data_melted['Country'] == country)]
        fig.add_trace(go.Scatter(x=df_filtered['Year'], y=df_filtered['Value'],
                             mode='lines+markers', name=f'{country} - {sector}',
                             visible=False))  # Set initial visibility to False

# Define the dropdown buttons for sectors and countries
sector_buttons = []
country_buttons = []

# Add dropdown for sectors (including "For all" option)
sector_buttons.append({
    'label': 'For all',
    'method': 'update',
    'args': [{'visible': [True for _ in fig.data]},  # Make all traces visible
             {'title': 'All Sectors'}]
})

for sector in sectors:
    sector_buttons.append({
        'label': sector,
        'method': 'update',
        'args': [{'visible': [True if sector == trace.name.split(' - ')[1] else False for trace in fig.data]},  # Show only selected sector
                 {'title': f'Sector: {sector}'}]
    })

# Add dropdown for countries (including "For all" option)
country_buttons.append({
    'label': 'For all',
    'method': 'update',
    'args': [{'visible': [True for _ in fig.data]},  # Make all traces visible
             {'title': 'All Countries'}]
})

for country in countries:
    country_buttons.append({
        'label': country,
        'method': 'update',
        'args': [{'visible': [True if country == trace.name.split(' - ')[0] else False for trace in fig.data]},  # Show only selected country
                 {'title': f'Country: {country}'}]
    })

# Add both dropdowns to the figure layout
fig.update_layout(
    title='Select a Country and Sector to View Data',
    updatemenus=[
        {
            'buttons': sector_buttons,
            'direction': 'down',
            'showactive': True,
            'active': 0,  # Default sector dropdown selection
            'x': 0.1,
            'xanchor': 'left',
            'y': 1.15,
            'yanchor': 'top'
        },
        {
            'buttons': country_buttons,
            'direction': 'down',
            'showactive': True,
            'active': 0,  # Default country dropdown selection
            'x': 0.1,
            'xanchor': 'left',
            'y': 1.05,
            'yanchor': 'top'
        }
    ],
    title_x=0.5
)


fig.write_html('interactive_plot.html')
print('finished')