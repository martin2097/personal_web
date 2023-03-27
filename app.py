from dash import Dash, html, dcc, page_container
import plotly.express as px
import pandas as pd

app = Dash(__name__, use_pages=True)
server = app.server

app.layout = page_container

if __name__ == '__main__':
    app.run_server(debug=False)
