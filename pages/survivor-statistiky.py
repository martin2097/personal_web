import dash
from dash import  dcc
from dash.dash_table import DataTable
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
import plotly.express as px

dash.register_page(__name__)

survivor_colors = {"Hrdinové": "#f70000", "Rebelové": "#0122dc"}

# basedir = os.path.abspath(os.path.dirname(__file__))
event_log_df = pd.read_excel(
    # os.path.join(basedir, "..", "data\survivor_2023_data.xlsx"),
    "survivor_2023_data.xlsx",
    sheet_name="event_log",
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
personal_stats_df_heat["IMMUNITY_WINS"] = personal_stats_df_heat.apply(
    pd.Series.value_counts, axis=1
)[1]
# personal_stats_df_heat["POWER_INDEX"] = personal_stats_df_heat["POWER_INDEX"].transform(
#     lambda x: "{:,.2f}".format(x)
# )

players = {
    "Adam": {
        "profile_picture": "/assets/adam_profile_photo.jpg",
        "Jméno": "Adam Bůžek",
        "Věk": "22",
        "Povolání": "Osobní trenér",
    },
    "Andrea": {
        "profile_picture": "/assets/andrea_profile_photo.jpg",
        "Jméno": "Andrea Bezděková",
        "Věk": "27",
        "Povolání": "Miss ČR",
    },
    "Bára": {
        "profile_picture": "/assets/bara_profile_photo.jpg",
        "Jméno": "Barbora Mlejnková",
        "Věk": "31",
        "Povolání": "Pokrová hráčka",
    },
    "Barbora": {
        "profile_picture": "/assets/barbora_profile_photo.jpg",
        "Jméno": "Barbora Krčálová",
        "Věk": "21",
        "Povolání": "Studentka práv",
    },
    "Filip": {
        "profile_picture": "/assets/filip_profile_photo.jpg",
        "Jméno": "Filip Jánoš",
        "Věk": "26",
        "Povolání": "Youtuber",
    },
    "Hanka": {
        "profile_picture": "/assets/hanka_profile_photo.jpg",
        "Jméno": "Hana Gelnarová",
        "Věk": "21",
        "Povolání": "Barmanka",
    },
    "Jiří": {
        "profile_picture": "/assets/jiri_profile_photo.jpg",
        "Jméno": "Jiří Hanousek",
        "Věk": "33",
        "Povolání": "Realitní makléř",
    },
    "Johanka": {
        "profile_picture": "/assets/johanka_profile_photo.jpg",
        "Jméno": "Johana Fabišíková",
        "Věk": "29",
        "Povolání": "Tanečnice",
    },
    "Karolína": {
        "profile_picture": "/assets/karolina_profile_photo.jpg",
        "Jméno": "Karolína Krézlová",
        "Věk": "35",
        "Povolání": "Herečka",
    },
    "Kateřina": {
        "profile_picture": "/assets/katka_profile_photo.jpg",
        "Jméno": "Kateřina Klinderová",
        "Věk": "30",
        "Povolání": "Moderátorka",
    },
    "Kristián": {
        "profile_picture": "/assets/kristian_profile_photo.jpg",
        "Jméno": "Kristian Kundrata",
        "Věk": "26",
        "Povolání": "Obchodní zástupce",
    },
    "Kulhy": {
        "profile_picture": "/assets/kulhy_profile_photo.jpg",
        "Jméno": "Martin Kulhánek",
        "Věk": "28",
        "Povolání": "Reality Star",
    },
    "Lída": {
        "profile_picture": "/assets/ludmila_profile_photo.jpg",
        "Jméno": "Ludmila Puldová",
        "Věk": "55",
        "Povolání": "Průvodkyně",
    },
    "Martin": {
        "profile_picture": "/assets/martin_profile_photo.jpg",
        "Jméno": "Martin Konečný",
        "Věk": "45",
        "Povolání": "Technik",
    },
    "Matěj": {
        "profile_picture": "/assets/matej_profile_photo.jpg",
        "Jméno": "Matěj Quitt",
        "Věk": "32",
        "Povolání": "Interiérový designér",
    },
    "Pavlína": {
        "profile_picture": "/assets/pavlina_profile_photo.jpg",
        "Jméno": "Pavlína Sigmundová",
        "Věk": "23",
        "Povolání": "Herečka",
    },
    "Pepa": {
        "profile_picture": "/assets/pepa_profile_photo.jpg",
        "Jméno": "Josef Kůrka",
        "Věk": "31",
        "Povolání": "Model",
    },
    "Pítr": {
        "profile_picture": "/assets/pitr_profile_photo.jpg",
        "Jméno": "Petr Havránek",
        "Věk": "26",
        "Povolání": "Reality Star",
    },
    "Soňa": {
        "profile_picture": "/assets/sona_profile_photo.jpg",
        "Jméno": "Soňa Sedláčková",
        "Věk": "43",
        "Povolání": "Fitness influencerka",
    },
    "Švanci": {
        "profile_picture": "/assets/svanci_profile_photo.jpg",
        "Jméno": "Petr Švancara",
        "Věk": "45",
        "Povolání": "Fotbalista",
    },
    "Tereza": {
        "profile_picture": "/assets/tereza_profile_photo.jpg",
        "Jméno": "Tereza Schejbalová",
        "Věk": "22",
        "Povolání": "Atletka",
    },
    "Tomáš": {
        "profile_picture": "/assets/tomas_profile_photo.jpg",
        "Jméno": "Tomáš Weimann",
        "Věk": "33",
        "Povolání": "Trenér skateboardingu",
    },
    "Vašek": {
        "profile_picture": "/assets/vasek_profile_photo.jpg",
        "Jméno": "Václav Matějovský",
        "Věk": "26",
        "Povolání": "Herec",
    },
    "Žaneta": {
        "profile_picture": "/assets/zaneta_profile_photo.jpg",
        "Jméno": "Žaneta Skružná",
        "Věk": "23",
        "Povolání": "Vizážistka",
    },
}

vypadnuty = list(
    event_log_df[(event_log_df["EVENT_TYPE"].isin(["Duel", "Odstoupení"]))][
        "LOSING_ROSTER"
    ]
)

vypadnuty = vypadnuty + ([None] * (24 - len(vypadnuty)))

for player in players:
    players[player]["Imunity"] = len(
        event_log_df[
            (event_log_df["EVENT_TYPE"] == "Souboj o osobní imunitu")
            & (event_log_df["WINNING_ROSTER"] == player)
        ].index
    )
    players[player]["Duely"] = len(
        event_log_df[
            (event_log_df["EVENT_TYPE"] == "Duel")
            & (event_log_df["WINNING_ROSTER"] == player)
        ].index
    )
    players[player]["Poradie"] = (
        (24 - vypadnuty.index(player)) if player in vypadnuty else None
    )

print(players)
df_players = pd.DataFrame.from_dict(players, orient="index")
print(df_players)


def player_card(player):
    return dmc.Card(
        [
            dmc.Grid(
                [
                    dmc.Col(
                        [
                            dmc.Center(
                                [
                                    dmc.Text(
                                        players[player]["Jméno"], size="lg", weight=600
                                    ),
                                    dmc.Badge(
                                        ("TOP " + str(players[player]["Poradie"]))
                                        if players[player]["Poradie"] is not None
                                        else "Ve hře",
                                        variant="dot" if players[player]["Poradie"] is None else "outline",
                                        color="green" if players[player]["Poradie"] is None else "blue",
                                        size="lg",
                                        style={"margin-left": "8px"},
                                    ),
                                ]
                            )
                        ]
                    )
                ]
            ),
            dmc.Grid(
                [
                    dmc.Col(
                        [
                            dmc.Tooltip(
                                dmc.Avatar(
                                    src=players[player]["profile_picture"],
                                    radius="lg",
                                    size="lg",
                                ),
                                label=player,
                                position="top",
                                transition="pop",
                            )
                        ],
                        span="content",
                    ),
                    dmc.Col(
                        [
                            dmc.Grid(
                                [
                                    dmc.Col(
                                        [dmc.Text("Věk: " + players[player]["Věk"])],
                                        style={
                                            "padding-top": "4px",
                                            "padding-bottom": "6px",
                                        },
                                    )
                                ]
                            ),
                            dmc.Grid(
                                [
                                    dmc.Col(
                                        [
                                            dmc.Text(
                                                players[player]["Povolání"]
                                            )
                                        ],
                                        style={
                                            "padding-top": "0px",
                                            "padding-bottom": "8px",
                                        },
                                    )
                                ]
                            ),
                        ],
                        span="auto",
                    ),
                ]
            ),
            dmc.Grid(
                [
                    dmc.Col(
                        [dmc.Text("Úspěchy:", weight=600)],
                        style={"padding-bottom": "0px", "padding-top": "5px"},
                    )
                ]
            ),
            dmc.Grid(
                [
                    dmc.Col(
                        []
                        + (
                            [
                                dmc.Tooltip(
                                    DashIconify(
                                        icon="icon-park-outline:diamond-necklace",
                                        width=30,
                                        height=30,
                                    ),
                                    label="Osobní imunita",
                                    position="top",
                                    transition="pop",
                                )
                            ]
                            * players[player]["Imunity"]
                        )
                        + (
                            [
                                dmc.Tooltip(
                                    DashIconify(
                                        icon="material-symbols:swords-outline",
                                        width=30,
                                        height=30,
                                    ),
                                    label="Výhra v duelu",
                                    position="top",
                                    transition="pop",
                                )
                            ]
                            * players[player]["Duely"]
                        )
                    )
                ]
            ),
        ],
        withBorder=True,
        shadow="sm",
        radius="lg",
        style={"padding": "10px", "height": "20vh", "width": "15vw"},
    )


def best_players_card(card_label, title_icon, top_table, col_labels, by_id):
    return dmc.Card(
        [
            dmc.Grid(
                [
                    dmc.Col(
                        [
                            dmc.Center(
                                [
                                    DashIconify(
                                        icon=title_icon,
                                        width=20,
                                        height=20,
                                        style={
                                            "padding-top": "2px",
                                            "padding-right": "8px",
                                        },
                                    ),
                                    dmc.Text(card_label, weight=700, size="xl"),
                                ]
                            )
                        ],
                        style={"padding-bottom": "12px"},
                    )
                ]
            ),
            dmc.Grid(
                [
                    dmc.Col(
                        [
                            dmc.Grid(
                                [
                                    dmc.Col(
                                        [
                                            dmc.Tooltip(
                                                [
                                                    dmc.Avatar(
                                                        src=players[top_table.index[1]][
                                                            "profile_picture"
                                                        ],
                                                        radius="lg",
                                                        size="lg",
                                                    ),
                                                    DashIconify(
                                                        icon="twemoji:2nd-place-medal",
                                                        width=30,
                                                        height=30,
                                                        style={
                                                            "position": "absolute",
                                                            "transform": "translate(42px, -62px)",
                                                        },
                                                    ),
                                                ],
                                                label=top_table.index[0],
                                                position="top",
                                                transition="pop",
                                            )
                                        ],
                                        span="content",
                                        style={"padding-bottom": "2px"},
                                    ),
                                    dmc.Col(
                                        [
                                            dmc.Tooltip(
                                                [
                                                    dmc.Avatar(
                                                        src=players[top_table.index[0]][
                                                            "profile_picture"
                                                        ],
                                                        radius="lg",
                                                        size="xl",
                                                    ),
                                                    DashIconify(
                                                        icon="twemoji:1st-place-medal",
                                                        width=40,
                                                        height=40,
                                                        style={
                                                            "position": "absolute",
                                                            "transform": "translate(70px, -90px)",
                                                        },
                                                    ),
                                                ],
                                                label=top_table.index[0],
                                                position="top",
                                                transition="pop",
                                            )
                                        ],
                                        span="content",
                                        style={"padding-bottom": "2px"},
                                    ),
                                    dmc.Col(
                                        [
                                            dmc.Tooltip(
                                                [
                                                    dmc.Avatar(
                                                        src=players[top_table.index[2]][
                                                            "profile_picture"
                                                        ],
                                                        radius="lg",
                                                        size="lg",
                                                    ),
                                                    DashIconify(
                                                        icon="twemoji:3rd-place-medal",
                                                        width=30,
                                                        height=30,
                                                        style={
                                                            "position": "absolute",
                                                            "transform": "translate(42px, -62px)",
                                                        },
                                                    ),
                                                ],
                                                label=top_table.index[0],
                                                position="top",
                                                transition="pop",
                                            )
                                        ],
                                        span="content",
                                        style={"padding-bottom": "2px"},
                                    ),
                                ],
                                align="end",
                                justify="space-around",
                            ),
                            dmc.Grid(
                                [
                                    dmc.Col(
                                        [
                                            dmc.Text(
                                                by_id
                                                + ": "
                                                + str(
                                                    players[top_table.index[2]][by_id]
                                                ),
                                                color="dimmed",
                                                style={"padding-right": "16px"},
                                            )
                                        ],
                                        span="content",
                                        style={"padding-top": "4px"},
                                    ),
                                    dmc.Col(
                                        [
                                            dmc.Text(
                                                by_id
                                                + ": "
                                                + str(
                                                    players[top_table.index[1]][by_id]
                                                ),
                                                color="dimmed",
                                            )
                                        ],
                                        span="content",
                                        style={"padding-top": "4px"},
                                    ),
                                    dmc.Col(
                                        [
                                            dmc.Text(
                                                by_id
                                                + ": "
                                                + str(
                                                    players[top_table.index[3]][by_id]
                                                ),
                                                color="dimmed",
                                                style={"padding-left": "16px"},
                                            )
                                        ],
                                        span="content",
                                        style={"padding-top": "4px"},
                                    ),
                                ],
                                align="top",
                                justify="space-around",
                            ),
                        ]
                    )
                ]
            ),
            dmc.Grid(
                [
                    dmc.Col(
                        [
                            dmc.Accordion(
                                styles={
                                    "item": {"border": "none"},
                                    "chevron": {
                                        "width": 0,
                                        "min-width": 0,
                                        "margin": 0,
                                    },
                                    "control": {"padding": 0},
                                },
                                variant="filled",
                                chevron=None,
                                children=[
                                    dmc.AccordionItem(
                                        [
                                            dmc.AccordionControl(
                                                dmc.Center(
                                                    [
                                                        dmc.Text(
                                                            "Pořadí TOP5",
                                                            color="dimmed",
                                                            weight=600,
                                                        ),
                                                        DashIconify(
                                                            icon="mdi:keyboard-arrow-down",
                                                            style={
                                                                "padding-top": "4px",
                                                                "padding-left": "4px",
                                                                "color": "#868e96",
                                                            },
                                                            width=20,
                                                            height=20,
                                                        ),
                                                    ]
                                                )
                                            ),
                                            dmc.AccordionPanel(
                                                # DashMantineReactTable(
                                                #         data=personal_stats_df_heat.sort_values(["IMMUNITY_WINS", "POWER_INDEX"], ascending=False).iloc[0:5][["IMMUNITY_WINS", "POWER_INDEX"]].reset_index().to_dict("records"),
                                                #         columns=[{"accessorKey": "index", "header": "", "minSize": "100px"}, {"accessorKey": "IMMUNITY_WINS", "header": "Imunity", "minSize": "100px"}, {"accessorKey": "POWER_INDEX", "header": "Power Index", "minSize": "100px"}],
                                                #         mrtProps={
                                                #             "enableHiding": False,
                                                #             "enableColumnFilters": False,
                                                #             "enablePagination": False,
                                                #             "enableColumnActions": False,
                                                #             "enableSorting": False,
                                                #             "enableBottomToolbar": False,
                                                #             "enableTopToolbar": False,
                                                #             "initialState": {"density": "xs"},
                                                #             "mantineTableProps": {"fontSize": "md", "highlightOnHover": False, "withBorder": False, "verticalSpacing": "5px", "striped": True, "style": {"width": "auto"}},
                                                #             "mantineTableHeadCellProps": {"style": {"fontWeight": 500}},
                                                #             "mantinePaperProps": {"withBorder": False, "shadow": False},
                                                #         },
                                                #     ),
                                                DataTable(
                                                    data=top_table.reset_index().to_dict(
                                                        "records"
                                                    ),
                                                    columns=[
                                                        {"name": x, "id": y}
                                                        for x, y in zip(
                                                            col_labels,
                                                            top_table.reset_index().columns,
                                                        )
                                                    ],
                                                    style_data={"lineHeight": "8px"},
                                                    style_cell={
                                                        "backgroundColor": "#f8f9fa",
                                                        "font-family": "Segoe UI",
                                                        "font_size": "14px",
                                                        "padding": "5px",
                                                    },
                                                    style_as_list_view=True,
                                                    style_header={
                                                        "backgroundColor": "#f8f9fa",
                                                        "fontWeight": "bold",
                                                    },
                                                ),
                                            ),
                                        ],
                                        value="detail_poradia",
                                    ),
                                ],
                            )
                        ]
                    )
                ]
            ),
        ],
        withBorder=True,
        shadow="sm",
        radius="lg",
        style={
            # "width": "25vw",
            "padding": "10px",
            # "margin-left": "10px",
        },
    )


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
            bullet=DashIconify(icon="mdi:flag-variant-outline", width=27, height=27),
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
        # align="right",
        # styles={"itemContent": {"justify-content": "right", "display": "grid"}}
    )
    return dmc.Card(
        [eventlog],
        withBorder=True,
        shadow="sm",
        radius="lg",
        style={"padding": "10px", "padding-left": "20px", "padding-top": "20px"},
    )


def discrete_background_color_bins(df, n_bins=5, columns='all'):
    import colorlover
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    if columns == 'all':
        if 'id' in df:
            df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
        else:
            df_numeric_columns = df.select_dtypes('number')
    else:
        df_numeric_columns = df[columns]
    df_max = df_numeric_columns.max().max()
    df_min = df_numeric_columns.min().min()
    ranges = [
        ((df_max - df_min) * i) + df_min
        for i in bounds
    ]
    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        backgroundColor = colorlover.scales[str(n_bins)]['seq']['YlGn'][i - 1]
        color = 'white' if i > len(bounds) / 2. else 'inherit'

        for column in df_numeric_columns:
            styles.append({
                'if': {
                    'filter_query': (
                        '{{{column}}} >= {min_bound}' +
                        (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                    ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                    'column_id': column
                },
                'backgroundColor': backgroundColor,
                'color': color
            })

    return styles


layout = [
    dmc.Header(
        height=60,
        children=[
            dmc.Grid(
                [
                    dmc.Col(
                        [dmc.Text("SURVIVOR 2023 - Statistiky", weight=500, size=20)],
                        style={"padding-left": "30px"},
                    )
                ],
                align="center",
                style={"height": "60px"},
            )
        ],
    ),
    dmc.Grid(
        [
            dmc.Col(
                [
                    dmc.Grid(
                        [dmc.Col([dmc.Text("Nejlepší hráči:", size="xl", weight=600)])]
                    ),
                    dmc.Grid(
                        [
                            dmc.Col(
                                [
                                    best_players_card(
                                        "Král osobních imunit",
                                        "icon-park-outline:diamond-necklace",
                                        personal_stats_df_heat.sort_values(
                                            ["IMMUNITY_WINS", "POWER_INDEX"],
                                            ascending=False,
                                        ).iloc[0:5][["IMMUNITY_WINS", "POWER_INDEX"]],
                                        ["", "Immunity", "Power Index"],
                                        "Imunity",
                                    ),
                                ],
                                span=4,
                            ),
                            dmc.Col(
                                [
                                    best_players_card(
                                        "Královna duelů",
                                        "material-symbols:swords-outline",
                                        pd.DataFrame.from_dict(players, orient="index")
                                        .sort_values(
                                            ["Duely"],
                                            ascending=False,
                                        )
                                        .iloc[0:5][["Duely"]],
                                        ["", "Duely"],
                                        "Duely",
                                    ),
                                ],
                                span=4,
                            ),
                        ]
                    ),
                    dmc.Grid([dmc.Col([dmc.Text("Hráči:", size="xl", weight=600)])]),
                    dmc.ScrollArea(
                        dmc.Grid(
                            [
                                dmc.Col(player_card(player), span="content")
                                for player in list(
                                    df_players.sort_values(
                                        "Poradie", na_position="first"
                                    ).index
                                )
                            ],
                            style={"width": "380vw"},
                        ),
                        style={"height": "22vh", "padding": "8px"},
                        type="always",
                    ),
                    dmc.Grid([dmc.Col([dmc.Text("Individuálne výsledky:", size="xl", weight=600)])]),
                    dmc.Grid(
                        [
                            dmc.Col(
                                [
                                    # dag.AgGrid(
                                    #     id="survivor-personal-stats-grid",
                                    #     rowData=personal_stats_df_heat.reset_index().to_dict(
                                    #         "records"
                                    #     ),
                                    #     columnDefs=[
                                    #         {
                                    #             "field": i,
                                    #             "id": i,
                                    #             "type": "numericColumn",
                                    #         }
                                    #         for i in personal_stats_df_heat.reset_index().columns
                                    #     ],
                                    #     defaultColDef={
                                    #         "resizable": True,
                                    #         "sortable": True,
                                    #         "filter": True,
                                    #         "minWidth": 50,
                                    #     },
                                    #     columnSize="autoSizeAll",
                                    #     # getRowId="params.data.State",
                                    # )
                                    dmc.Card(
                                        [
                                            DataTable(
                                                data=personal_stats_df_heat.reset_index().to_dict(
                                                    "records"
                                                ),
                                                columns=[
                                                    {"name": x, "id": x}
                                                    for x in personal_stats_df_heat.reset_index().columns
                                                ],
                                                style_data={"lineHeight": "8px"},
                                                style_cell={
                                                    # "backgroundColor": "#f8f9fa",
                                                    "font-family": "Segoe UI",
                                                    "font_size": "14px",
                                                    "padding": "5px",
                                                },
                                                style_as_list_view=True,
                                                style_header={
                                                    "backgroundColor": "white",
                                                    "fontWeight": "bold",
                                                },
                                                style_data_conditional=discrete_background_color_bins(personal_stats_df_heat, columns=['POWER_INDEX'])
                                            ),
                                        ],
                                        withBorder=True,
                                        shadow="sm",
                                        radius="lg",
                                        style={"padding": "10px"},
                                    )
                                ]
                            )
                        ]
                    ),
                    dmc.Grid(
                        [
                            dmc.Col(
                                [
                                    dcc.Graph(
                                        id="survivor-personal-stats-heatmap",
                                        figure=px.imshow(
                                            personal_stats_df_heat.iloc[:, :-2],
                                            text_auto=True,
                                            color_continuous_scale="RdYlGn_r",
                                        ),
                                        style={"height": "90vh"},
                                    ),
                                ]
                            )
                        ]
                    ),
                ],
                span=8,
            ),
            dmc.Col(
                [
                    dmc.Grid(
                        [dmc.Col([dmc.Text("Časová osa:", size="xl", weight=600)])]
                    ),
                    dmc.Grid([dmc.Col([create_eventlog(event_log_df)])]),
                ],
                span=4,
            ),
        ],
        style={"padding": "20px"}
    ),
]
