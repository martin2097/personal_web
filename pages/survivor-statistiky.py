import dash
from dash import dcc, callback, Output, Input, State, html, clientside_callback
from dash.dash_table import DataTable
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
from plotly.express import imshow
from dash.dash_table.Format import Format, Scheme

dash.register_page(__name__, title="Survivor - Statistiky", description="Statistiky česko-slovenské verze reality show Survivor", image="survivor-statistky-nahlad.PNG")

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
    players[player]["Odměny"] = len(
        event_log_df[
            (event_log_df["EVENT_TYPE"] == "Souboj o odměnu")
            & (event_log_df["WINNING_ROSTER"].str.contains(player))
        ].index
    )
    players[player]["Poradie"] = (
        (24 - vypadnuty.index(player)) if player in vypadnuty else None
    )

df_players = pd.DataFrame.from_dict(players, orient="index")


def best_team(card_label, title_icon, by_id, num_label):
    if by_id == "all":
        df_team = event_log_df[(event_log_df["EVENT_TYPE"].isin(["Souboj o imunitu", "Souboj o odměnu"])) & (event_log_df["WINNING_SIDE"].isin(["Rebelové", "Hrdinové"]))][["DAY", 'WINNING_SIDE']].groupby(
            ['WINNING_SIDE']).count().reset_index().rename(columns={"DAY": "CNT"}).sort_values(["CNT"], ascending=False)
    else:
        df_team = event_log_df[(event_log_df["EVENT_TYPE"] == by_id) & (event_log_df["WINNING_SIDE"].isin(["Rebelové", "Hrdinové"]))][["DAY", 'WINNING_SIDE']].groupby(
            ['WINNING_SIDE']).count().reset_index().rename(columns={"DAY": "CNT"}).sort_values(["CNT"], ascending=False)
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
                                    ),
                                    dmc.Text(card_label, weight=700, size="xl", style={"padding-left": "6px"}),
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
                                                        DashIconify(icon="game-icons:eagle-emblem" if df_team["WINNING_SIDE"].values[0] == "Hrdinové" else "game-icons:tiger-head",
                                                                    style={"color": survivor_colors[df_team["WINNING_SIDE"].values[0]]},
                                                                    width=60,
                                                                    height=60,
                                                                    ),
                                                        radius="lg",
                                                        size="xl",
                                                        styles={"placeholder": {"background-color": "#d4dcde"}}
                                                    ),
                                                    DashIconify(
                                                        icon="twemoji:trophy",
                                                        width=30,
                                                        height=30,
                                                        style={
                                                            "position": "absolute",
                                                            "transform": "translate(70px, -90px)",
                                                        },
                                                    ),
                                                ],
                                                label=df_team["WINNING_SIDE"].values[0],
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
                                                        DashIconify(icon="game-icons:eagle-emblem" if df_team["WINNING_SIDE"].values[1] == "Hrdinové" else "game-icons:tiger-head",
                                                                    style={"color": survivor_colors[df_team["WINNING_SIDE"].values[1]]},
                                                                    width=35,
                                                                    height=35,),
                                                        radius="lg",
                                                        size="lg",
                                                        styles={"placeholder": {"background-color": "#d4dcde"}}
                                                    ),
                                                ],
                                                label=df_team["WINNING_SIDE"].values[1],
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
                                                num_label
                                                + ": "
                                                + str(
                                                    df_team["CNT"].values[0]
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
                                                num_label
                                                + ": "
                                                + str(
                                                    df_team["CNT"].values[1]
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
                                        variant="dot"
                                        if players[player]["Poradie"] is None
                                        else "outline",
                                        color="green"
                                        if players[player]["Poradie"] is None
                                        else "blue",
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
                                        [dmc.Text(players[player]["Povolání"])],
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
                []
                + (
                    [
                        dmc.Col(
                            dmc.Tooltip(
                                DashIconify(
                                    icon="icon-park-outline:diamond-necklace",
                                    width=30,
                                    height=30,
                                    style={"color": "#868e96"},
                                ),
                                label="Osobní imunita",
                                position="top",
                                transition="pop",
                            ),
                            span="content",
                            style={"padding-left": "4px", "padding-right": "4px"},
                        )
                    ]
                    * players[player]["Imunity"]
                )
                + (
                    [
                        dmc.Col(
                            dmc.Tooltip(
                                DashIconify(
                                    icon="material-symbols:swords-outline",
                                    width=30,
                                    height=30,
                                    style={"color": "#868e96"},
                                ),
                                label="Výhra v duelu",
                                position="top",
                                transition="pop",
                            ),
                            span="content",
                            style={"padding-left": "4px", "padding-right": "4px"},
                        )
                    ]
                    * players[player]["Duely"]
                )
                + (
                    [
                        dmc.Col(
                            dmc.Tooltip(
                                DashIconify(
                                    icon="material-symbols:token-outline",
                                    width=34,
                                    height=34,
                                    style={"color": "#868e96"},
                                ),
                                label=i,
                                position="top",
                                transition="pop",
                            ),
                            span="content",
                            style={"padding-left": "4px", "padding-right": "4px"},
                            pt=6,
                        )
                        for i in event_log_df[
                            (event_log_df["EVENT_TYPE"] == "Výhoda")
                            & (event_log_df["WINNING_ROSTER"] == player)
                        ]["EVENT_DESC"]
                    ]
                )
                + (
                    [
                        dmc.Col(
                            dmc.Tooltip(
                                DashIconify(
                                    icon="material-symbols:merge-rounded",
                                    width=36,
                                    height=36,
                                    style={"color": "#868e96"},
                                ),
                                label="Sloučení",
                                position="top",
                                transition="pop",
                            ),
                            span="content",
                            px=0,
                            pt=4,
                        )
                        if player in event_log_df[event_log_df["EVENT_TYPE"] == "Sloučení"]["WINNING_ROSTER"].values[0] else None
                    ]
                ),
                style={"padding-left": "8px"},
            ),
        ],
        withBorder=True,
        shadow="sm",
        radius="lg",
        style={
            "padding": "10px",
            "height": "170px",
            "width": "300px",
        },  # "height": "20vh", "width": "15vw"
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
                                    ),
                                    dmc.Text(card_label, weight=700, size="xl", style={"padding-left": "6px"}),
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
                                                label=top_table.index[1],
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
                                                        icon="twemoji:cupcake" if by_id == "Odměny" else "twemoji:1st-place-medal",
                                                        width=40,
                                                        height=40,
                                                        style={
                                                            "position": "absolute",
                                                            "transform": "translate(65px, -95px)" if by_id == "Odměny" else "translate(70px, -90px)",
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
                                                label=top_table.index[2],
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
                                                    players[top_table.index[1]][by_id]
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
                                                    players[top_table.index[0]][by_id]
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
                                                    players[top_table.index[2]][by_id]
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
                                                        {
                                                            "name": x,
                                                            "id": y,
                                                            "type": z,
                                                            "format": a,
                                                        }
                                                        for x, y, z, a in zip(
                                                            col_labels,
                                                            top_table.reset_index().columns,
                                                            [
                                                                "numeric"
                                                                if col == "POWER_INDEX"
                                                                else None
                                                                for col in top_table.reset_index().columns
                                                            ],
                                                            [
                                                                Format(
                                                                    precision=2,
                                                                    scheme=Scheme.fixed,
                                                                )
                                                                if col == "POWER_INDEX"
                                                                else None
                                                                for col in top_table.reset_index().columns
                                                            ],
                                                        )
                                                    ],
                                                    style_data={"lineHeight": "8px"},
                                                    style_cell={
                                                        "backgroundColor": "rgba(0,0,0,0)",
                                                        "font-family": "Segoe UI",
                                                        "font_size": "14px",
                                                        "padding": "5px",
                                                        "border": "none",
                                                    },
                                                    # style_as_list_view=True,
                                                    cell_selectable=False,
                                                    style_header={
                                                        "backgroundColor": "rgba(0,0,0,0)",
                                                        "fontWeight": "bold",
                                                        "border": "none",
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
            width=15,
            height=15,
        ),
        label=dmc.Grid(
            [
                dmc.Col(
                    [
                        DashIconify(
                            icon="mdi:movie-open-outline",
                            width=15,
                            height=15,
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
                        dmc.Text("Epizóda " + str(data_string["EPISODE"]), size="sm"),
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
                            width=15,
                            height=15,
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
                        dmc.Text(str(data_string["TIMESTAMP"]), size="sm"),
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
            "padding": "1px",
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
                                                            size="sm",
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "5px",
                                                        "padding-bottom": "4px",
                                                        "padding-right": "2px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [episode_timestamp],
                                                    span="content",
                                                    style={
                                                        "padding-top": "5px",
                                                        "padding-bottom": "4px",
                                                        "padding-left": "0px",
                                                    },
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
                                                            width=18,
                                                            height=18,
                                                            style={
                                                                "color": survivor_colors[
                                                                    data_string[
                                                                        "WINNING_SIDE"
                                                                    ]
                                                                ] if data_string[
                                                                        "WINNING_SIDE"
                                                                    ] in ["Hrdinové", "Rebelové"] else None,
                                                                "padding-top": "2px",
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                        "padding-right": "3px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            data_string["WINNING_SIDE"],
                                                            size="sm",
                                                            weight=700,
                                                            style={
                                                                "color": survivor_colors[
                                                                    data_string[
                                                                        "WINNING_SIDE"
                                                                    ]
                                                                ] if data_string[
                                                                        "WINNING_SIDE"
                                                                    ] in ["Hrdinové", "Rebelové"] else None
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                        "padding-left": "0px",
                                                        "padding-right": "4px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            "("
                                                            + data_string["SCORE"]
                                                            + ")",
                                                            size="sm",
                                                            color="dimmed",
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                        "padding-left": "0px",
                                                        "padding-right": "0px",
                                                    },
                                                ) if data_string["WINNING_SIDE"] in ["Hrdinové", "Rebelové"] else
                                                dmc.Col(
                                                    dmc.Grid(
                                                        [
                                                        dmc.Col(
                                                            [
                                                                dmc.Tooltip(
                                                                    dmc.Avatar(
                                                                        src=players[
                                                                            data_string[
                                                                                "WINNING_SIDE"
                                                                            ]
                                                                        ]["profile_picture"],
                                                                        radius="lg",
                                                                        size="sm",
                                                                    ),
                                                                    label=data_string[
                                                                        "WINNING_SIDE"
                                                                    ],
                                                                    position="top",
                                                                    transition="pop",
                                                                    style={
                                                                        "padding": "1px",
                                                                        "padding-left": "5px",
                                                                        "padding-right": "5px",
                                                                    },
                                                                ),

                                                            ],
                                                            span="content",
                                                            style={
                                                                "padding-top": "4px",
                                                                "padding-bottom": "5px",
                                                                "padding-left": "4px",
                                                            },
                                                        ),
                                                        dmc.Col(
                                                            [
                                                                DashIconify(
                                                                    icon="heroicons:user-group-solid",
                                                                    width=20,
                                                                    height=20,
                                                                    style={
                                                                        "padding-top": "4px",
                                                                    },
                                                                ),
                                                            ],
                                                            span="content",
                                                            style={
                                                                "padding-top": "4px",
                                                                "padding-bottom": "5px",
                                                                "padding-right": "0px",
                                                                "padding-left": "0px",
                                                                "margin-right": "-8px"
                                                            },
                                                        ),
                                                            ]
                                                    )
                                                            ,span="content",
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
                                                                        size="sm",
                                                                    ),
                                                                    label=member,
                                                                    position="top",
                                                                    transition="pop",
                                                                    style={
                                                                        "padding": "1px",
                                                                        "padding-left": "2px",
                                                                        "padding-right": "5px",
                                                                    },
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
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                    },
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
                    shadow="xs",
                    radius="lg",
                    style={
                        "width": "fit-content",
                        # "border-color": survivor_colors[data_string["WINNING_SIDE"]],
                        # "border-style": "solid",
                        # "border-width": "2px",
                        "padding": "5px",
                        "padding-left": "10px",
                        "padding-right": "10px",
                    },
                )
            ],
            style={"margin-top": "8px"},
            bullet=DashIconify(icon="mdi:gift-outline", width=17, height=17)
            if data_string["EVENT_TYPE"] == "Souboj o odměnu"
            else DashIconify(
                icon="material-symbols:shield-outline", width=17, height=17
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
                                                            size="sm",
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "5px",
                                                        "padding-bottom": "4px",
                                                        "padding-right": "2px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [episode_timestamp],
                                                    span="content",
                                                    style={
                                                        "padding-top": "5px",
                                                        "padding-bottom": "4px",
                                                        "padding-left": "0px",
                                                    },
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
                                                            width=18,
                                                            height=18,
                                                            style={
                                                                "color": survivor_colors[
                                                                    data_string[
                                                                        "WINNING_SIDE"
                                                                    ]
                                                                ] if data_string[
                                                                        "WINNING_SIDE"
                                                                    ] in ["Hrdinové", "Rebelové"] else None,
                                                                "padding-top": "2px",
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                        "padding-right": "3px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            data_string[
                                                                "WINNING_ROSTER"
                                                            ],
                                                            size="sm",
                                                            weight=700,
                                                            style={
                                                                "color": survivor_colors[
                                                                    data_string[
                                                                        "WINNING_SIDE"
                                                                    ]
                                                                ] if data_string[
                                                                        "WINNING_SIDE"
                                                                    ] in ["Hrdinové", "Rebelové"] else None
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
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
                                                                size="sm",
                                                            ),
                                                            label=data_string[
                                                                "WINNING_ROSTER"
                                                            ],
                                                            position="top",
                                                            transition="pop",
                                                            style={
                                                                "padding": "1px",
                                                                "padding-left": "5px",
                                                                "padding-right": "5px",
                                                            },
                                                        )
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                    },
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
                    shadow="xs",
                    radius="lg",
                    style={
                        "width": "fit-content",
                        # "border-color": "black",
                        # "border-style": "solid",
                        # "border-width": "2px",
                        "padding": "5px",
                        "padding-left": "10px",
                        "padding-right": "10px",
                    },
                )
            ],
            style={"margin-top": "8px"},
            bullet=DashIconify(
                icon="icon-park-solid:diamond-necklace", width=17, height=17
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
                                                            size="sm",
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "5px",
                                                        "padding-bottom": "4px",
                                                        "padding-right": "2px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [episode_timestamp],
                                                    span="content",
                                                    style={
                                                        "padding-top": "5px",
                                                        "padding-bottom": "4px",
                                                        "padding-left": "0px",
                                                    },
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
                                                            width=18,
                                                            height=18,
                                                            style={
                                                                "color": survivor_colors[
                                                                    data_string[
                                                                        "WINNING_SIDE"
                                                                    ]
                                                                ] if data_string[
                                                                        "WINNING_SIDE"
                                                                    ] in ["Hrdinové", "Rebelové"] else None,
                                                                "padding-top": "2px",
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                        "padding-right": "3px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            data_string[
                                                                "WINNING_ROSTER"
                                                            ],
                                                            size="sm",
                                                            weight=700,
                                                            style={
                                                                "color": survivor_colors[
                                                                    data_string[
                                                                        "WINNING_SIDE"
                                                                    ]
                                                                ] if data_string[
                                                                        "WINNING_SIDE"
                                                                    ] in ["Hrdinové", "Rebelové"] else None
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
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
                                                                size="sm",
                                                            ),
                                                            label=data_string[
                                                                "WINNING_ROSTER"
                                                            ],
                                                            position="top",
                                                            transition="pop",
                                                            style={
                                                                "padding": "1px",
                                                                "padding-left": "5px",
                                                                "padding-right": "5px",
                                                            },
                                                        )
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [
                                                        DashIconify(
                                                            icon="material-symbols:swords-outline",
                                                            width=18,
                                                            height=18,
                                                            style={
                                                                "padding-top": "2px",
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
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
                                                                size="sm",
                                                            ),
                                                            label=data_string[
                                                                "LOSING_ROSTER"
                                                            ],
                                                            position="top",
                                                            transition="pop",
                                                            style={
                                                                "padding": "1px",
                                                                "padding-left": "5px",
                                                                "padding-right": "5px",
                                                            },
                                                        )
                                                    ],
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                    },
                                                    span="content",
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            data_string[
                                                                "LOSING_ROSTER"
                                                            ],
                                                            size="sm",
                                                            weight=700,
                                                            style={
                                                                "color": survivor_colors[
                                                                    data_string[
                                                                        "WINNING_SIDE"
                                                                    ]
                                                                ] if data_string[
                                                                        "WINNING_SIDE"
                                                                    ] in ["Hrdinové", "Rebelové"] else None
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                        "padding-left": "0px",
                                                        "padding-right": "0px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [
                                                        DashIconify(
                                                            icon="mingcute:hand-finger-2-line",
                                                            width=18,
                                                            height=18,
                                                            style={
                                                                "color": survivor_colors[
                                                                    data_string[
                                                                        "WINNING_SIDE"
                                                                    ]
                                                                ] if data_string[
                                                                        "WINNING_SIDE"
                                                                    ] in ["Hrdinové", "Rebelové"] else None,
                                                                "padding-top": "2px",
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                        "padding-left": "3px",
                                                    },
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
                        # "border-color": "black",
                        # "border-style": "solid",
                        # "border-width": "2px",
                        "padding": "5px",
                        "padding-left": "10px",
                        "padding-right": "10px",
                    },
                )
            ],
            style={"margin-top": "8px"},
            bullet=DashIconify(
                icon="mdi:campfire",
                width=18,
                height=18,
                style={"padding-bottom": "1px"},
            ),
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
                                                            size="sm",
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "5px",
                                                        "padding-bottom": "4px",
                                                        "padding-right": "2px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [episode_timestamp],
                                                    span="content",
                                                    style={
                                                        "padding-top": "5px",
                                                        "padding-bottom": "4px",
                                                        "padding-left": "0px",
                                                    },
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
                                                            width=18,
                                                            height=18,
                                                            style={
                                                                "color": survivor_colors[
                                                                    data_string[
                                                                        "WINNING_SIDE"
                                                                    ]
                                                                ] if data_string[
                                                                        "WINNING_SIDE"
                                                                    ] in ["Hrdinové", "Rebelové"] else None,
                                                                "padding-top": "2px",
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                        "padding-right": "3px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            data_string[
                                                                "WINNING_ROSTER"
                                                            ],
                                                            size="sm",
                                                            weight=700,
                                                            style={
                                                                "color": survivor_colors[
                                                                    data_string[
                                                                        "WINNING_SIDE"
                                                                    ]
                                                                ] if data_string[
                                                                        "WINNING_SIDE"
                                                                    ] in ["Hrdinové", "Rebelové"] else None
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
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
                                                                size="sm",
                                                            ),
                                                            label=data_string[
                                                                "WINNING_ROSTER"
                                                            ],
                                                            position="top",
                                                            transition="pop",
                                                            style={
                                                                "padding": "1px",
                                                                "padding-left": "5px",
                                                                "padding-right": "5px",
                                                            },
                                                        )
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [
                                                        DashIconify(
                                                            icon="material-symbols:swords-outline",
                                                            width=18,
                                                            height=18,
                                                            style={
                                                                "padding-top": "2px",
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
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
                                                                size="sm",
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
                                                            style={
                                                                "padding": "1px",
                                                                "padding-left": "5px",
                                                                "padding-right": "5px",
                                                            },
                                                        )
                                                    ],
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                    },
                                                    span="content",
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            data_string[
                                                                "LOSING_ROSTER"
                                                            ],
                                                            size="sm",
                                                            weight=700,
                                                            color="dimmed",
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                        "padding-left": "0px",
                                                        "padding-right": "0px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [
                                                        DashIconify(
                                                            icon="material-symbols:person-remove-outline",
                                                            width=18,
                                                            height=18,
                                                            style={
                                                                "color": "#868e96",
                                                                "padding-top": "3px",
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                        "padding-left": "3px",
                                                    },
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
                        # "border-color": "black",
                        # "border-style": "solid",
                        # "border-width": "2px",
                        "padding": "5px",
                        "padding-left": "10px",
                        "padding-right": "10px",
                    },
                )
            ],
            style={"margin-top": "8px"},
            bullet=DashIconify(
                icon="material-symbols:swords-outline", width=17, height=17
            ),
        )
    elif data_string["EVENT_TYPE"] in ["Noví hráči", "Výměna členů"]:
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
                                                            size="sm",
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "5px",
                                                        "padding-bottom": "4px",
                                                        "padding-right": "2px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [episode_timestamp],
                                                    span="content",
                                                    style={
                                                        "padding-top": "5px",
                                                        "padding-bottom": "4px",
                                                        "padding-left": "0px",
                                                    },
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
                                                            size="sm",
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
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
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
                                                                        size="sm",
                                                                    ),
                                                                    label=member,
                                                                    position="top",
                                                                    transition="pop",
                                                                    style={
                                                                        "padding": "1px",
                                                                        "padding-left": "5px",
                                                                        "padding-right": "5px",
                                                                    },
                                                                )
                                                                for member in data_string[
                                                                    "WINNING_ROSTER"
                                                                ].split(
                                                                    ", "
                                                                )
                                                            ],
                                                        )
                                                    ],
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                    },
                                                    span="content",
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            data_string[
                                                                "LOSING_ROSTER"
                                                            ],
                                                            size="sm",
                                                            weight=700,
                                                            style={
                                                                "color": survivor_colors[
                                                                    "Rebelové"
                                                                ] if data_string["WINNING_SIDE"] == "Hrdinové" else survivor_colors[
                                                                    "Hrdinové"
                                                                ]
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
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
                                                                        size="sm",
                                                                    ),
                                                                    label=member,
                                                                    position="top",
                                                                    transition="pop",
                                                                    style={
                                                                        "padding": "1px",
                                                                        "padding-left": "5px",
                                                                        "padding-right": "5px",
                                                                    },
                                                                )
                                                                for member in data_string[
                                                                    "LOSING_ROSTER"
                                                                ].split(
                                                                    ", "
                                                                )
                                                            ],
                                                        )
                                                    ],
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                    },
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
                        # "border-color": "black",
                        # "border-style": "solid",
                        # "border-width": "2px",
                        "padding": "5px",
                        "padding-left": "10px",
                        "padding-right": "10px",
                    },
                )
            ],
            style={"margin-top": "8px"},
            bullet=DashIconify(
                icon="material-symbols:person-add-outline", width=18, height=18
            ) if data_string["EVENT_TYPE"] == "Noví hráči"
            else DashIconify(
                icon="material-symbols:sync", width=20, height=20
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
                                                            size="sm",
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "5px",
                                                        "padding-bottom": "4px",
                                                        "padding-right": "2px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [episode_timestamp],
                                                    span="content",
                                                    style={
                                                        "padding-top": "5px",
                                                        "padding-bottom": "4px",
                                                        "padding-left": "0px",
                                                    },
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
                                                            width=18,
                                                            height=18,
                                                            style={
                                                                "color": "#868e96",
                                                                "padding-top": "3px",
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                        "padding-right": "3px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            data_string[
                                                                "LOSING_ROSTER"
                                                            ],
                                                            size="sm",
                                                            weight=700,
                                                            color="dimmed",
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
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
                                                                size="sm",
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
                                                            style={
                                                                "padding": "1px",
                                                                "padding-left": "5px",
                                                                "padding-right": "5px",
                                                            },
                                                        )
                                                    ],
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                    },
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
                        # "border-color": "black",
                        # "border-style": "solid",
                        # "border-width": "2px",
                        "padding": "5px",
                        "padding-left": "10px",
                        "padding-right": "10px",
                    },
                )
            ],
            style={"margin-top": "8px"},
            bullet=DashIconify(
                icon="mdi:flag-variant-outline",
                width=20,
                height=20,
                style={"padding-left": "1px"},
            ),
        )
    elif data_string["EVENT_TYPE"] == "Výhoda":
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
                                                                +
                                                                " ("
                                                                + str(
                                                                    data_string[
                                                                        "EVENT_DESC"
                                                                    ]
                                                                )
                                                                + ")"
                                                            ],
                                                            weight=500,
                                                            size="sm",
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "5px",
                                                        "padding-bottom": "4px",
                                                        "padding-right": "2px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [episode_timestamp],
                                                    span="content",
                                                    style={
                                                        "padding-top": "5px",
                                                        "padding-bottom": "4px",
                                                        "padding-left": "0px",
                                                    },
                                                ),
                                            ],
                                            align="center",
                                        ),
                                        dmc.Grid(
                                            [
                                                dmc.Col(
                                                    [
                                                        DashIconify(
                                                            icon="material-symbols:trending-up",
                                                            width=18,
                                                            height=18,
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
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                        "padding-right": "3px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            data_string[
                                                                "WINNING_ROSTER"
                                                            ],
                                                            size="sm",
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
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                        "padding-left": "0px",
                                                        "padding-right": "4px",
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
                                                                        size="sm",
                                                                    ),
                                                                    label=member,
                                                                    position="top",
                                                                    transition="pop",
                                                                    style={
                                                                        "padding": "1px",
                                                                        "padding-left": "2px",
                                                                        "padding-right": "5px",
                                                                    },
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
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                        "padding-left": "0px",
                                                    },
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
                    shadow="xs",
                    radius="lg",
                    style={
                        "width": "fit-content",
                        # "border-color": survivor_colors[data_string["WINNING_SIDE"]],
                        # "border-style": "solid",
                        # "border-width": "2px",
                        "padding": "5px",
                        "padding-left": "10px",
                        "padding-right": "10px",
                    },
                )
            ],
            style={"margin-top": "8px"},
            bullet=DashIconify(icon="material-symbols:token-outline", width=20, height=20)
        )
    elif data_string["EVENT_TYPE"] in ["Sloučení"]:
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
                                                            size="sm",
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "5px",
                                                        "padding-bottom": "4px",
                                                        "padding-right": "2px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [episode_timestamp],
                                                    span="content",
                                                    style={
                                                        "padding-top": "5px",
                                                        "padding-bottom": "4px",
                                                        "padding-left": "0px",
                                                    },
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
                                                            width=18,
                                                            height=18,
                                                            style={
                                                                "padding-top": "2px",
                                                            },
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                        "padding-right": "3px",
                                                    },
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            data_string["WINNING_SIDE"],
                                                            size="sm",
                                                            weight=700,
                                                        ),
                                                    ],
                                                    span="content",
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                        "padding-left": "0px",
                                                        "padding-right": "4px",
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
                                                                        size="sm",
                                                                    ),
                                                                    label=member,
                                                                    position="top",
                                                                    transition="pop",
                                                                    style={
                                                                        "padding": "1px",
                                                                        "padding-left": "2px",
                                                                        "padding-right": "5px",
                                                                    },
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
                                                    style={
                                                        "padding-top": "4px",
                                                        "padding-bottom": "5px",
                                                    },
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
                    shadow="xs",
                    radius="lg",
                    style={
                        "width": "fit-content",
                        # "border-color": survivor_colors[data_string["WINNING_SIDE"]],
                        # "border-style": "solid",
                        # "border-width": "2px",
                        "padding": "5px",
                        "padding-left": "10px",
                        "padding-right": "10px",
                    },
                )
            ],
            style={"margin-top": "8px"},
            bullet=DashIconify(icon="material-symbols:merge-rounded", width=20, height=20)
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


def create_event_log(data):
    items = []
    for i in range(len(data.index) - 1, -1, -1):
        items.append(eventlog_item(data.iloc[i]))
    eventlog = dmc.Timeline(
        active=len(data.index),
        bulletSize=25,
        lineWidth=1,
        children=items,
        color="gray",
        # align="right",
        # styles={"itemContent": {"justify-content": "right", "display": "grid"}}
    )
    return eventlog

def discrete_background_color_bins(df, n_bins=5, columns="all"):
    import colorlover

    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    if columns == "all":
        if "id" in df:
            df_numeric_columns = df.select_dtypes("number").drop(["id"], axis=1)
        else:
            df_numeric_columns = df.select_dtypes("number")
    else:
        df_numeric_columns = df[columns]
    df_max = df_numeric_columns.max().max()
    df_min = df_numeric_columns.min().min()
    ranges = [((df_max - df_min) * i) + df_min for i in bounds]
    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        backgroundColor = colorlover.scales[str(n_bins)]["seq"]["YlGn"][i - 1]
        color = "white" if i > len(bounds) / 2.0 else "inherit"

        for column in df_numeric_columns:
            styles.append(
                {
                    "if": {
                        "filter_query": (
                            "{{{column}}} >= {min_bound}"
                            + (
                                " && {{{column}}} < {max_bound}"
                                if (i < len(bounds) - 1)
                                else ""
                            )
                        ).format(
                            column=column, min_bound=min_bound, max_bound=max_bound
                        ),
                        "column_id": column,
                    },
                    "backgroundColor": backgroundColor,
                    "color": color,
                }
            )

    return styles


def layout():
    return [
        dmc.Header(
            height=60,
            children=[
                dmc.Grid(
                    [
                        dmc.Col(
                            [
                                dmc.MediaQuery(
                                    dmc.Container([
                                        dmc.Text(
                                            "SURVIVOR 2023", weight=500, size=20
                                        ),
                                    ], style={"padding": "0px", "padding-left": "10px"}),
                                    largerThan="sm",
                                    styles={"display": "none"},
                                ),
                                dmc.MediaQuery(
                                    dmc.Container([
                                        dmc.Text(
                                            "SURVIVOR 2023 - Statistiky", weight=500, size=20
                                        ),
                                    ], style={"padding": "0px", "padding-left": "30px"}),
                                    smallerThan="sm",
                                    styles={"display": "none"},
                                ),
                            ],
                            span="content",

                        ),
                        dmc.Col([
                            dmc.MediaQuery(
                            dmc.Container([
                            dmc.Grid([
                                dmc.Col([
                                    dmc.ActionIcon(
                                        DashIconify(
                                            icon="radix-icons:blending-mode", width=30
                                        ),
                                        size="lg",
                                        id="color-scheme-toggle",
                                    ),
                                ], span="content", style={"padding": "0px"}),
                                dmc.Col([
                                    html.A(
                                        dmc.Tooltip(
                                            dmc.ActionIcon(
                                                DashIconify(icon="mdi:github", width=30),
                                                size="lg"
                                            ),
                                            label="Github",
                                            position="top",
                                            transition="pop",
                                        ),
                                        href="https://github.com/martin2097/",
                                        target="_blank",
                                    ),
                                ], span="content", style={"padding": "0px"}),
                                dmc.Col([
                                    html.A(
                                        dmc.Tooltip(
                                            dmc.ActionIcon(
                                                DashIconify(icon="mdi:linkedin", width=30),
                                                size="lg"
                                            ),
                                            label="Linkedin",
                                            position="top",
                                            transition="pop",
                                        ),
                                        href="https://linkedin.com/in/martin-rapavy",
                                        target="_blank",
                                    )
                                ], span="content", style={"padding": "0px", "padding-right": "10px"}),
                            ])
                                ], style={"padding": "0px"}),
                                    largerThan="sm",
                                    styles={"padding-right": "20px"}
                                )
                        ],
                            span="content",

                        )
                    ],
                    align="center",
                    justify="space-between",
                    style={"height": "60px", "margin": "0px"},
                )
            ],
        ),
        dmc.Grid(
            [
                dmc.Col(
                    [
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [dmc.Text("Nejlepší hráči:", size="xl", weight=600)]
                                )
                            ]
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
                                            ).iloc[0:5][
                                                ["IMMUNITY_WINS", "POWER_INDEX"]
                                            ],
                                            ["", "Immunity", "Power Index"],
                                            "Imunity",
                                        ),
                                    ],
                                    xl=4,
                                    sm=6,
                                ),
                                dmc.Col(
                                    [
                                        best_players_card(
                                            "Královna duelů",
                                            "material-symbols:swords-outline",
                                            pd.DataFrame.from_dict(
                                                players, orient="index"
                                            )
                                            .sort_values(
                                                ["Duely"],
                                                ascending=False,
                                            )
                                            .iloc[0:5][["Duely"]],
                                            ["", "Duely"],
                                            "Duely",
                                        ),
                                    ],
                                    xl=4,
                                    sm=6,
                                ),
                                dmc.Col(
                                    [
                                        best_players_card(
                                            "Účasti na odměnách",
                                            "mdi:gift-outline",
                                            pd.DataFrame.from_dict(
                                                players, orient="index"
                                            )
                                            .sort_values(
                                                ["Odměny"],
                                                ascending=False,
                                            )
                                            .iloc[0:5][["Odměny"]],
                                            ["", "Odměny"],
                                            "Odměny",
                                        ),
                                    ],
                                    xl=4,
                                    sm=6,
                                ),
                            ]
                        ),
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [dmc.Text("Týmové výkony:", size="xl", weight=600)]
                                )
                            ]
                        ),
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        best_team(
                                            "Celková vítězství",
                                            "mdi:trophy",
                                            "all",
                                            "Výhry",
                                        )
                                    ],
                                    xl=4,
                                    sm=6,
                                ),
                                dmc.Col(
                                    [
                                        best_team(
                                            "Souboje o imunity",
                                            "game-icons:diablo-skull",
                                            "Souboj o imunitu",
                                            "Imunity",
                                        )
                                    ],
                                    xl=4,
                                    sm=6,
                                ),
                                dmc.Col(
                                    [
                                        best_team(
                                            "Souboje o odměnu",
                                            "mdi:gift-outline",
                                            "Souboj o odměnu",
                                            "Odměny",
                                        )
                                    ],
                                    xl=4,
                                    sm=6,
                                ),
                            ]
                        ),
                        dmc.Grid(
                            [dmc.Col([dmc.Text("Hráči:", size="xl", weight=600)])]
                        ),
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        dmc.ScrollArea(
                                            dmc.Grid(
                                                [
                                                    dmc.Col(
                                                        player_card(player),
                                                        span="content",
                                                    )
                                                    for player in list(
                                                        df_players.sort_values(
                                                            "Poradie",
                                                            na_position="first",
                                                        ).index
                                                    )
                                                ],
                                                style={"width": "7584px"},
                                            ),
                                            style={"height": "196px", "padding": "8px"},
                                            type="always",
                                        ),
                                    ], style={"padding": "0px"}
                                )
                            ]
                        ),
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        dmc.Text(
                                            "Vývoj Power Indexu:", size="xl", weight=600
                                        ),
                                    ],
                                    span="content",
                                ),
                                dmc.Col(
                                    [
                                        dmc.Grid(
                                            [
                                                dmc.Col(
                                                    [
                                                        dmc.Switch(
                                                            id="power_index_active_switch",
                                                            size="md",
                                                            radius="lg",
                                                            label="Aktivní hráči",
                                                            checked=False,
                                                        )
                                                    ],
                                                    span="content",
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Switch(
                                                            id="power_index_current_switch",
                                                            size="md",
                                                            radius="lg",
                                                            label="Aktualní forma",
                                                            checked=False,
                                                        )
                                                    ],
                                                    span="content",
                                                ),
                                            ],
                                            align="flex-end",
                                        ),
                                    ],
                                    span="content",
                                ),
                            ],
                            justify="space-between",
                            align="flex-end",
                        ),
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        dmc.Card(
                                            [
                                                dmc.Grid(
                                                    [
                                                        dmc.Col(
                                                            [
                                                                dmc.ScrollArea([
                                                                    dmc.Grid([
                                                                        dmc.Col([
                                                                            dcc.Graph(
                                                                                id="power_index_history_heatmap",
                                                                                # style={"height": "90vh"},
                                                                                config={
                                                                                    "staticPlot": True
                                                                                },
                                                                            ),
                                                                        ], span="content", style={"padding": "0px"})
                                                                    ], justify="center", style={"margin": "0px"})
                                                                ])
                                                            ],
                                                        )
                                                    ]
                                                ),
                                            ],
                                            withBorder=True,
                                            shadow="sm",
                                            radius="lg",
                                            style={
                                                "padding": "10px",
                                            },
                                        ),
                                    ]
                                )
                            ]
                        ),
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        dmc.Text(
                                            "Individuálne výsledky:",
                                            size="xl",
                                            weight=600,
                                        )
                                    ]
                                )
                            ]
                        ),
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        dmc.Card(
                                            [
                                                DataTable(
                                                    data=personal_stats_df_heat.reset_index().to_dict(
                                                        "records"
                                                    ),
                                                    columns=[
                                                        {
                                                            "name": y,
                                                            "id": x,
                                                            "type": "numeric"
                                                            if x == "POWER_INDEX"
                                                            else None,
                                                            "format": Format(
                                                                precision=2,
                                                                scheme=Scheme.fixed,
                                                            )
                                                            if x == "POWER_INDEX"
                                                            else None,
                                                        }
                                                        for x, y in zip(
                                                            [
                                                                "index",
                                                                "POWER_INDEX",
                                                                "IMMUNITY_WINS",
                                                            ]
                                                            + list(
                                                                personal_stats_df_heat.reset_index()
                                                                .iloc[:, 1:-2]
                                                                .columns
                                                            ),
                                                            [
                                                                "Hráč",
                                                                "Power Index",
                                                                "Imunity",
                                                            ]
                                                            + list(
                                                                i
                                                                for i in personal_stats_df_heat.reset_index()
                                                                .iloc[:, 1:-2]
                                                                .columns
                                                            ),
                                                        )  # "Den " +
                                                    ],
                                                    style_table={"overflowX": "auto"},
                                                    # fill_width=False,
                                                    style_data={
                                                        "lineHeight": "8px",
                                                        "minWidth": "50px",
                                                        "border": "none",
                                                    },
                                                    style_cell={
                                                        "backgroundColor": "rgba(0,0,0,0)",
                                                        "font-family": "Segoe UI",
                                                        "font_size": "14px",
                                                        "padding": "5px",
                                                        "border": "none",
                                                    },
                                                    cell_selectable=False,
                                                    # style_as_list_view=True,
                                                    style_header={
                                                        "backgroundColor": "rgba(0,0,0,0)",
                                                        "fontWeight": "bold",
                                                    },
                                                    style_data_conditional=discrete_background_color_bins(
                                                        personal_stats_df_heat,
                                                        columns=["POWER_INDEX"],
                                                    ),
                                                ),
                                            ],
                                            withBorder=True,
                                            shadow="sm",
                                            radius="lg",
                                            style={"padding": "20px"},
                                        )
                                    ]
                                )
                            ]
                        ),
                    ],
                    xl=9,
                    lg=8,
                ),
                dmc.Col(
                    [
                        dmc.Grid(
                            [dmc.Col([dmc.Text("Časová osa:", size="xl", weight=600)])]
                        ),
                        dmc.Grid([dmc.Col([dmc.Card(
                            children=[dmc.Grid([
                                dmc.Col([
                                    create_event_log(event_log_df.tail(31))
                                ],
                            id="event-log-output",)
                            ]),
                            dmc.Grid([
                                dmc.Col([
                                    dmc.Button(
                                        "Ukázat vše",
                                        id="event-log-more-button",
                                        variant="light",
                                        size="md",
                                        radius="xl",
                                        color="gray",
                                        fullWidth=True,
                                        leftIcon=DashIconify(icon="material-symbols:expand-more-rounded", width=25, height=25),
                                    ),
                                ], span="auto", style={"padding-top": "16px"}
                                )
                            ], justify="center")],
                            withBorder=True,
                            shadow="sm",
                            radius="lg",
                            style={"padding": "10px"},
                        )])]),
                    ],
                    xl=3,
                    lg=4,
                ),
            ],
            gutterLg=40, style={"margin": "0px"}
        ),
        dmc.Center(
            my=20,
            children=dmc.Group(
                spacing="xs",
                children=[
                    dmc.Text("Made with"),
                    DashIconify(
                        icon="akar-icons:heart",
                        width=19,
                        color=dmc.theme.DEFAULT_COLORS["red"][8],
                    ),
                    dmc.Text("by Martin Rapavý"),
                ],
            ),
        ),
    ]


@callback(
    Output("power_index_history_heatmap", "figure"),
    Input("power_index_active_switch", "checked"),
    Input("power_index_current_switch", "checked"),
    Input("theme-store", "data"),
)
def update_line_chart(active_player, current_form, theme):
    current_form_index = 5
    personal_stats_df_pi_history = personal_stats_df_heat[
        list(personal_stats_df_heat.columns)[:-2]
    ].copy()
    for i in personal_stats_df_heat[list(personal_stats_df_heat.columns)[:-2]].columns:
        ind = personal_stats_df_heat[
            list(personal_stats_df_heat.columns)[:-2]
        ].columns.get_loc(i)
        if current_form & (ind > (current_form_index - 1)):
            min_ind = ind - (current_form_index - 1)
        else:
            min_ind = 0
        personal_stats_df_pi_history[i] = (
            1
            - (
                personal_stats_df_heat[list(personal_stats_df_heat.columns)[:-2]].iloc[
                    :, min_ind : ind + 1
                ]
                - 1
            ).div(
                personal_stats_df_heat[list(personal_stats_df_heat.columns)[:-2]]
                .iloc[:, min_ind : ind + 1]
                .count(axis=0)
                - 1
            )
        ).mean(axis=1)
    if active_player:
        dff = pd.DataFrame.from_dict(players, orient="index")
        active_players = list(dff[dff["Poradie"].isna()].index)
        width = 600
    else:
        dff = pd.DataFrame.from_dict(players, orient="index")
        active_players = list(dff.index)
        width = 1200
    fig_hm = imshow(
        personal_stats_df_pi_history.filter(items=active_players, axis=0).T,
        text_auto=".2f",
        range_color=[0, 1],
        color_continuous_scale="RdYlGn",
        height=550,
        width=width,
    )
    fig_hm.update_layout(
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(
            family="Segoe UI",
            size=14,
        ),
        margin=dict(r=0, b=10, t=10),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        modebar=dict(
            bgcolor="rgba(0, 0, 0, 0)",
            color="rgba(0, 0, 0, 0.3)",
            activecolor="rgba(0, 0, 0, 0.3)",
        ),
        yaxis_title=None,
        xaxis=dict(showgrid=False, color="#444" if theme["colorScheme"] == "light" else "#FFFFFF"),
        yaxis=dict(showgrid=False, color="#444" if theme["colorScheme"] == "light" else "#FFFFFF"),
    )
    fig_hm.update_coloraxes(showscale=False)
    return fig_hm


@callback(
    Output("event-log-output", "children"),
    Output("event-log-more-button", "children"),
    Output("event-log-more-button", "leftIcon"),
    Input("event-log-more-button", "n_clicks"),
    prevent_initial_call=True,
)
def update_eventlog(more_n_clicks):
    data = event_log_df.copy()
    if more_n_clicks is None:
        more_n_clicks = 0
    if more_n_clicks % 2 == 0:
        data = data.tail(31)
        text = "Ukázat vše"
        icon = DashIconify(icon="material-symbols:expand-more-rounded", width=25, height=25),
    else:
        text = "Skrýt"
        icon = DashIconify(icon="material-symbols:expand-less-rounded", width=25, height=25),
    eventlog = create_event_log(data)
    return eventlog, text, icon


clientside_callback(
    """ function(data) { return data } """,
    Output("mantine-docs-theme-provider", "theme"),
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
            return { colorScheme: "light" }
        }
    }""",
    Output("theme-store", "data"),
    Input("color-scheme-toggle", "n_clicks"),
    State("theme-store", "data"),
)
