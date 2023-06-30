import pandas as pd
import plotly.express as px
from flask import Flask, render_template
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np

# Create the Flask app and Dash app
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.UNITED, dbc.icons.BOOTSTRAP])

# Read the data from CSV files
df = pd.read_csv('dataset.csv')
df2 = pd.read_csv('count.csv')
dtf = pd.read_csv('test.csv')

# Define the components and plots

# Header component
Header_component = html.H1("Main Dashboard", style={"text-align": "center", "color": "Grey", "font-size": "50px",
                                                     "font-family": "Times New Roman"})

# Time-Concentration Overview Plot
countfig = go.FigureWidget()
countfig.add_scatter(name="Treatment A", x=df2['Time'], y=df2['Concentration'], fill='tozeroy', line_shape='spline')
countfig.add_scatter(name="Treatment B", x=df2['Time'], y=df2['Conc2'], fill='tozeroy', line_shape='spline')
countfig.update_layout(title="Time vs. Concentration", xaxis_title="Time (h)", yaxis_title="Concentration (ng/mL)",
                       plot_bgcolor="rgba(0, 0, 0, 0)", paper_bgcolor="rgba(0, 0, 0, 0)",
                       width=400,  # Set the width of the plot
    height=300)  # Set the height of the plot)


# Parameters Overview Plot
countfig_cum = go.FigureWidget()
# countfig_cum.add_scatter(name="100 mg", x=dtf['TIME'], y=df['CONCENTRATION'], mode='lines+markers', line_shape='spline')
# countfig_cum.add_scatter(name="200 mg", x=dtf['dose'], y=df['part'], mode='lines+markers', line_shape='spline')
dose = 100
dose2=200
subjects = dtf[dtf['DOSE'] == dose]['SUBJECT'].unique()
subjects2 = dtf[dtf['DOSE'] == dose2]['SUBJECT'].unique()
for subject in subjects:
    countfig_cum.add_scatter(name=subject,
                             x=dtf[(dtf['DOSE'] == dose) & (dtf['SUBJECT'] == subject)]['TIME'],
                             y=dtf[(dtf['DOSE'] == dose) & (dtf['SUBJECT'] == subject)]['CONCENTRATION'],
                             mode='lines+markers',
                             line_shape='spline')
for subject in subjects2:
    countfig_cum.add_scatter(name=subject,
                             x=dtf[(dtf['DOSE'] == dose2) & (dtf['SUBJECT'] == subject)]['TIME'],
                             y=dtf[(dtf['DOSE'] == dose2) & (dtf['SUBJECT'] == subject)]['CONCENTRATION'],
                             mode='lines+markers',
                             line_shape='spline')
countfig_cum.update_layout(title="Individual Profiles", xaxis_title="Time (h)", yaxis_title="Concentration (ng/mL)",
                           plot_bgcolor="rgba(0, 0, 0, 0)", paper_bgcolor="rgba(0, 0, 0, 0)",width=400,  # Set the width of the plot
    height=300,legend=dict(
        font=dict(
            size=10  # Adjust the font size of the legend
        )
    ))  # Set the height of the plot))

# Individual Profiles Plot
cus = go.FigureWidget()
x0 = np.random.randn(100)
x1 = np.random.randn(100) + 1
cus = go.Figure()
cus.add_trace(go.Histogram(
    x=x0,
    histnorm='percent',
    name='Control',
    xbins=dict(start=-4.0, end=3.0, size=0.5),
    marker_color='#EB89B5',
    opacity=0.75
))
cus.add_trace(go.Histogram(
    x=x1,
    histnorm='percent',
    name='Experimental',
    xbins=dict(start=-3.0, end=4, size=0.5),
    marker_color='#330C73',
    opacity=0.75
))
cus.update_layout(
    title='Results',
    xaxis_title_text='Value',
    yaxis_title_text='Count',
    bargap=0.2,
    bargroupgap=0.1,
    plot_bgcolor="rgba(0, 0, 0, 0)",
    paper_bgcolor="rgba(0, 0, 0, 0)",
    legend_title_text='Treatment',
    width=400,  # Set the width of the plot
    height=300)  # Set the height of the plot)


# Correlation Analysis Plot
figg = go.FigureWidget()
figg = px.histogram(df, x="parameter", y="concentration", color="type")
figg.update_layout(title="Parameters by Type", xaxis_title="", yaxis_title="",
                   plot_bgcolor="rgba(0, 0, 0, 0)", paper_bgcolor="rgba(0, 0, 0, 0)",
                   legend_title_text='', bargap=0.2,width=400,  # Set the width of the plot
    height=300)  # Set the height of the plot))

pirgif = go.FigureWidget(
    px.pie(
        labels=["Treatment A","Treatment B"],
        values=[df2['Concentration'].sum(),df2['Conc2'].sum()],
        hole= 0.4
    ))
pirgif.update_layout(title = "Total concentration of the two treatments",plot_bgcolor="rgba(0, 0, 0, 0)",
                    paper_bgcolor="rgba(0, 0, 0, 0)",width=400,  # Set the width of the plot
    height=300)  # Set the height of the plot))

sidebar = html.Div(
    [
        html.Div(
            style={
                "background-color": "#a14842",
                "padding": "20px",  # Adjust padding as needed
                "text-align": "center",
            },
            children=[
                html.H2(
                    "Dashboard",
                    style={"color": "white", "font-size": "18px", "margin": "0"},
                )
            ]
        ),
       html.Div(
            children=[
                
            
        dbc.Nav(
            [
                dbc.NavLink("Compound Selection", href="/compound_selection", active="exact"),
                dbc.NavLink("Patient Data", href="/patient_data", active="exact"),
                dbc.NavLink("Clinical Trial Data", href="/clinical_trial_data", active="exact"),
                dbc.NavLink("PK/PD Data", href="/pk_pd_data", active="exact"),
                dbc.NavLink("Regulatory & Compliance", href="/regulatory_compliance", active="exact"),
                dbc.NavLink("Market Research & Sales Data", href="/market_research_sales_data", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        html.P(
            "Enter the Compound ID for detailed view:", style={"font-size": "13px"}
        ),
        dcc.Input(
            id="input_box",
            placeholder="Enter ID...",
            style={"width": "150px", "height": "30px", "margin-top": "0px","font-size": "13px"}
        ),

       dcc.Dropdown(
            id="treatment_dropdown",
            options=[
                {"label": "Treatment A", "value": "A"},
                {"label": "Treatment B", "value": "B"},
                # ... other treatment options
            ],
            placeholder="Treatment",
            style={"margin-top": "10px","width": "150px", "height": "30px","font-size": "13px","margin-bottom": "150px"}
        )
    ],
    style={"margin-top": "0px",
    "background-color": "#FFCCCC","padding": "10px"})]
)


# Define the app layout
app.layout = html.Div(style={"background-image": "url('assets/background2.jpg')"}, children=[
    dbc.Row([
        dbc.Col(sidebar, width=2),  # Sidebar
        dbc.Col([  # Rest of your content
            dbc.Row([
                dbc.Row([""], style={"margin-top": "10px"}),
                dbc.Col(dbc.NavLink("Main Dashboard", href="/", external_link=True, className="my-custom-link")),
                dbc.Col(dbc.NavLink("Time-Concentration", href="/time_concentration", external_link=True, className="my-custom-link")),
                dbc.Col(dbc.NavLink("Parameters", href="/parameters_overview", external_link=True, className="my-custom-link")),
                dbc.Col(dbc.NavLink("Individual Profiles", href="/individual_profiles", external_link=True, className="my-custom-link")),
                dbc.Col(dbc.NavLink("Correlation Analysis", href="/correlation_analysis", external_link=True, className="my-custom-link")),
                 dbc.Row([""], style={"margin-top": "5px"}),
                  html.Hr(),
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(figure=countfig)]),
                dbc.Col([dcc.Graph(figure=countfig_cum)])
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(figure=figg)]),
                dbc.Col([dcc.Graph(figure=cus)]),
                dbc.Col([dcc.Graph(figure=pirgif)])
            ]),
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content')
        ], width=10),
    ]),
])



# Callback to render the selected page based on the URL
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return Header_component
    elif pathname == '/time_concentration':
        return dcc.Graph(figure=countfig)
    elif pathname == '/parameters_overview':
        return dcc.Graph(figure=countfig_cum)
    elif pathname == '/individual_profiles':
        return dcc.Graph(figure=cus)
    elif pathname == '/correlation_analysis':
        return dcc.Graph(figure=figg)
    else:
        return '404 Page not found' # You can modify this as needed

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)


