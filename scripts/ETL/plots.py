import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def plot(df):
    df = df.drop(columns=["subsector"], inplace=True)
    df_melted = df.melt(id_vars=["sector", "year"],
                        var_name="EnergyType",
                        value_name="Value")

    # Create line plot with dropdown
    fig = px.line(
        df_melted,
        x="year",
        y="Value",
        color="EnergyType",
        title="Zużycie energii według sektora",
    )

    fig.update_layout(
        updatemenus=[
            {
                "buttons": [
                    {
                        "label": sector,
                        "method": "update",
                        "args": [
                            {"visible": df_melted["Sector"] == sector},
                            {"title": f"Zużycie energii w sektorze {sector}"},
                        ],
                    }
                    for sector in df["Sector"].unique()
                ],
                "direction": "down",
                "showactive": True,
            }
        ]
    )

    fig.write_html("wykres.html")

def print_head(df):
    print(df)

