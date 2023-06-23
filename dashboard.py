import pandas as pd
import plotly.express as px
from flask import Flask, render_template
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np


server = Flask(__name__)
app = dash.Dash(__name__,server = server,external_stylesheets=[dbc.themes.UNITED,dbc.icons.BOOTSTRAP])


df = pd.read_csv('dataset.csv')
df2 = pd.read_csv('count.csv')


Header_component = html.H1("PK/PD Dashboard",style = {"text-align":"center","color":"Grey","font-size":"50px","font-family":"Times New Roman"})

countfig = go.FigureWidget()

countfig.add_scatter(name = "Treatment A",x = df2['Time'],y = df2['Concentration'],fill = 'tozeroy',line_shape='spline')
countfig.add_scatter(name = "Treatment B",x = df2['Time'],y = df2['Conc2'],fill = 'tozeroy',line_shape='spline')

countfig.update_layout(title = "Time versus Concentration",
                       xaxis_title = "Time (h)",
                       yaxis_title = "Concentration (ng/mL)",
                       plot_bgcolor="rgba(0, 0, 0, 0)",
                    paper_bgcolor="rgba(0, 0, 0, 0)")


#comp2

countfig_cum = go.FigureWidget()

countfig_cum.add_scatter(name = "Period",x = df['dose'],y = df['period'],mode='lines+markers',line_shape='spline')
countfig_cum.add_scatter(name = "Part",x = df['dose'],y = df['part'],mode='lines+markers',line_shape='spline')

countfig_cum.update_layout(title = "Dose versus Concentration",xaxis_title = "Dose (mg)",yaxis_title = "Part/Period",
                           plot_bgcolor="rgba(0, 0, 0, 0)",
                    paper_bgcolor="rgba(0, 0, 0, 0)")

#com3
cus= go.FigureWidget()

x0 = np.random.randn(100)
x1 = np.random.randn(100) + 1

cus = go.Figure()
cus.add_trace(go.Histogram(
    x=x0,
    histnorm='percent',
    name='Control', # name used in legend and hover labels
    xbins=dict( # bins used for histogram
        start=-4.0,
        end=3.0,
        size=0.5
    ),
    marker_color='#EB89B5',
    opacity=0.75
))
cus.add_trace(go.Histogram(
    x=x1,
    histnorm='percent',
    name='Experimental',
    xbins=dict(
        start=-3.0,
        end=4,
        size=0.5
    ),
    marker_color='#330C73',
    opacity=0.75
))

cus.update_layout(
    title='Results', # title of plot
    xaxis_title_text='Value', # xaxis label
    yaxis_title_text='Count', # yaxis label
    bargap=0.2, # gap between bars of adjacent location coordinates
    bargroupgap=0.1, # gap between bars of the same location coordinates
     plot_bgcolor="rgba(0, 0, 0, 0)",
    paper_bgcolor="rgba(0, 0, 0, 0)"
)

#comp4
fig = go.FigureWidget()
fig = px.histogram(df, x="parameter", y="concentration", color="type")

fig.update_layout(title = "Parameters by Type",
                       xaxis_title = "",yaxis_title = "",
                       plot_bgcolor="rgba(0, 0, 0, 0)",
                    paper_bgcolor="rgba(0, 0, 0, 0)",legend_title_text='',bargap=0.2)
#com5
pirgif = go.FigureWidget(
    px.pie(
        labels=["Treatment A","Treatment B"],
        values=[df2['Concentration'].sum(),df2['Conc2'].sum()],
        hole= 0.4
    ))
pirgif.update_layout(title = "Total concentration of the two treatments",plot_bgcolor="rgba(0, 0, 0, 0)",
                    paper_bgcolor="rgba(0, 0, 0, 0)")


#com6
np.random.seed(1)

x0 = np.random.normal(2, 0.4, 400)
y0 = np.random.normal(2, 0.4, 400)
x1 = np.random.normal(3, 0.6, 600)
y1 = np.random.normal(6, 0.4, 400)
x2 = np.random.normal(4, 0.2, 200)
y2 = np.random.normal(4, 0.4, 200)

# Create figure
figg = go.Figure()

# Add traces
figg.add_trace(
    go.Scatter(
        x=x0,
        y=y0,
        mode="markers",
        marker=dict(color="DarkOrange")
    )
)

figg.add_trace(
    go.Scatter(
        x=x1,
        y=y1,
        mode="markers",
        marker=dict(color="Crimson")
    )
)

figg.add_trace(
    go.Scatter(
        x=x2,
        y=y2,
        mode="markers",
        marker=dict(color="RebeccaPurple")
    )
)

# Add buttons that add shapes
cluster0 = [dict(type="circle",
                            xref="x", yref="y",
                            x0=min(x0), y0=min(y0),
                            x1=max(x0), y1=max(y0),
                            line=dict(color="DarkOrange"))]
cluster1 = [dict(type="circle",
                            xref="x", yref="y",
                            x0=min(x1), y0=min(y1),
                            x1=max(x1), y1=max(y1),
                            line=dict(color="Crimson"))]
cluster2 = [dict(type="circle",
                            xref="x", yref="y",
                            x0=min(x2), y0=min(y2),
                            x1=max(x2), y1=max(y2),
                            line=dict(color="RebeccaPurple"))]

figg.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            buttons=[
                dict(label="None",
                     method="relayout",
                     args=["shapes", []]),
                dict(label="Cluster 0",
                     method="relayout",
                     args=["shapes", cluster0]),
                dict(label="Cluster 1",
                     method="relayout",
                     args=["shapes", cluster1]),
                dict(label="Cluster 2",
                     method="relayout",
                     args=["shapes", cluster2]),
                dict(label="All",
                     method="relayout",
                     args=["shapes", cluster0 + cluster1 + cluster2])
            ],
        )
    ],plot_bgcolor="rgba(0, 0, 0, 0)",
                    paper_bgcolor="rgba(0, 0, 0, 0)",
)

# Update remaining layout properties
figg.update_layout(
    title_text="Highlight Clusters",
    showlegend=False,
)



app.layout = html.Div(style={
    "background-image":"url('assets/background.jpg')",
},children =
    [
    dbc.Row([
        Header_component
    ]),
    dbc.Row(
        [dbc.Col(
            [dcc.Graph(figure = countfig)]
        ),dbc.Col(
            [dcc.Graph(figure = countfig_cum)]
        )]
    ),
    dbc.Row(
        [dbc.Col(
            [dcc.Graph(figure = fig)]
        ),dbc.Col(
            [dcc.Graph(figure = cus)]    
        ),dbc.Col(
            [dcc.Graph(figure = pirgif)]
     
    ),
    ]
),dbc.Row(
        [dbc.Col(
            [dcc.Graph(figure = figg)]
        )]
    ),
])

app.run_server(debug = True)


# # Load the CSV file


# @app.route('/')
# def index():
#     # Randomly select variables for plotting
#     x_variable = 'Time'
#     y_variable = 'concentration'
#     color_variable = 'type'

#     # Generate a scatter plot using Plotly
#     scatter_fig = px.scatter(data, x=x_variable, y=y_variable, color=color_variable, title='Scatter Plot')
#     scatter_div = scatter_fig.to_html(full_html=False)

#     # Randomly select variables for the table
#     table_data = data.sample(n=10)

#     return render_template('dash.html', scatter_div=scatter_div, table=table_data.to_html(index=False))

# if __name__ == '__main__':
#     app.run(debug=True)
