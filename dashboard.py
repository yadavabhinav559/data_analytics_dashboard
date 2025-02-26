import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load dataset
from sqlalchemy import create_engine
import pandas as pd

# Database connection
DB_URL = "postgresql://postgres:0@localhost/business_db"


def fetch_data():
    engine = create_engine(DB_URL)
    query = "SELECT * FROM kpi_data ORDER BY date ASC"
    df = pd.read_sql(query, engine)

    print("✅ Data Loaded from PostgreSQL")
    print(df.head())  # Print first few rows for debugging
    print("Columns in DataFrame:", df.columns.tolist())  # Debugging line
    return df


df = fetch_data()
df["date"] = pd.to_datetime(df["date"])

# Custom Apple-style font (Google Fonts alternative to SF Pro Display)
APPLE_FONT = {"fontFamily": "'Inter', sans-serif"}  # Inter is close to SF Pro Display

# Initialize Dash app with Bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.LUX,  # Main theme
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap",  # Inter font
    ],
)
# Define Layout
app.layout = dbc.Container(
    [
        # Navbar with reduced spacing
        dbc.NavbarSimple(
            brand="📊 Business Insights",
            brand_href="#",
            color="dark",
            dark=True,
            style={
                "fontSize": "24px",
                "fontWeight": "bold",
                "padding": "10px",
                **APPLE_FONT,
            },
        ),
        # Hero Section with reduced whitespace
        html.Div(
            [
                html.H1(
                    "📈 Gain Deeper Insights",
                    className="text-center",
                    style={"marginBottom": "10px", **APPLE_FONT},
                ),
                html.P(
                    "Discover trends in revenue, expenses, and profits with interactive visualizations.",
                    className="text-center lead",
                    style={"marginBottom": "20px", **APPLE_FONT},
                ),
            ],
            style={"textAlign": "center", "padding": "20px 0"},  # Reduced padding
        ),
        # Filters section with reduced gaps
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Label(
                                    "📅 Select date Range:",
                                    style={"fontWeight": "bold", **APPLE_FONT},
                                ),
                                dcc.DatePickerRange(
                                    id="date-picker",
                                    min_date_allowed=df["date"].min(),
                                    max_date_allowed=df["date"].max(),
                                    start_date=df["date"].min(),
                                    end_date=df["date"].max(),
                                    display_format="MMM D, YYYY",
                                    className="mb-3",
                                ),
                            ]
                        ),
                        className="shadow p-2 mb-2 bg-light",
                        style={"borderRadius": "12px"},
                    ),
                    md=6,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Label(
                                    "� Select KPI to Display:",
                                    style={"fontWeight": "bold", **APPLE_FONT},
                                ),
                                dcc.Dropdown(
                                    id="kpi-dropdown",
                                    options=[
                                        {
                                            "label": "Revenue",
                                            "value": "revenue",
                                        },  # Use lowercase values
                                        {"label": "Expenses", "value": "expenses"},
                                        {"label": "Profit", "value": "profit"},
                                        {
                                            "label": "Customer Count",
                                            "value": "customer_count",
                                        },
                                    ],
                                    value=[
                                        "revenue",
                                        "expenses",
                                        "profit",
                                    ],  # Default selection with lowercase
                                    multi=True,
                                    className="mb-3",
                                ),
                            ]
                        ),
                        className="shadow p-2 mb-2 bg-light",
                        style={"borderRadius": "12px"},
                    ),
                    md=6,
                ),
            ],
            className="mb-2",  # Reduced bottom margin
        ),
        # Graph section with white background
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4(
                        "📊 Business KPIs Over Time",
                        className="card-title",
                        style=APPLE_FONT,
                    ),
                    dcc.Graph(id="kpi-graph"),
                ]
            ),
            className="shadow mb-3",
            style={"borderRadius": "12px", "backgroundColor": "#ffffff"},
        ),
    ],
    fluid=True,
)


@app.callback(
    Output("kpi-graph", "figure"),
    [
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
        Input("kpi-dropdown", "value"),
    ],
)
def update_graph(start_date, end_date, selected_kpis):
    df = fetch_data()

    # Ensure 'date' column is in datetime format
    df["date"] = pd.to_datetime(df["date"])

    # Filter data based on selected date range
    filtered_df = df[(df["date"] >= start_date) & (df["date"] <= end_date)]

    # Debugging print statements
    print(f"Selected KPIs: {selected_kpis}")
    print(filtered_df.head())  # Print first few rows to check

    # Ensure selected_kpis is a list
    if isinstance(selected_kpis, str):
        selected_kpis = [selected_kpis]

    # Ensure selected KPIs exist in the DataFrame
    valid_kpis = [kpi for kpi in selected_kpis if kpi in filtered_df.columns]

    if not valid_kpis:
        print("⚠️ No valid KPIs selected!")  # Debugging message
        return px.line(title="No data available")

    # Create figure with valid KPIs
    fig = px.line(
        filtered_df,
        x="date",
        y=valid_kpis,
        title="Business KPIs Over Time",
        template="plotly_white",
    )

    return fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
