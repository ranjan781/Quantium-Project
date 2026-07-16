import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------
df = pd.read_csv("formatted_output.csv")

df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# ---------------------------------------------------
# Dash App
# ---------------------------------------------------
app = Dash(__name__)
app.title = "Soul Foods Dashboard"

# ---------------------------------------------------
# Layout
# ---------------------------------------------------
app.layout = html.Div(

    style={
        "backgroundColor": "#F4F7FC",
        "padding": "30px 60px",
        "fontFamily": "Segoe UI",
        "maxWidth": "1700px",
        "margin": "auto",
    },

    children=[

        html.H1(
            "🍬 Soul Foods Pink Morsel Sales Dashboard",
            style={
                "textAlign": "center",
                "color": "#2C3E50",
                "fontSize": "42px",
                "fontWeight": "bold",
            },
        ),

        html.P(
            "Interactive dashboard showing Pink Morsel sales before and after the 15 January 2021 price increase.",
            style={
                "textAlign": "center",
                "fontSize": "18px",
                "color": "#555",
                "marginBottom": "35px",
            },
        ),

        html.Div(

            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "15px",
                "boxShadow": "0px 4px 12px rgba(0,0,0,0.15)",
                "marginBottom": "30px",
            },

            children=[

                html.Label(
                    "Select Region",
                    style={
                        "fontWeight": "bold",
                        "fontSize": "22px",
                        "marginBottom": "15px",
                        "display": "block",
                    },
                ),

                dcc.RadioItems(

                    id="region-radio",

                    options=[
                        {"label": " All", "value": "all"},
                        {"label": " North", "value": "north"},
                        {"label": " East", "value": "east"},
                        {"label": " South", "value": "south"},
                        {"label": " West", "value": "west"},
                    ],

                    value="all",

                    inline=True,

                    labelStyle={
                        "marginRight": "30px",
                        "fontSize": "18px",
                        "cursor": "pointer",
                    },
                ),

            ],
        ),

        dcc.Graph(
            id="sales-chart",
            style={
                "height": "750px",
                "width": "100%",
            },
        ),
    ],
)

# ---------------------------------------------------
# Callback
# ---------------------------------------------------
@app.callback(
    Output("sales-chart", "figure"),
    Input("region-radio", "value"),
)
def update_chart(region):

    if region == "all":
        filtered = df.copy()
    else:
        filtered = df[df["Region"] == region]

    # Monthly Sales
    chart = (
        filtered
        .set_index("Date")
        .resample("ME")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        chart,
        x="Date",
        y="Sales",
        markers=True,
        title="Monthly Pink Morsel Sales",
    )

    fig.update_traces(
        line=dict(color="#E91E63", width=4),
        marker=dict(size=5),
    )

    # Price Increase Line
    fig.add_vline(
        x="2021-01-15",
        line_dash="dash",
        line_color="red",
        line_width=3,
        annotation_text="Price Increase",
        annotation_position="top left",
    )

    fig.update_layout(

        height=700,

        plot_bgcolor="white",
        paper_bgcolor="#F4F7FC",

        hovermode="x unified",

        font=dict(size=15),

        title={
            "x": 0.5,
            "font": {"size": 28},
        },

        margin=dict(
            l=40,
            r=40,
            t=80,
            b=40,
        ),

        xaxis=dict(
            title="Date",
            tickformat="%b\n%Y",

            rangeselector=dict(
                buttons=[
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(count=2, label="2Y", step="year", stepmode="backward"),
                    dict(step="all"),
                ]
            ),

            rangeslider=dict(visible=True),

            showgrid=True,
            gridcolor="#ECECEC",
        ),

        yaxis=dict(
            title="Sales ($)",
            showgrid=True,
            gridcolor="#ECECEC",
        ),
    )

    return fig


# ---------------------------------------------------
# Run
# ---------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)