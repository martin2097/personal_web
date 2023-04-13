from dash import Dash, html, dcc, page_container
import dash_mantine_components as dmc

app = Dash(__name__, use_pages=True)
server = app.server

app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-3W95YB8LX7"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
        
          gtag('config', 'G-3W95YB8LX7');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <meta property="og:type" content="article">
        <meta property="og:title" content="Cryptocurrency Indicators Dashboard"">
        <meta property="og:site_name" content="https://crypto-indicators-dashboard.herokuapp.com">
        <meta property="og:url" content="https://crypto-indicators-dashboard.herokuapp.com">
        <meta property="og:image" content="https://raw.githubusercontent.com/dc-aichara/DS-ML-Public/master/Medium_Files/dashboard_demo/assets/favicon.ico">
        <meta property="article:published_time" content="2020-11-01">
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

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
