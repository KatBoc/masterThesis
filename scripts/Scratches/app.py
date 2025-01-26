from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Load the CSV data
DATA_FILE = "data.csv"  # Path to your CSV file
data = pd.read_csv(DATA_FILE)


@app.route("/", methods=["GET", "POST"])
def index():
    # Extract filter options
    countries = sorted(data["Country"].unique())
    sectors = sorted(data["Sector"].unique())
    gases = sorted(data["Gas"].unique())

    # Default filters
    selected_country = request.form.get("country", "all")
    selected_sector = request.form.get("sector", "all")
    selected_gas = request.form.get("gas", "all")

    # Filter data based on user input
    filtered_data = data.copy()
    if selected_country != "all":
        filtered_data = filtered_data[
            filtered_data["Country"] == selected_country]
    if selected_sector != "all":
        filtered_data = filtered_data[
            filtered_data["Sector"] == selected_sector]
    if selected_gas != "all":
        filtered_data = filtered_data[filtered_data["Gas"] == selected_gas]

    # Prepare data for plotting
    years = [str(year) for year in range(1990, 2022)]
    aggregated_data = filtered_data[years].sum()

    # Generate chart
    chart_url = generate_chart(years, aggregated_data)

    return render_template(
        "index.html",
        countries=countries,
        sectors=sectors,
        gases=gases,
        selected_country=selected_country,
        selected_sector=selected_sector,
        selected_gas=selected_gas,
        chart_url=chart_url
    )


def generate_chart(years, values):
    """Generate a line chart and return it as a base64 string."""
    plt.figure(figsize=(10, 6))
    plt.plot(years, values, marker="o", color="blue")
    plt.title("GHG Emissions Over Time")
    plt.xlabel("Year")
    plt.ylabel("Emissions (Mt CO2e)")
    plt.grid(True)

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    # Encode the BytesIO object as a base64 string
    return base64.b64encode(buf.getvalue()).decode("utf-8")


if __name__ == "__main__":
    app.run(debug=True)
