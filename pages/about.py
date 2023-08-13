import dash
import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify
from lib.utils import visit_link_icon, mid_col_responsive

dash.register_page(__name__, title="Martin Rapavý - About Me")

about_me_p1 = (
    "My name is Martin, and I enjoy making other people's lives easier. It may be data insight presented in a "
    "user-friendly way, or it could be teaching them how to do it themselves. "
)

about_me_p2 = (
    "Python has been my primary tool for this for the last few years. It all started with Dash, and it's still my "
    "favorite to this day. It allows me to deliver the most insight from data in a way that is accessible even to "
    "non-technical users."
)

about_me_p3 = (
    "I also want to give something back because I have learnt so much from others. I am involved in the "
    "Dash community and also organize educational events for my coworkers."
)

layout = mid_col_responsive(
    dmc.Stack(
        [
            # dmc.Text("About Me", weight=600, size=25, p=8),
            dmc.Divider(
                label="Who am I?",
                size="sm",
                styles={"label": {"font-size": "25px", "font-weight": 600}},
                mt=20,
            ),
            dmc.Grid(
                [
                    dmc.MediaQuery(
                        dmc.Col(
                            [
                                dmc.Grid(
                                    [
                                        dmc.Col(
                                            [
                                                dmc.Avatar(
                                                    src="assets/profile_pic.jpg",
                                                    style={
                                                        "background": "linear-gradient(45deg, rgb(25, 113, 194) 0%, rgb(9, 146, 104) 100%)"
                                                    },
                                                    styles={"image": {"opacity": 0.5}},
                                                    size=250,
                                                    radius="xl",
                                                )
                                            ],
                                            span="content",
                                        )
                                    ],
                                    justify="center",
                                )
                            ],
                        ),
                        largerThan="md",
                        styles={"display": "none"},
                        innerBoxStyle={"width": "100%"},
                    ),
                    dmc.Col(
                        [
                            dmc.Text(about_me_p1, align="justify"),
                            dmc.Space(h=25),
                            dmc.Text(about_me_p2, align="justify"),
                            dmc.Space(h=25),
                            dmc.Text(about_me_p3, align="justify"),
                        ],
                        sm="auto",
                    ),
                    dmc.MediaQuery(
                        dmc.Col(
                            [
                                dmc.Grid(
                                    [
                                        dmc.Col(
                                            [
                                                dmc.Avatar(
                                                    src="assets/profile_pic.jpg",
                                                    style={
                                                        "background": "linear-gradient(45deg, rgb(25, 113, 194) 0%, rgb(9, 146, 104) 100%)"
                                                    },
                                                    styles={"image": {"opacity": 0.5}},
                                                    size=250,
                                                    radius="xl",
                                                )
                                            ],
                                            span="content",
                                        )
                                    ],
                                    justify="flex-end",
                                )
                            ],
                        ),
                        smallerThan="md",
                        styles={"display": "none"},
                        innerBoxStyle={"width": "275px"},
                    ),
                ],
                m=0,
            ),
            dmc.Divider(
                label="My Talents",
                size="sm",
                styles={"label": {"font-size": "25px", "font-weight": 600}},
                my=10,
            ),
            dmc.Grid(
                [
                    dmc.Col(
                        [
                            dmc.Text("Technical Skills:", mb=5),
                            dmc.List(
                                [
                                    dmc.ListItem(
                                        dmc.Text(
                                            [
                                                dmc.Anchor(
                                                    "Dash",
                                                    href="https://dash.plotly.com/",
                                                    underline=False,
                                                    target="_blank",
                                                ),
                                                ", ",
                                                dmc.Anchor(
                                                    "Plotly",
                                                    href="https://plotly.com/python/",
                                                    underline=False,
                                                    target="_blank",
                                                ),
                                                ", ",
                                                dmc.Anchor(
                                                    "DMC",
                                                    href="https://www.dash-mantine-components.com/",
                                                    underline=False,
                                                    target="_blank",
                                                ),
                                                ", ",
                                                dmc.Anchor(
                                                    "DAG",
                                                    href="https://dash.plotly.com/dash-ag-grid",
                                                    underline=False,
                                                    target="_blank",
                                                ),
                                            ]
                                        ),
                                        icon=DashIconify(
                                            icon="akar-icons:python-fill", width=24
                                        ),
                                    ),
                                    dmc.ListItem(
                                        dmc.Text(
                                            [
                                                dmc.Anchor(
                                                    "Pandas",
                                                    href="https://pandas.pydata.org/docs/index.html",
                                                    underline=False,
                                                    target="_blank",
                                                )
                                            ]
                                        ),
                                        icon=DashIconify(
                                            icon="akar-icons:python-fill", width=24
                                        ),
                                    ),
                                    dmc.ListItem(
                                        "SQL",
                                        icon=DashIconify(
                                            icon="material-symbols:database", width=24
                                        ),
                                    ),
                                    dmc.ListItem(
                                        "Git, Jira, Confluence",
                                        icon=DashIconify(
                                            icon="mdi:atlassian", width=24
                                        ),
                                    ),
                                ]
                            ),
                        ],
                        sm=6,
                    ),
                    dmc.Col(
                        [
                            dmc.Text("Soft Skills:", mb=5),
                            dmc.List(
                                [
                                    dmc.ListItem("Strong Problem Solving"),
                                    dmc.ListItem("Managing Changes"),
                                    dmc.ListItem("Influencing Others"),
                                    dmc.ListItem("Empathetic"),
                                    dmc.ListItem("Eager Learner"),
                                ]
                            ),
                        ],
                        sm=6,
                    ),
                ],
                m=0,
            ),
        ],
        spacing=0,
        # align="center",
        className="animate__animated animate__fadeInUp animate__faster",
        id="about-stack",
    )
)
