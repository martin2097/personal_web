import dash_mantine_components as dmc
from dash import dcc, html
from dash_iconify import DashIconify
from lib.utils import visit_link_icon


def navbar(links, brand_icon, brand_name):
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
                                                icon=brand_icon, height=35, width=35
                                            ),
                                            variant="transparent",
                                            id={"type": "navlink", "index": "logo"},
                                        ),
                                        href="/",
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
                                ],
                                spacing=5,
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
                                                    dmc.MediaQuery(
                                                        dmc.NavLink(
                                                            label=links[link]["label"],
                                                            href=link,
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
                                                    dmc.ActionIcon(
                                                        DashIconify(
                                                            icon="radix-icons:blending-mode",
                                                            width=25,
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
                overlayOpacity=0.55,
                overlayBlur=3,
                zIndex=9,
                size=300,
                children=[
                    dmc.ScrollArea(
                        offsetScrollbars=True,
                        type="scroll",
                        style={"height": "100vh"},
                        pt=20,
                        children=dmc.Stack(
                            [
                                html.A(
                                    dmc.NavLink(
                                        label=links[link]["label"],
                                        href=link,
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
                    )
                ],
            ),
        ],
        style={"margin-bottom": "3px"},
        withBorder=False,
    )
