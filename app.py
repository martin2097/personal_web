from dash import Dash, html, dcc, page_container
import dash_mantine_components as dmc

app = Dash(__name__, use_pages=True)
server = app.server

app.layout = html.Div(
    [
        dcc.Store(id="theme-store", storage_type="local"),
        dmc.MantineProvider(
            page_container,
            theme={"colorScheme": "light"},
            withGlobalStyles=True,
            id="mantine-docs-theme-provider",
        ),
    ]
)

if __name__ == '__main__':
    app.run_server(debug=False)
