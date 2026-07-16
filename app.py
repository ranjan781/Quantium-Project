import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load the data
df = pd.read_csv("formatted_output.csv")

# Convert Date column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Sort by date
df = df.sort_values("Date")

# Create Dash app
app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(
            "Pink Morsel Sales Dashboard",
            style={"textAlign": "center"}
        ),

        html.P(
            "Analyse sales before and after the price increase on 15 January 2021.",
            style={"textAlign": "center"}
        ),

        dcc.Dropdown(
            id="region-dropdown",
            options=[
                {"label": "All Regions", "value": "All"}
            ] + [
                {"label": region.title(), "value": region}
                for region in sorted(df["Region"].unique())
            ],
            value="All",
            clearable=False,
            style={"width": "50%", "margin": "auto"}
        ),

        dcc.Graph(id="sales-chart")
    ]
)


@app.callback(
    Output("sales-chart", "figure"),
    Input("region-dropdown", "value")
)
def update_chart(selected_region):

    if selected_region == "All":
        filtered_df = df
    else:
        filtered_df = df[df["Region"] == selected_region]

    chart = (
        filtered_df.groupby("Date", as_index=False)["Sales"]
        .sum()
    )

    fig = px.line(
        chart,
        x="Date",
        y="Sales",
        title="Pink Morsel Sales Over Time"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales ($)",
        template="plotly_white"
    )

    fig.add_vline(
        x="2021-01-15",
        line_dash="dash",
        line_color="red",
        annotation_text="Price Increase",
        annotation_position="top left"
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)