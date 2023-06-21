import pandas as pd
import plotly.express as px
from flask import Flask, render_template

app = Flask(__name__)

# Load the CSV file
data = pd.read_csv('dataset.csv')

@app.route('/')
def index():
    # Randomly select variables for plotting
    x_variable = 'Time'
    y_variable = 'concentration'
    color_variable = 'type'

    # Generate a scatter plot using Plotly
    scatter_fig = px.scatter(data, x=x_variable, y=y_variable, color=color_variable, title='Scatter Plot')
    scatter_div = scatter_fig.to_html(full_html=False)

    # Randomly select variables for the table
    table_data = data.sample(n=10)

    return render_template('dash.html', scatter_div=scatter_div, table=table_data.to_html(index=False))

if __name__ == '__main__':
    app.run(debug=True)
