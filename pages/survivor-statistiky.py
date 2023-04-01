import dash
from dash import html, Output, Input, State, callback, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
import os
import plotly.express as px
import dash_ag_grid as dag

dash.register_page(__name__)

survivor_colors = {"Hrdinové": "#f70000", "Rebelové": "#0122dc"}

# basedir = os.path.abspath(os.path.dirname(__file__))
event_log_df = pd.read_excel(
    # os.path.join(basedir, "..", "data\survivor_2023_data.xlsx"),
    "survivor_2023_data.xlsx",
    sheet_name="event_log"
)
personal_stats_df = pd.read_excel(
    # os.path.join(basedir, "..", "data\survivor_2023_data.xlsx"),
    "survivor_2023_data.xlsx",
    sheet_name="personal_statistics",
)
personal_stats_df["DAY"] = personal_stats_df["DAY"].astype(str)
personal_stats_df_heat = personal_stats_df.copy()
personal_stats_df_heat = personal_stats_df_heat.set_index("DAY")
personal_stats_df_heat = personal_stats_df_heat.iloc[:, 2:]
personal_stats_df_heat = personal_stats_df_heat.T
personal_stats_df_heat["POWER_INDEX"] = (
    1 - (personal_stats_df_heat - 1).div(personal_stats_df_heat.count(axis=0) - 1)
).mean(axis=1)

players = {
    "Adam": {"profile_picture": "/assets/adam_profile_photo.jpg"},
    "Andrea": {"profile_picture": "/assets/andrea_profile_photo.jpg"},
    "Bára": {"profile_picture": "/assets/bara_profile_photo.jpg"},
    "Barbora": {"profile_picture": "/assets/barbora_profile_photo.jpg"},
    "Filip": {"profile_picture": "/assets/filip_profile_photo.jpg"},
    "Hanka": {"profile_picture": "/assets/hanka_profile_photo.jpg"},
    "Jiří": {"profile_picture": "/assets/jiri_profile_photo.jpg"},
    "Johanka": {"profile_picture": "/assets/johanka_profile_photo.jpg"},
    "Karolína": {"profile_picture": "/assets/karolina_profile_photo.jpg"},
    "Kateřina": {"profile_picture": "/assets/katka_profile_photo.jpg"},
    "Kristián": {"profile_picture": "/assets/kristian_profile_photo.jpg"},
    "Kulhy": {"profile_picture": "/assets/kulhy_profile_photo.jpg"},
    "Lída": {"profile_picture": "/assets/ludmila_profile_photo.jpg"},
    "Martin": {"profile_picture": "/assets/martin_profile_photo.jpg"},
    "Matěj": {"profile_picture": "/assets/matej_profile_photo.jpg"},
    "Pavlína": {"profile_picture": "/assets/pavlina_profile_photo.jpg"},
    "Pepa": {"profile_picture": "/assets/pepa_profile_photo.jpg"},
    "Pítr": {"profile_picture": "/assets/pitr_profile_photo.jpg"},
    "Soňa": {"profile_picture": "/assets/sona_profile_photo.jpg"},
    "Švanci": {"profile_picture": "/assets/svanci_profile_photo.jpg"},
    "Tereza": {"profile_picture": "/assets/tereza_profile_photo.jpg"},
    "Tomáš": {"profile_picture": "/assets/tomas_profile_photo.jpg"},
    "Vašek": {"profile_picture": "/assets/vasek_profile_photo.jpg"},
    "Žaneta": {"profile_picture": "/assets/zaneta_profile_photo.jpg"},
}


def eventlog_item(data_string):
    episode_timestamp = dmc.Tooltip(
        DashIconify(
            icon="mdi:television-classic",
            style={"padding-top": "4px"},
            width=20,
            height=20,
        ),
        label=dmc.Grid(
            [
                dmc.Col(
                    [
                        DashIconify(
                            icon="mdi:movie-open-outline",
                            width=20,
                            height=20,
                            style={
                                "padding": "0px",
                                "margin": "0px",
                            },
                        ),
                    ],
                    style={
                        "padding-left": "3px",
                        "padding-right": "4px",
                        "padding-top": "4px",
                        "padding-bottom": "0px",
                        "margin": "0px",
                    },
                    span="content",
                ),
                dmc.Col(
                    [
                        dmc.Text("Epizóda " + str(data_string["EPISODE"])),
                    ],
                    style={
                        "padding": "0px",
                        "margin": "0px",
                    },
                    span="content",
                ),
                dmc.Col(
                    [
                        DashIconify(
                            icon="ic:outline-access-time",
                            width=20,
                            height=20,
                            style={
                                "padding": "0px",
                                "margin": "0px",
                            },
                        ),
                    ],
                    style={
                        "padding-left": "5px",
                        "padding-right": "3px",
                        "padding-top": "4px",
                        "padding-bottom": "0px",
                        "margin": "0px",
                    },
                    span="content",
                ),
                dmc.Col(
                    [
                        dmc.Text(str(data_string["TIMESTAMP"])),
                    ],
                    style={
                        "padding-left": "0px",
                        "padding-right": "3px",
                        "padding-top": "0px",
                        "padding-bottom": "0px",
                        "margin": "0px",
                    },
                    span="content",
                ),
            ],
            style={
                "padding": "0px",
                "margin": "0px",
            },
            align="center",
        ),
        style={
            "padding": "3px",
            "margin": "0px",
        },
        position="top",
        transition="pop",
    )
    if data_string["EVENT_TYPE"] in ["Souboj o odměnu", "Souboj o imunitu"]:
        item = dmc.TimelineItem(
            children=[
                dmc.Card(
                    [
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        dmc.Grid(
                                            [
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            [
                                                                "Den "
                                                                + str(
                                                                    data_string["DAY"]
                                                                )
                                                                + " - "
                                                                + data_string[
                                                                    "EVENT_TYPE"
                                                                ]
                                                                + (
                                                                    " ("
                                                                    + str(
                                                                        data_string[
                                                                            "EVENT_DESC"
                                                                        ]
                                                                    )
                                                                    + ")"
                                                                    if data_string[
                                                                        "EVENT_TYPE"
                                                                    ]
                                                                    == "Souboj o odměnu"
                                                                    else ""
                                                                )
                                                            ],
                                                            weight=500,
                                                            size="lg",
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={"padding-right": "6px"},
                                                ),
                                                dmc.Col(
                                                    [episode_timestamp],
                                                    span="content",
                                                    style={"padding-left": "0px"},
                                                ),
                                            ],
                                            align="center",
                                        ),
                                        dmc.Grid(
                                            [
                                                dmc.Col(
                                                    [
                                                        DashIconify(
                                                            icon="mdi:crown",
                                                            width=25,
                                                            height=25,
                                                            style={
                                                                "color": survivor_colors[
                                                                    data_string[
                                                                        "WINNING_SIDE"
                                                                    ]
                                                                ],
                                                                "padding-top": "2px",
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={"padding-right": "3px"},
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            data_string["WINNING_SIDE"],
                                                            size="lg",
                                                            weight=700,
                                                            style={
                                                                "color": survivor_colors[
                                                                    data_string[
                                                                        "WINNING_SIDE"
                                                                    ]
                                                                ]
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={"padding-left": "0px"},
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            "("
                                                            + data_string["SCORE"]
                                                            + ")",
                                                            size="lg",
                                                            color="dimmed",
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-left": "0px",
                                                        "padding-right": "0px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.AvatarGroup(
                                                            children=[
                                                                dmc.Tooltip(
                                                                    dmc.Avatar(
                                                                        src=players[
                                                                            member
                                                                        ][
                                                                            "profile_picture"
                                                                        ],
                                                                        radius="lg",
                                                                    ),
                                                                    label=member,
                                                                    position="top",
                                                                    transition="pop",
                                                                )
                                                                for member in data_string[
                                                                    "WINNING_ROSTER"
                                                                ].split(
                                                                    ", "
                                                                )
                                                            ],
                                                        )
                                                    ],
                                                    span="content",
                                                ),
                                            ],
                                            align="center",
                                        ),
                                    ],
                                    span="content",
                                )
                            ]
                        )
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="lg",
                    style={
                        "width": "fit-content",
                        "border-color": survivor_colors[data_string["WINNING_SIDE"]],
                        "border-style": "solid",
                        "border-width": "2px",
                        "padding": "10px",
                        "margin-left": "10px",
                    },
                )
            ],
            bullet=DashIconify(icon="mdi:gift-outline", width=23, height=23)
            if data_string["EVENT_TYPE"] == "Souboj o odměnu"
            else DashIconify(
                icon="material-symbols:shield-outline", width=25, height=25
            ),
        )
    elif data_string["EVENT_TYPE"] == "Souboj o osobní imunitu":
        item = dmc.TimelineItem(
            children=[
                dmc.Card(
                    [
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        dmc.Grid(
                                            [
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            [
                                                                "Den "
                                                                + str(
                                                                    data_string["DAY"]
                                                                )
                                                                + " - "
                                                                + data_string[
                                                                    "EVENT_TYPE"
                                                                ]
                                                            ],
                                                            weight=500,
                                                            size="lg",
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={"padding-right": "6px"},
                                                ),
                                                dmc.Col(
                                                    [episode_timestamp],
                                                    span="content",
                                                    style={"padding-left": "0px"},
                                                ),
                                            ],
                                            align="center",
                                        ),
                                        dmc.Grid(
                                            [
                                                dmc.Col(
                                                    [
                                                        DashIconify(
                                                            icon="mdi:shield-sword-outline",
                                                            width=25,
                                                            height=25,
                                                            style={
                                                                "color": survivor_colors[
                                                                    data_string[
                                                                        "WINNING_SIDE"
                                                                    ]
                                                                ],
                                                                "padding-top": "2px",
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={"padding-right": "3px"},
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            data_string[
                                                                "WINNING_ROSTER"
                                                            ],
                                                            size="lg",
                                                            weight=700,
                                                            style={
                                                                "color": survivor_colors[
                                                                    data_string[
                                                                        "WINNING_SIDE"
                                                                    ]
                                                                ]
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-left": "0px",
                                                        "padding-right": "0px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Tooltip(
                                                            dmc.Avatar(
                                                                src=players[
                                                                    data_string[
                                                                        "WINNING_ROSTER"
                                                                    ]
                                                                ]["profile_picture"],
                                                                radius="lg",
                                                            ),
                                                            label=data_string[
                                                                "WINNING_ROSTER"
                                                            ],
                                                            position="top",
                                                            transition="pop",
                                                        )
                                                    ],
                                                    span="content",
                                                ),
                                            ],
                                            align="center",
                                        ),
                                    ],
                                    span="content",
                                )
                            ]
                        )
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="lg",
                    style={
                        "width": "fit-content",
                        "border-color": "black",
                        "border-style": "solid",
                        "border-width": "2px",
                        "padding": "10px",
                        "margin-left": "10px",
                    },
                )
            ],
            bullet=DashIconify(
                icon="icon-park-solid:diamond-necklace", width=23, height=23
            ),
        )
    elif data_string["EVENT_TYPE"] == "Kmenová rada":
        item = dmc.TimelineItem(
            children=[
                dmc.Card(
                    [
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        dmc.Grid(
                                            [
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            [
                                                                "Den "
                                                                + str(
                                                                    data_string["DAY"]
                                                                )
                                                                + " - "
                                                                + data_string[
                                                                    "EVENT_TYPE"
                                                                ]
                                                            ],
                                                            weight=500,
                                                            size="lg",
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={"padding-right": "6px"},
                                                ),
                                                dmc.Col(
                                                    [episode_timestamp],
                                                    span="content",
                                                    style={"padding-left": "0px"},
                                                ),
                                            ],
                                            align="center",
                                        ),
                                        dmc.Grid(
                                            [
                                                dmc.Col(
                                                    [
                                                        DashIconify(
                                                            icon="ic:baseline-how-to-vote",
                                                            width=25,
                                                            height=25,
                                                            style={
                                                                "color": survivor_colors[
                                                                    data_string[
                                                                        "WINNING_SIDE"
                                                                    ]
                                                                ],
                                                                "padding-top": "2px",
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={"padding-right": "3px"},
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            data_string[
                                                                "WINNING_ROSTER"
                                                            ],
                                                            size="lg",
                                                            weight=700,
                                                            style={
                                                                "color": survivor_colors[
                                                                    data_string[
                                                                        "WINNING_SIDE"
                                                                    ]
                                                                ]
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-left": "0px",
                                                        "padding-right": "0px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Tooltip(
                                                            dmc.Avatar(
                                                                src=players[
                                                                    data_string[
                                                                        "WINNING_ROSTER"
                                                                    ]
                                                                ]["profile_picture"],
                                                                radius="lg",
                                                            ),
                                                            label=data_string[
                                                                "WINNING_ROSTER"
                                                            ],
                                                            position="top",
                                                            transition="pop",
                                                        )
                                                    ],
                                                    span="content",
                                                ),
                                                dmc.Col(
                                                    [
                                                        DashIconify(
                                                            icon="material-symbols:swords-outline",
                                                            width=25,
                                                            height=25,
                                                            style={
                                                                "color": "black",
                                                                "padding-top": "2px",
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-right": "0px",
                                                        "padding-left": "0px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Tooltip(
                                                            dmc.Avatar(
                                                                src=players[
                                                                    data_string[
                                                                        "LOSING_ROSTER"
                                                                    ]
                                                                ]["profile_picture"],
                                                                radius="lg",
                                                            ),
                                                            label=data_string[
                                                                "LOSING_ROSTER"
                                                            ],
                                                            position="top",
                                                            transition="pop",
                                                        )
                                                    ],
                                                    span="content",
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            data_string[
                                                                "LOSING_ROSTER"
                                                            ],
                                                            size="lg",
                                                            weight=700,
                                                            style={
                                                                "color": survivor_colors[
                                                                    data_string[
                                                                        "WINNING_SIDE"
                                                                    ]
                                                                ]
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-left": "0px",
                                                        "padding-right": "0px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [
                                                        DashIconify(
                                                            icon="mingcute:hand-finger-2-line",
                                                            width=25,
                                                            height=25,
                                                            style={
                                                                "color": survivor_colors[
                                                                    data_string[
                                                                        "WINNING_SIDE"
                                                                    ]
                                                                ],
                                                                "padding-top": "2px",
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={"padding-left": "3px"},
                                                ),
                                            ],
                                            align="center",
                                        ),
                                    ],
                                    span="content",
                                )
                            ]
                        )
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="lg",
                    style={
                        "width": "fit-content",
                        "border-color": "black",
                        "border-style": "solid",
                        "border-width": "2px",
                        "padding": "10px",
                        "margin-left": "10px",
                    },
                )
            ],
            bullet=DashIconify(icon="mdi:campfire", width=23, height=23),
        )
    elif data_string["EVENT_TYPE"] == "Duel":
        item = dmc.TimelineItem(
            children=[
                dmc.Card(
                    [
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        dmc.Grid(
                                            [
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            [
                                                                "Den "
                                                                + str(
                                                                    data_string["DAY"]
                                                                )
                                                                + " - "
                                                                + data_string[
                                                                    "EVENT_TYPE"
                                                                ]
                                                            ],
                                                            weight=500,
                                                            size="lg",
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={"padding-right": "6px"},
                                                ),
                                                dmc.Col(
                                                    [episode_timestamp],
                                                    span="content",
                                                    style={"padding-left": "0px"},
                                                ),
                                            ],
                                            align="center",
                                        ),
                                        dmc.Grid(
                                            [
                                                dmc.Col(
                                                    [
                                                        DashIconify(
                                                            icon="mdi:crown",
                                                            width=25,
                                                            height=25,
                                                            style={
                                                                "color": survivor_colors[
                                                                    data_string[
                                                                        "WINNING_SIDE"
                                                                    ]
                                                                ],
                                                                "padding-top": "2px",
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={"padding-right": "3px"},
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            data_string[
                                                                "WINNING_ROSTER"
                                                            ],
                                                            size="lg",
                                                            weight=700,
                                                            style={
                                                                "color": survivor_colors[
                                                                    data_string[
                                                                        "WINNING_SIDE"
                                                                    ]
                                                                ]
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-left": "0px",
                                                        "padding-right": "0px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Tooltip(
                                                            dmc.Avatar(
                                                                src=players[
                                                                    data_string[
                                                                        "WINNING_ROSTER"
                                                                    ]
                                                                ]["profile_picture"],
                                                                radius="lg",
                                                            ),
                                                            label=data_string[
                                                                "WINNING_ROSTER"
                                                            ],
                                                            position="top",
                                                            transition="pop",
                                                        )
                                                    ],
                                                    span="content",
                                                ),
                                                dmc.Col(
                                                    [
                                                        DashIconify(
                                                            icon="material-symbols:swords-outline",
                                                            width=25,
                                                            height=25,
                                                            style={
                                                                "color": "black",
                                                                "padding-top": "2px",
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-right": "0px",
                                                        "padding-left": "0px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Tooltip(
                                                            dmc.Avatar(
                                                                src=players[
                                                                    data_string[
                                                                        "LOSING_ROSTER"
                                                                    ]
                                                                ]["profile_picture"],
                                                                radius="lg",
                                                                style={
                                                                    "opacity": "0.5",
                                                                    "background-color": "grey",
                                                                },
                                                            ),
                                                            label=data_string[
                                                                "LOSING_ROSTER"
                                                            ],
                                                            position="top",
                                                            transition="pop",
                                                        )
                                                    ],
                                                    span="content",
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            data_string[
                                                                "LOSING_ROSTER"
                                                            ],
                                                            size="lg",
                                                            weight=700,
                                                            color="dimmed",
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-left": "0px",
                                                        "padding-right": "0px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [
                                                        DashIconify(
                                                            icon="material-symbols:person-remove-outline",
                                                            width=25,
                                                            height=25,
                                                            style={
                                                                "color": "#868e96",
                                                                "padding-top": "3px",
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={"padding-left": "3px"},
                                                ),
                                            ],
                                            align="center",
                                        ),
                                    ],
                                    span="content",
                                )
                            ]
                        )
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="lg",
                    style={
                        "width": "fit-content",
                        "border-color": "black",
                        "border-style": "solid",
                        "border-width": "2px",
                        "padding": "10px",
                        "margin-left": "10px",
                    },
                )
            ],
            bullet=DashIconify(
                icon="material-symbols:swords-outline", width=23, height=23
            ),
        )
    elif data_string["EVENT_TYPE"] == "Noví hráči":
        item = dmc.TimelineItem(
            children=[
                dmc.Card(
                    [
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        dmc.Grid(
                                            [
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            [
                                                                "Den "
                                                                + str(
                                                                    data_string["DAY"]
                                                                )
                                                                + " - "
                                                                + data_string[
                                                                    "EVENT_TYPE"
                                                                ]
                                                            ],
                                                            weight=500,
                                                            size="lg",
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={"padding-right": "6px"},
                                                ),
                                                dmc.Col(
                                                    [episode_timestamp],
                                                    span="content",
                                                    style={"padding-left": "0px"},
                                                ),
                                            ],
                                            align="center",
                                        ),
                                        dmc.Grid(
                                            [
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            data_string[
                                                                "WINNING_ROSTER"
                                                            ],
                                                            size="lg",
                                                            weight=700,
                                                            style={
                                                                "color": survivor_colors[
                                                                    data_string[
                                                                        "WINNING_SIDE"
                                                                    ]
                                                                ]
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={"padding-right": "0px"},
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.AvatarGroup(
                                                            children=[
                                                                dmc.Tooltip(
                                                                    dmc.Avatar(
                                                                        src=players[
                                                                            member
                                                                        ][
                                                                            "profile_picture"
                                                                        ],
                                                                        radius="lg",
                                                                    ),
                                                                    label=member,
                                                                    position="top",
                                                                    transition="pop",
                                                                )
                                                                for member in data_string[
                                                                    "WINNING_ROSTER"
                                                                ].split(
                                                                    ", "
                                                                )
                                                            ],
                                                        )
                                                    ],
                                                    span="content",
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            data_string[
                                                                "LOSING_ROSTER"
                                                            ],
                                                            size="lg",
                                                            weight=700,
                                                            style={
                                                                "color": survivor_colors[
                                                                    "Rebelové"
                                                                ]
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-left": "0px",
                                                        "padding-right": "0px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.AvatarGroup(
                                                            children=[
                                                                dmc.Tooltip(
                                                                    dmc.Avatar(
                                                                        src=players[
                                                                            member
                                                                        ][
                                                                            "profile_picture"
                                                                        ],
                                                                        radius="lg",
                                                                    ),
                                                                    label=member,
                                                                    position="top",
                                                                    transition="pop",
                                                                )
                                                                for member in data_string[
                                                                    "LOSING_ROSTER"
                                                                ].split(
                                                                    ", "
                                                                )
                                                            ],
                                                        )
                                                    ],
                                                    span="content",
                                                ),
                                            ],
                                            align="center",
                                        ),
                                    ],
                                    span="content",
                                )
                            ]
                        )
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="lg",
                    style={
                        "width": "fit-content",
                        "border-color": "black",
                        "border-style": "solid",
                        "border-width": "2px",
                        "padding": "10px",
                        "margin-left": "10px",
                    },
                )
            ],
            bullet=DashIconify(
                icon="material-symbols:person-add-outline", width=23, height=23
            ),
        )
    elif data_string["EVENT_TYPE"] == "Odstoupení":
        item = dmc.TimelineItem(
            children=[
                dmc.Card(
                    [
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        dmc.Grid(
                                            [
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            [
                                                                "Den "
                                                                + str(
                                                                    data_string["DAY"]
                                                                )
                                                                + " - "
                                                                + data_string[
                                                                    "EVENT_TYPE"
                                                                ]
                                                            ],
                                                            weight=500,
                                                            size="lg",
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={"padding-right": "6px"},
                                                ),
                                                dmc.Col(
                                                    [episode_timestamp],
                                                    span="content",
                                                    style={"padding-left": "0px"},
                                                ),
                                            ],
                                            align="center",
                                        ),
                                        dmc.Grid(
                                            [
                                                dmc.Col(
                                                    [
                                                        DashIconify(
                                                            icon="material-symbols:person-remove-outline",
                                                            width=25,
                                                            height=25,
                                                            style={
                                                                "color": "#868e96",
                                                                "padding-top": "3px",
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={"padding-right": "3px"},
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            data_string[
                                                                "LOSING_ROSTER"
                                                            ],
                                                            size="lg",
                                                            weight=700,
                                                            color="dimmed",
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-left": "0px",
                                                        "padding-right": "0px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Tooltip(
                                                            dmc.Avatar(
                                                                src=players[
                                                                    data_string[
                                                                        "LOSING_ROSTER"
                                                                    ]
                                                                ]["profile_picture"],
                                                                radius="lg",
                                                                style={
                                                                    "opacity": "0.5",
                                                                    "background-color": "grey",
                                                                },
                                                            ),
                                                            label=data_string[
                                                                "LOSING_ROSTER"
                                                            ],
                                                            position="top",
                                                            transition="pop",
                                                        )
                                                    ],
                                                    span="content",
                                                ),
                                            ],
                                            align="center",
                                        ),
                                    ],
                                    span="content",
                                )
                            ]
                        )
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="lg",
                    style={
                        "width": "fit-content",
                        "border-color": "black",
                        "border-style": "solid",
                        "border-width": "2px",
                        "padding": "10px",
                        "margin-left": "10px",
                    },
                )
            ],
            bullet=DashIconify(
                icon="mdi:flag-variant-outline", width=27, height=27
            ),
        )
    else:
        item = dmc.TimelineItem(
            children=[
                dmc.Card(
                    [
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        dmc.Grid(
                                            [
                                                dmc.Col(
                                                    [episode_timestamp],
                                                    span="content",
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            [
                                                                "Den "
                                                                + str(
                                                                    data_string["DAY"]
                                                                )
                                                                + ", "
                                                                + data_string[
                                                                    "EVENT_TYPE"
                                                                ]
                                                            ]
                                                        ),
                                                    ],
                                                    span="content",
                                                ),
                                            ]
                                        ),
                                        dmc.Text(
                                            data_string["WINNING_SIDE"],
                                            color="dimmed",
                                            size="sm",
                                        ),
                                    ],
                                    span="content",
                                )
                            ]
                        )
                    ],
                    withBorder=True,
                    shadow="sm",
                    radius="lg",
                    style={"width": "fit-content"},
                )
            ],
        )
    return item


def create_eventlog(data):
    items = []
    for i in range(len(data.index)):
        items.append(eventlog_item(data.loc[i]))
    eventlog = dmc.Timeline(
        active=len(data.index),
        bulletSize=40,
        lineWidth=2,
        children=items,
        color="gray",
    )
    return eventlog


layout = dmc.Grid(
    [
        dmc.Col(
            [
                dmc.Grid([dmc.Col([create_eventlog(event_log_df)])]),
                dmc.Grid(
                    [
                        dmc.Col(
                            [
                                dcc.Graph(
                                    id="survivor-personal-stats-heatmap",
                                    figure=px.imshow(
                                        personal_stats_df_heat,
                                        text_auto=True,
                                        color_continuous_scale="RdYlGn_r",
                                    ),
                                    style={"height": "90vh"},
                                ),
                            ]
                        )
                    ]
                ),
                dmc.Grid(
                    [
                        dmc.Col(
                            [
                                dag.AgGrid(
                                    id="survivor-personal-stats-grid",
                                    rowData=personal_stats_df_heat.reset_index().to_dict(
                                        "records"
                                    ),
                                    columnDefs=[
                                        {"field": i, "id": i, "type": "numericColumn"}
                                        for i in personal_stats_df_heat.reset_index().columns
                                    ],
                                    defaultColDef={
                                        "resizable": True,
                                        "sortable": True,
                                        "filter": True,
                                        "minWidth": 50,
                                    },
                                    columnSize="autoSizeAll",
                                    # getRowId="params.data.State",
                                )
                            ]
                        )
                    ]
                ),
            ],
            span=10,
            offset=1,
        )
    ]
)
