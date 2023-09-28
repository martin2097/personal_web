from dash import html
import dash_mantine_components as dmc
from lib.navbar import navbar
from lib.utils import visit_link_icon


links = {
    "/about": {"en": "About Me", "sk": "O mne"},
    "/projects": {"en": "Projects", "sk": "Projekty"},
    "/experience": {"en": "Experience", "sk": "Skúsenosti"},
    "/contact": {"en": "Contact Me", "sk": "Kontaktujte ma"},
}


def page_template(page, language):
    return html.Div(
        [
            navbar(links, language, "tabler:square-rounded-letter-m", ""),
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
                                dmc.MediaQuery(
                                    html.Div(
                                        dmc.MediaQuery(
                                            html.Div(
                                                page,
                                                style={"padding-top": "40px"},
                                            ),
                                            largerThan="sm",
                                            styles={"max-width": "calc(100vw - 60px)"},
                                            boxWrapperProps={
                                                "style": {"width": "100%"}
                                            },
                                        ),
                                    ),
                                    smallerThan="sm",
                                    styles={"max-width": "100vw"},
                                    boxWrapperProps={"style": {"width": "100%"}},
                                ),
                                style={"width": "100%", "height": "100vh"},
                                type="scroll",
                                # offsetScrollbars=True,
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
        ]
    )
