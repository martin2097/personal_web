from dash import Dash, html, dcc, page_container
import dash_mantine_components as dmc

app = Dash(__name__, use_pages=True)
server = app.server

app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-P1X46SBN10"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
        
          gtag('config', 'G-P1X46SBN10');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <meta name="seznam-wmt" content="XHyoishcgDiRoWjHaGC2Myu4JV2rYxQ8" />
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
