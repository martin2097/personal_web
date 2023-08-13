from dash import (
    Dash,
    html,
    Output,
    Input,
    State,
    clientside_callback,
    callback,
    dcc,
    page_container,
    ALL,
)
import dash_mantine_components as dmc
from lib.utils import visit_link_icon
from lib.navbar import navbar

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

links = {
    "about": {"label": "About Me"},
    "experience": {"label": "Experience"},
    "contact": {"label": "Contact Me"},
}


app.layout = html.Div(
    [
        dcc.Store(id="theme-store", storage_type="local"),
        dmc.MantineProvider(
            [
                navbar(links, "tabler:square-rounded-letter-m", ""),
                dmc.Grid(
                    [
                        dmc.MediaQuery(
                            dmc.Col(
                                dmc.Stack(
                                    [
                                        visit_link_icon(
                                            "https://github.com/martin2097/",
                                            "mdi:github",
                                        ),
                                        visit_link_icon(
                                            "https://linkedin.com/in/martin-rapavy",
                                            "mdi:linkedin",
                                        ),
                                        dmc.Center(
                                            dmc.Divider(
                                                orientation="vertical",
                                                style={"height": "25vh"},
                                                size="sm",
                                            ),
                                        ),
                                    ],
                                    spacing=0,
                                    justify="flex-end",
                                    align="center",
                                    style={"height": "100%"},
                                ),
                                p=0,
                                m=0,
                                style={"height": "100%", "width": "60px"},
                            ),
                            smallerThan="sm",
                            styles={"display": "none"},
                            # innerBoxStyle={"height": "calc(100vh - 43px)"},
                        ),
                        dmc.Col(
                            [
                                dmc.ScrollArea(
                                    page_container,
                                    style={"width": "100%", "height": "100vh"},
                                    type="scroll",
                                )
                            ],
                            span="auto",
                            style={"overflow": "hidden"},
                            p=0,
                        ),
                    ],
                    m=0,
                    style={"height": "100vh", "width": "100vw"},
                ),
            ],
            theme={"colorScheme": "dark"},
            withGlobalStyles=True,
            id="theme-provider",
        ),
    ],
)


clientside_callback(
    """ function(data) { return data } """,
    Output("theme-provider", "theme"),
    Input("theme-store", "data"),
)


clientside_callback(
    """function(n_clicks, data) {
        if (data) {
            if (n_clicks) {
                const scheme = data["colorScheme"] == "dark" ? "light" : "dark"
                return { colorScheme: scheme } 
            }
            return dash_clientside.no_update
        } else {
            return { colorScheme: "dark" }
        }
    }""",
    Output("theme-store", "data"),
    Input("color-scheme-toggle", "n_clicks"),
    State("theme-store", "data"),
)


clientside_callback(
    """function(n_clicks, opened) { return !opened }""",
    Output("navbar-drawer", "opened"),
    Input("burger-button", "n_clicks"),
    State("navbar-drawer", "opened"),
    prevent_initial_call=True,
)


clientside_callback(
    """
        function (i) {
            console.log(i);
            return false
        }
    """,
    Output("navbar-drawer", "opened", allow_duplicate=True),
    Input({"index": ALL, "type": "navlink"}, "n_clicks"),
    prevent_initial_call=True,
)


if __name__ == "__main__":
    app.run(debug=False)
