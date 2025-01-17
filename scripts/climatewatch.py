import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Read your CSV data
data = pd.read_csv('../Data/Raw/ClimateWatch_HistoricalEmissions/CW_HistoricalEmissions_ClimateWatch.csv')  # Replace with your actual CSV file path

data_melted = data.melt(id_vars=['Country', 'Source', 'Sector', 'Gas'],
                        value_vars=[str(year) for year in range(1990, 2022)],
                        var_name='Year', value_name='Value')

data_melted['Year'] = data_melted['Year'].astype(int)

fig = go.Figure()

sectors = data_melted['Sector'].unique()
countries = data_melted['Country'].unique()

for sector in sectors:
    for country in countries:
        df_filtered = data_melted[(data_melted['Sector'] == sector) & (data_melted['Country'] == country)]
        fig.add_trace(go.Scatter(x=df_filtered['Year'], y=df_filtered['Value'],
                             mode='lines+markers', name=f'{country} - {sector}',
                             visible=False))  # Set initial visibility to False

sector_buttons = []
country_buttons = []

for sector in sectors:
    sector_buttons.append({
        'label': sector,
        'method': 'update',
        'args': [{'visible': [True if sector == trace.name.split(' - ')[1] else False for trace in fig.data]},  # Make the selected sector visible
                 {'title': f'Sector: {sector}'}]
    })

for country in countries:
    country_buttons.append({
        'label': country,
        'method': 'update',
        'args': [{'visible': [True if country == trace.name.split(' - ')[0] else False for trace in fig.data]},  # Make the selected country visible
                 {'title': f'Country: {country}'}]
    })

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

fig.write_html('output_plot.html')

print('finished')