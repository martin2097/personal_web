import dash_mantine_components as dmc
from dash import dcc, html
from dash_iconify import DashIconify
from lib.utils import visit_link_icon


def navbar(links, language, brand_icon, brand_name):
    if language not in ["en", "sk"]:
        language = "en"
    return dmc.Header(
        height=40,
        fixed=True,
        children=[
            dmc.Grid(
                [
                    dmc.Col(
                        [
                            dmc.Group(
                                [
                                    dcc.Link(
                                        dmc.ActionIcon(
                                            DashIconify(
                                                icon=brand_icon,
                                                height=35,
                                                width=35,
                                                color="rgb(134, 142, 150)",
                                            ),
                                            variant="transparent",
                                            id={"type": "navlink", "index": "logo"},
                                        ),
                                        href="/" + language + "/",
                                    ),
                                    dmc.Anchor(
                                        brand_name,
                                        size=24,
                                        style={
                                            "margin": "0px",
                                            "padding": "0px",
                                            "font-weight": "500",
                                            "color": "#868E96",
                                        },
                                        href="/",
                                        underline=False,
                                    ),
                                ]
                                + [
                                    dmc.MediaQuery(
                                        dmc.NavLink(
                                            label=links[link][language],
                                            href="/" + language + link,
                                            style={
                                                "padding": "7px",
                                                "width": "auto",
                                            },
                                            styles={
                                                "label": {
                                                    "color": "#868E96",
                                                    "font-weight": "500",
                                                    "font-size": "16px",
                                                },
                                            },
                                        ),
                                        smallerThan="sm",
                                        styles={"display": "none"},
                                    )
                                    for link in links
                                ]
                                + [
                                    dmc.MediaQuery(
                                        dcc.Link(
                                            dmc.Button(
                                                "Blog",
                                                leftIcon=DashIconify(
                                                    icon="jam:write",
                                                    width=16,
                                                    height=16,
                                                ),
                                                variant="gradient",
                                                radius="xl",
                                                size="xs",
                                                gradient={
                                                    "from": "blue",
                                                    "to": "teal",
                                                    "deg": 45,
                                                },
                                                styles={
                                                    "label": {"font-size": "16px"},
                                                    "leftIcon": {"margin-right": "5px"},
                                                },
                                                px=20,
                                            ),
                                            # href="/" + language + "/blog",
                                            href="https://blog.rapavy.cz/" + language + "/home",
                                            target="_blank",
                                        ),
                                        smallerThan="sm",
                                        styles={"display": "none"},
                                    )
                                ],
                                spacing=20,
                                style={"margin-left": "2vh"},
                            )
                        ],
                        style={"margin": "0px", "padding": "0px"},
                        span="content",
                    ),
                    dmc.Col(
                        [
                            dmc.Grid(
                                [
                                    dmc.Col(
                                        [
                                            dmc.Group(
                                                [
                                                    dmc.SegmentedControl(
                                                        id="language-switch",
                                                        value=language,
                                                        size="sm",
                                                        data=[
                                                            {
                                                                "value": "en",
                                                                "label": "EN",
                                                            },
                                                            {
                                                                "value": "sk",
                                                                "label": "SK",
                                                            },
                                                        ],
                                                        style={
                                                            "background-color": "rgba(0,0,0,0)"
                                                        },
                                                        styles={
                                                            "indicator": {
                                                                "background-color": "rgba(0,0,0,0)",
                                                                "box-shadow": "none",
                                                            },
                                                            "label": {
                                                                "color": "rgb(134, 142, 150)",
                                                                "font-size": "16px",
                                                                "padding-left": "10px",
                                                                "padding-right": "0px",
                                                                "padding-top": "0px",
                                                                "padding-bottom": "0px",
                                                            },
                                                            "controlActive": {
                                                                "color": "rgb(34, 139, 230)"
                                                            },
                                                        },
                                                    )
                                                ]
                                                + [
                                                    dmc.ActionIcon(
                                                        DashIconify(
                                                            icon="radix-icons:blending-mode",
                                                            width=25,
                                                            color="rgb(134, 142, 150)",
                                                        ),
                                                        variant="transparent",
                                                        id="color-scheme-toggle",
                                                    ),
                                                ]
                                                + [
                                                    dmc.MediaQuery(
                                                        dmc.ActionIcon(
                                                            DashIconify(
                                                                icon="radix-icons:hamburger-menu",
                                                                width=25,
                                                                color="rgb(134, 142, 150)",
                                                            ),
                                                            variant="transparent",
                                                            id="burger-button",
                                                        ),
                                                        largerThan="sm",
                                                        styles={"display": "none"},
                                                    ),
                                                ]
                                            )
                                        ],
                                        span="content",
                                        style={
                                            "padding": "0px",
                                            "margin-right": "2vh",
                                        },
                                    )
                                ],
                                justify="flex-end",
                            )
                        ],
                        span="auto",
                    ),
                ],
                align="center",
                style={"margin": "0px", "padding": "0px", "height": "100%"},
                columns=24,
            ),
            dmc.Drawer(
                id="navbar-drawer",
                overlayProps={"opacity": 0.55, "blur": 3},
                zIndex=9,
                size=300,
                children=[
                    dmc.Stack(
                        [
                            html.A(
                                dmc.NavLink(
                                    label=links[link][language],
                                    href="/" + language + link,
                                    n_clicks=0,
                                    style={
                                        "padding": "7px",
                                        "width": "auto",
                                    },
                                    styles={
                                        "label": {
                                            "color": "#868E96",
                                            "font-weight": "500",
                                            "font-size": "24px",
                                        },
                                    },
                                ),
                                id={
                                    "type": "navlink",
                                    "index": link,
                                },
                            )
                            for link in links
                        ]
                        + [
                            dcc.Link(
                                dmc.Button(
                                    "Blog",
                                    leftIcon=DashIconify(
                                        icon="jam:write",
                                        width=24,
                                        height=24,
                                    ),
                                    fullWidth=True,
                                    size="lg",
                                    variant="gradient",
                                    radius="xl",
                                    gradient={
                                        "from": "blue",
                                        "to": "teal",
                                        "deg": 45,
                                    },
                                    styles={
                                        "label": {
                                            "font-weight": "500",
                                            "font-size": "24px",
                                        }
                                    },
                                ),
                                # href="/" + language + "/blog",
                                href="https://blog.rapavy.cz/" + language + "/home",
                                target="_blank",
                                style={"width": "80%", "text-decoration": "none"},
                            )
                        ]
                        + [
                            dmc.Group(
                                [
                                    visit_link_icon(
                                        "https://github.com/martin2097/",
                                        "mdi:github",
                                    ),
                                    visit_link_icon(
                                        "https://linkedin.com/in/martin-rapavy",
                                        "mdi:linkedin",
                                    ),
                                ],
                                pt=20,
                            ),
                        ],
                        align="center",
                        spacing=5,
                    ),
                ],
            ),
        ],
        style={"margin-bottom": "3px"},
        withBorder=False,
    )
