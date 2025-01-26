from scripts.ETL.co2analytics import CO2Analytics

CO2Analytics = CO2Analytics()
CO2Analytics.run()
print(CO2Analytics.transformed_data)