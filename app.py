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
import dash
from lib.utils import visit_link_icon
from lib.navbar import navbar
from flask import redirect, Flask

server = Flask(__name__)


@server.route("/")
def index_redirect():
    return redirect("/en/")


app = Dash(__name__, server=server, use_pages=True)

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
        dcc.Location(id="url", refresh="callback-nav"),
        dmc.MantineProvider(
            page_container,
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


@callback(
    Output("url", "pathname"),
    Input("language-switch", "value"),
    State("url", "pathname"),
)
def switch_language(language, pathname):
    try:
        split_path = pathname.split("/", 2)
        return "/" + language + "/" + split_path[2]
    except:
        return dash.no_update


if __name__ == "__main__":
    app.run(debug=False)
