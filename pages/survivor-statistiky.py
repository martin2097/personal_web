import dash
from dash import html, Output, Input, State, callback, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
import os
import plotly.express as px
import dash_ag_grid as dag

dash.register_page(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
event_log_df = pd.read_excel(
    os.path.join(basedir, "..", "data\survivor_2023_data.xlsx"), sheet_name="event_log"
)
personal_stats_df = pd.read_excel(
    os.path.join(basedir, "..", "data\survivor_2023_data.xlsx"),
    sheet_name="personal_statistics",
)
personal_stats_df["DAY"] = personal_stats_df["DAY"].astype(str)
print(personal_stats_df)
personal_stats_df_heat = personal_stats_df.copy()
personal_stats_df_heat = personal_stats_df_heat.set_index("DAY")
personal_stats_df_heat = personal_stats_df_heat.iloc[:, 2:]
personal_stats_df_heat = personal_stats_df_heat.T
personal_stats_df_heat["POWER_INDEX"] = (
    1 - (personal_stats_df_heat - 1).div(personal_stats_df_heat.count(axis=0) - 1)
).mean(axis=1)
print(personal_stats_df_heat)
print(personal_stats_df_heat.reset_index())

players = {
    "Adam": {"profile_picture": "/assets/adam_profile_photo.jpg"}
}

def eventlog_item(data_string):
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
                                                    dmc.Tooltip(
                                                        DashIconify(
                                                            icon="mdi:television-classic"
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
                                                                        dmc.Text(
                                                                            "Epizóda "
                                                                            + str(
                                                                                data_string[
                                                                                    "EPISODE"
                                                                                ]
                                                                            )
                                                                        ),
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
                                                                        dmc.Text(
                                                                            str(
                                                                                data_string[
                                                                                    "TIMESTAMP"
                                                                                ]
                                                                            )
                                                                        ),
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
                                                    ),
                                                ],
                                                span="content",
                                            ),
                                            dmc.Col(
                                                [
                                                    dmc.Text(
                                                        [
                                                            "Den "
                                                            + str(data_string["DAY"])
                                                            + ", "
                                                            + data_string["EVENT_TYPE"]
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
                radius="md",
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
        bulletSize=30,
        lineWidth=2,
        children=items,
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
                                dmc.Avatar(src=players["Adam"]["profile_picture"]),
                                dcc.Graph(
                                    id="survivor-personal-stats-heatmap",
                                    figure=px.imshow(
                                        personal_stats_df_heat,
                                        text_auto=True,
                                        color_continuous_scale="RdYlGn_r",
                                    ),
                                    style={"height": "90vh"},
                                )
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
                                        {"field": i, "id": i, 'type': 'numericColumn'}
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
