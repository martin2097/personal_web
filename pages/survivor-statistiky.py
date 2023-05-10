import dash
from dash import dcc, callback, Output, Input, State, html, clientside_callback, ALL, ctx
from dash.exceptions import PreventUpdate
from dash.dash_table import DataTable
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import pandas as pd
from plotly.express import imshow, line, bar
from dash.dash_table.Format import Format, Scheme
import numpy as np

dash.register_page(
    __name__,
    title="Survivor Česko & Slovensko - Statistiky",
    description="Statistiky reality show Survivor Česko & Slovensko. Podrobné spracování průběhu jednotlivých řad, rekordy, hlasování na kmenových radách a statistika soubojů.",
    image="survivor-statistky-nahlad.PNG",
    redirect_from=["/survivor", "/statistiky-survivor", "/survivor-statistics"]
)

survivor_colors = {"Hrdinové": "#f70000", "Rebelové": "#0122dc"}

# basedir = os.path.abspath(os.path.dirname(__file__))
event_log_df = pd.read_excel(
    # os.path.join(basedir, "..", "data\survivor_2023_data.xlsx"),
    "survivor_2023_data.xlsx",
    sheet_name="event_log",
)
sledovanost_df = pd.read_excel(
    # os.path.join(basedir, "..", "data\survivor_2023_data.xlsx"),
    "survivor_2023_data.xlsx",
    sheet_name="sledovanost",
)
kmenovky_hlasovani_df = pd.read_excel(
    # os.path.join(basedir, "..", "data\survivor_2023_data.xlsx"),
    "survivor_2023_data.xlsx",
    sheet_name="kmenovky_hlasovani",
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
vypadnuty_den = list(
    event_log_df[(event_log_df["EVENT_TYPE"].isin(["Duel", "Odstoupení"]))]["DAY"]
)
den_vypadnutia = {}
for i in range(len(vypadnuty)):
    den_vypadnutia[vypadnuty[i]] = vypadnuty_den[i]

poradie_vypadnutych = vypadnuty.copy()
for i in players:
    if i not in poradie_vypadnutych:
        poradie_vypadnutych.append(i)
poradie_vypadnutych.reverse()

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
            (event_log_df["EVENT_TYPE"].isin(["Souboj o odměnu", "Odměna"]))
            & (event_log_df["WINNING_ROSTER"].str.contains(player))
        ].index
    )
    players[player]["Poradie"] = (
        (24 - vypadnuty.index(player)) if player in vypadnuty else None
    )
    players[player]["Skryté Imunity"] = len(
        event_log_df[
            (event_log_df["EVENT_TYPE"] == "Výhoda")
            & (event_log_df["WINNING_ROSTER"] == player)
            & (event_log_df["EVENT_DESC"] == "Skrytá imunita")
        ].index
    )
    players[player]["Výhody"] = len(
        event_log_df[
            (event_log_df["EVENT_TYPE"] == "Výhoda")
            & (event_log_df["WINNING_ROSTER"] == player)
            & (event_log_df["EVENT_DESC"] != "Skrytá imunita")
        ].index
    )
    try:
        players[player]["Den vypadnutia"] = den_vypadnutia[player]
    except KeyError:
        players[player]["Den vypadnutia"] = None

df_players = pd.DataFrame.from_dict(players, orient="index")

hlasovani_vypad_df = pd.merge(
    kmenovky_hlasovani_df[kmenovky_hlasovani_df["TYPE"] == "Primární"],
    event_log_df[event_log_df["EVENT_TYPE"] == "Kmenová rada"],
    how="left",
    left_on=["DAY", "EPISODE"],
    right_on=["DAY", "EPISODE"],
)
uspesne_hlasovani = {}
for p in players:
    uspesne_hlasovani[p] = len(
        hlasovani_vypad_df[
            hlasovani_vypad_df[p] == hlasovani_vypad_df["WINNING_ROSTER"]
        ].index
    )
df_uspesne_hlasovani = pd.DataFrame.from_dict(
    uspesne_hlasovani, orient="index", columns=["Vyhlasování"]
)

hlasovani_nezapoc_df = pd.merge(
    kmenovky_hlasovani_df[kmenovky_hlasovani_df["TYPE"] == "Primární"],
    event_log_df[(event_log_df["EVENT_TYPE"] == "Výhoda") & (event_log_df["EVENT_DESC"] == "Skrytá imunita")],
    how="left",
    left_on=["DAY", "EPISODE"],
    right_on=["DAY", "EPISODE"],
)
df_nezapocitane_hlasy = pd.DataFrame()
for p in players:
    one_df = hlasovani_nezapoc_df[
            hlasovani_nezapoc_df[p] == hlasovani_nezapoc_df["LOSING_ROSTER"]
        ].value_counts(subset=[p]).rename_axis("unique_values").reset_index(name="cnt").set_index("unique_values")
    df_nezapocitane_hlasy = pd.concat([df_nezapocitane_hlasy, one_df])
df_nezapocitane_hlasy = df_nezapocitane_hlasy.groupby(["unique_values"])["cnt"].sum().reset_index().set_index("unique_values")


def information_bubble(content_container, desktop_width=800):
    return dmc.Menu(
        transition="pop",
        shadow="sm",
        radius="lg",
        position="bottom-start",
        # withArrow=True,
        offset=0,
        # arrowSize=10,
        children=[
            dmc.MenuTarget(
                DashIconify(
                    icon="material-symbols:info-outline",
                    width=25,
                )
            ),
            dmc.MenuDropdown(
                dmc.MediaQuery(
                    dmc.Container(
                        content_container,
                        p=10,
                        style={
                            "max-width": "97vw"
                        },
                    ),
                    largerThan="sm",
                    styles={
                        "max-width": str(desktop_width) + "px"
                    },
                )
            ),
        ],
    )


def avatar_group(members, avatar_style):
    return dmc.AvatarGroup(
        children=[
            dmc.Tooltip(
                dmc.Avatar(
                    src=players[member]["profile_picture"],
                    radius="lg",
                    size="sm",
                    style=avatar_style,
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
            for member in members
        ],
    )


def best_team(card_label, title_icon, by_id, num_label):
    if by_id == "all":
        df_team = (
            event_log_df[
                (
                    event_log_df["EVENT_TYPE"].isin(
                        ["Souboj o imunitu", "Souboj o odměnu"]
                    )
                )
                & (event_log_df["WINNING_SIDE"].isin(["Rebelové", "Hrdinové"]))
            ][["DAY", "WINNING_SIDE"]]
            .groupby(["WINNING_SIDE"])
            .count()
            .reset_index()
            .rename(columns={"DAY": "CNT"})
            .sort_values(["CNT"], ascending=False)
        )
    else:
        df_team = (
            event_log_df[
                (event_log_df["EVENT_TYPE"] == by_id)
                & (event_log_df["WINNING_SIDE"].isin(["Rebelové", "Hrdinové"]))
            ][["DAY", "WINNING_SIDE"]]
            .groupby(["WINNING_SIDE"])
            .count()
            .reset_index()
            .rename(columns={"DAY": "CNT"})
            .sort_values(["CNT"], ascending=False)
        )
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
                                    dmc.Text(
                                        card_label,
                                        weight=700,
                                        size="xl",
                                        style={"padding-left": "6px"},
                                    ),
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
                                                        DashIconify(
                                                            icon="game-icons:eagle-emblem"
                                                            if df_team[
                                                                "WINNING_SIDE"
                                                            ].values[0]
                                                            == "Hrdinové"
                                                            else "game-icons:tiger-head",
                                                            style={
                                                                "color": survivor_colors[
                                                                    df_team[
                                                                        "WINNING_SIDE"
                                                                    ].values[0]
                                                                ]
                                                            },
                                                            width=60,
                                                            height=60,
                                                        ),
                                                        radius="lg",
                                                        size="xl",
                                                        styles={
                                                            "placeholder": {
                                                                "background-color": "#d4dcde"
                                                            }
                                                        },
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
                                                        DashIconify(
                                                            icon="game-icons:eagle-emblem"
                                                            if df_team[
                                                                "WINNING_SIDE"
                                                            ].values[1]
                                                            == "Hrdinové"
                                                            else "game-icons:tiger-head",
                                                            style={
                                                                "color": survivor_colors[
                                                                    df_team[
                                                                        "WINNING_SIDE"
                                                                    ].values[1]
                                                                ]
                                                            },
                                                            width=35,
                                                            height=35,
                                                        ),
                                                        radius="lg",
                                                        size="lg",
                                                        styles={
                                                            "placeholder": {
                                                                "background-color": "#d4dcde"
                                                            }
                                                        },
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
                                                + str(df_team["CNT"].values[0]),
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
                                                + str(df_team["CNT"].values[1]),
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
            dmc.Stack([
                dmc.Grid([
                    dmc.Col([
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
                                            style={
                                                "padding-left": "4px",
                                                "padding-right": "4px",
                                                "padding-bottom": "0px",
                                            },
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
                                            style={
                                                "padding-left": "4px",
                                                "padding-right": "4px",
                                                "padding-bottom": "0px",
                                            },
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
                                        style={
                                            "padding-left": "4px",
                                            "padding-right": "4px",
                                            "padding-bottom": "0px",
                                        },
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
                                        pb=0,
                                    )
                                    if player
                                       in event_log_df[event_log_df["EVENT_TYPE"] == "Sloučení"][
                                           "WINNING_ROSTER"
                                       ].values[0]
                                    else None
                                ]
                            ),
                            style={"padding-left": "8px"},
                        ),
                    ])
                ]),
                dmc.Grid([
                    dmc.Col([
                        dmc.Button(
                            "Zobrazit detail soutěžícího",
                            id={"type": "show-player-detail", "subtype": player},
                            fullWidth=True,
                            variant="light",
                            color="gray",
                            radius="xl",
                            leftIcon=DashIconify(icon="ph:list-magnifying-glass"),
                            style={"height": "26px"}
                        ),
                    ])
                ])
            ], justify="space-between", style={"height": "100%"})
        ],
        withBorder=True,
        shadow="sm",
        radius="lg",
        style={
            "padding": "10px",
            "height": "260px",
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
                                    dmc.Text(
                                        card_label,
                                        weight=700,
                                        size="xl",
                                        style={"padding-left": "6px"},
                                    ),
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
                                                        icon="twemoji:cupcake"
                                                        if by_id == "Odměny"
                                                        else "twemoji:1st-place-medal",
                                                        width=40,
                                                        height=40,
                                                        style={
                                                            "position": "absolute",
                                                            "transform": "translate(65px, -95px)"
                                                            if by_id == "Odměny"
                                                            else "translate(70px, -90px)",
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
                                        style={
                                            "padding-bottom": "2px",
                                            "opacity": "0"
                                            if int(top_table.iloc[2, 0]) == 0
                                            else None,
                                        },
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
                                                + str(int(top_table.iloc[1, 0])),
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
                                                + str(int(top_table.iloc[0, 0])),
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
                                                + str(int(top_table.iloc[2, 0])),
                                                color="dimmed",
                                                style={"padding-left": "16px"},
                                            )
                                        ],
                                        span="content",
                                        style={
                                            "padding-top": "4px",
                                            "opacity": "0"
                                            if int(top_table.iloc[2, 0]) == 0
                                            else None,
                                        },
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
    episode_timestamp = dmc.Menu(
        transition="pop",
        shadow="sm",
        radius="lg",
        withArrow="true",
        offset=-3,
        children=[
            dmc.MenuTarget(
                [
                    DashIconify(
                        icon="mdi:television-classic",
                        width=15,
                        height=15,
                    ),
                ]
            ),
            dmc.MenuDropdown(
                [
                    dmc.Grid(
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
                                    dmc.Text(
                                        "Epizóda " + str(data_string["EPISODE"]),
                                        size="sm",
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
                    )
                ]
            ),
        ],
        # style={
        #     "padding": "1px",
        #     "margin": "0px",
        # },
        # position="top",
        # transition="pop",
    )
    if data_string["EVENT_TYPE"] in ["Souboj o odměnu", "Souboj o imunitu", "Odměna"]:
        item = dmc.TimelineItem(
            children=[
                dmc.Card(
                    [
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [episode_timestamp],
                                    span="content",
                                    style={
                                        "padding-top": "6px",
                                        "padding-bottom": "4px",
                                        "padding-right": "0px",
                                    },
                                ),
                                dmc.Col(
                                    [
                                        dmc.Text(
                                            [
                                                "Den "
                                                + str(data_string["DAY"])
                                                + " - "
                                                + data_string["EVENT_TYPE"]
                                                + (
                                                    " ("
                                                    + str(data_string["EVENT_DESC"])
                                                    + ")"
                                                    if data_string["EVENT_TYPE"]
                                                    in ["Souboj o odměnu", "Odměna"]
                                                    else ""
                                                )
                                            ],
                                            weight=500,
                                            size="sm",
                                            style={"line-height": "1.25"},
                                        ),
                                    ],
                                    span="auto",
                                    style={
                                        "padding-top": "5px",
                                        "padding-bottom": "4px",
                                        "padding-left": "2px",
                                    },
                                ),
                            ],
                            align="center",
                        ),
                        dmc.Grid(
                            (
                                [
                                    dmc.Col(
                                        [
                                            DashIconify(
                                                icon="mdi:crown",
                                                width=18,
                                                height=18,
                                                style={
                                                    "color": survivor_colors[
                                                        data_string["WINNING_SIDE"]
                                                    ]
                                                    if data_string["WINNING_SIDE"]
                                                    in ["Hrdinové", "Rebelové"]
                                                    else None,
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
                                                        data_string["WINNING_SIDE"]
                                                    ]
                                                    if data_string["WINNING_SIDE"]
                                                    in ["Hrdinové", "Rebelové"]
                                                    else None
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
                                ]
                                if data_string["EVENT_TYPE"]
                                in ["Souboj o odměnu", "Souboj o imunitu"]
                                else []
                            )
                            + [
                                dmc.Col(
                                    [
                                        dmc.Text(
                                            "(" + data_string["SCORE"] + ")",
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
                                )
                                if data_string["WINNING_SIDE"]
                                in ["Hrdinové", "Rebelové"]
                                else None,
                                dmc.Col(
                                    [
                                        dmc.AvatarGroup(
                                            children=[
                                                dmc.Tooltip(
                                                    dmc.Avatar(
                                                        src=players[member][
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
                                                ].split(", ")
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
                        "overflow": "visible",
                    },
                )
            ],
            style={"margin-top": "8px", "padding-left": "16px"},
            bullet=DashIconify(icon="mdi:gift-outline", width=17, height=17)
            if data_string["EVENT_TYPE"] in ["Souboj o odměnu", "Odměna"]
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
                                                    [episode_timestamp],
                                                    span="content",
                                                    style={
                                                        "padding-top": "5px",
                                                        "padding-bottom": "4px",
                                                        "padding-right": "0px",
                                                    },
                                                ),
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
                                                        "padding-left": "2px",
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
                                                                ]
                                                                if data_string[
                                                                    "WINNING_SIDE"
                                                                ]
                                                                in [
                                                                    "Hrdinové",
                                                                    "Rebelové",
                                                                ]
                                                                else None,
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
                                                                if data_string[
                                                                    "WINNING_SIDE"
                                                                ]
                                                                in [
                                                                    "Hrdinové",
                                                                    "Rebelové",
                                                                ]
                                                                else None
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
                        "overflow": "visible",
                    },
                )
            ],
            style={"margin-top": "8px", "padding-left": "16px"},
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
                                                    [episode_timestamp],
                                                    span="content",
                                                    style={
                                                        "padding-top": "5px",
                                                        "padding-bottom": "4px",
                                                        "padding-right": "0px",
                                                    },
                                                ),
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
                                                        "padding-left": "2px",
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
                                                                ]
                                                                if data_string[
                                                                    "WINNING_SIDE"
                                                                ]
                                                                in [
                                                                    "Hrdinové",
                                                                    "Rebelové",
                                                                ]
                                                                else None,
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
                                                                if data_string[
                                                                    "WINNING_SIDE"
                                                                ]
                                                                in [
                                                                    "Hrdinové",
                                                                    "Rebelové",
                                                                ]
                                                                else None
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
                                                                ]
                                                                if data_string[
                                                                    "WINNING_SIDE"
                                                                ]
                                                                in [
                                                                    "Hrdinové",
                                                                    "Rebelové",
                                                                ]
                                                                else None
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
                                                                ]
                                                                if data_string[
                                                                    "WINNING_SIDE"
                                                                ]
                                                                in [
                                                                    "Hrdinové",
                                                                    "Rebelové",
                                                                ]
                                                                else None,
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
                        "overflow": "visible",
                    },
                )
            ],
            style={"margin-top": "8px", "padding-left": "16px"},
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
                                                    [episode_timestamp],
                                                    span="content",
                                                    style={
                                                        "padding-top": "5px",
                                                        "padding-bottom": "4px",
                                                        "padding-right": "0px",
                                                    },
                                                ),
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
                                                        "padding-left": "2px",
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
                                                                ]
                                                                if data_string[
                                                                    "WINNING_SIDE"
                                                                ]
                                                                in [
                                                                    "Hrdinové",
                                                                    "Rebelové",
                                                                ]
                                                                else None,
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
                                                                if data_string[
                                                                    "WINNING_SIDE"
                                                                ]
                                                                in [
                                                                    "Hrdinové",
                                                                    "Rebelové",
                                                                ]
                                                                else None
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
                        "overflow": "visible",
                    },
                )
            ],
            style={"margin-top": "8px", "padding-left": "16px"},
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
                                                    [episode_timestamp],
                                                    span="content",
                                                    style={
                                                        "padding-top": "5px",
                                                        "padding-bottom": "4px",
                                                        "padding-right": "0px",
                                                    },
                                                ),
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
                                                        "padding-left": "2px",
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
                                                                ]
                                                                if data_string[
                                                                    "WINNING_SIDE"
                                                                ]
                                                                == "Hrdinové"
                                                                else survivor_colors[
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
                        "overflow": "visible",
                    },
                )
            ],
            style={"margin-top": "8px", "padding-left": "16px"},
            bullet=DashIconify(
                icon="material-symbols:person-add-outline", width=18, height=18
            )
            if data_string["EVENT_TYPE"] == "Noví hráči"
            else DashIconify(icon="material-symbols:sync", width=20, height=20),
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
                                                    [episode_timestamp],
                                                    span="content",
                                                    style={
                                                        "padding-top": "5px",
                                                        "padding-bottom": "4px",
                                                        "padding-right": "0px",
                                                    },
                                                ),
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
                                                        "padding-left": "2px",
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
                        "overflow": "visible",
                    },
                )
            ],
            style={"margin-top": "8px", "padding-left": "16px"},
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
                                                    [episode_timestamp],
                                                    span="content",
                                                    style={
                                                        "padding-top": "5px",
                                                        "padding-bottom": "4px",
                                                        "padding-right": "0px",
                                                    },
                                                ),
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
                                                                + " ("
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
                                                        "padding-left": "2px",
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
                                                                ]
                                                                if data_string[
                                                                    "WINNING_SIDE"
                                                                ]
                                                                in [
                                                                    "Hrdinové",
                                                                    "Rebelové",
                                                                ]
                                                                else None,
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
                                                                if data_string[
                                                                    "WINNING_SIDE"
                                                                ]
                                                                in [
                                                                    "Hrdinové",
                                                                    "Rebelové",
                                                                ]
                                                                else None
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
                        "overflow": "visible",
                    },
                )
            ],
            style={"margin-top": "8px", "padding-left": "16px"},
            bullet=DashIconify(
                icon="material-symbols:token-outline", width=20, height=20
            ),
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
                                                    [episode_timestamp],
                                                    span="content",
                                                    style={
                                                        "padding-top": "5px",
                                                        "padding-bottom": "4px",
                                                        "padding-right": "0px",
                                                    },
                                                ),
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
                                                        "padding-left": "2px",
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
                        "overflow": "visible",
                    },
                )
            ],
            style={"margin-top": "8px", "padding-left": "16px"},
            bullet=DashIconify(
                icon="material-symbols:merge-rounded", width=20, height=20
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
        color = "white" if i > len(bounds) / 2.0 else "#444"

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


def kmenovka_hlasovani_item(episode, day, first=False):
    odhlasovan = event_log_df[
        (event_log_df["DAY"] == day)
        & (event_log_df["EPISODE"] == episode)
        & (event_log_df["EVENT_TYPE"] == "Kmenová rada")
    ]["WINNING_ROSTER"].values
    p_row = kmenovky_hlasovani_df[
        (kmenovky_hlasovani_df["EPISODE"] == episode)
        & (kmenovky_hlasovani_df["TYPE"] == "Primární")
    ]
    p_hlasy = {}
    for p in players:
        if str(p_row[p].values[0]) != "nan":
            for one_p in p_row[p].values[0].split(", "):
                if one_p in p_hlasy:
                    p_hlasy[one_p].append(p)
                else:
                    p_hlasy[one_p] = [p]
    s_row = kmenovky_hlasovani_df[
        (kmenovky_hlasovani_df["EPISODE"] == episode)
        & (kmenovky_hlasovani_df["TYPE"] == "Doplňkové")
    ]
    if not s_row.empty:
        s_hlasy = {}
        for p in players:
            if str(s_row[p].values[0]) != "nan":
                for one_p in s_row[p].values[0].split(", "):
                    if one_p in s_hlasy:
                        s_hlasy[one_p].append(p)
                    else:
                        s_hlasy[one_p] = [p]
        doplnkove_row = [
            dmc.Grid(
                [
                    # dmc.Col([dmc.Space(w=50)], span="content"),
                    dmc.Col(
                        [DashIconify(icon="material-symbols:subdirectory-arrow-right")],
                        span="content",
                        pr=0,
                    ),
                    dmc.Col(
                        [dmc.Text("Opakované hlasování", style={"width": "160px"})],
                        span="content",
                        px=0,
                    ),
                ]
                + [
                    dmc.Col(
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
                                                                dmc.Indicator(
                                                                    dmc.Avatar(
                                                                        src=players[
                                                                            hlas_pre
                                                                        ][
                                                                            "profile_picture"
                                                                        ],
                                                                        radius="sm",
                                                                        size="sm",
                                                                        style={
                                                                            "opacity": "0.5",
                                                                            "background-color": "grey",
                                                                        }
                                                                        if hlas_pre
                                                                        != odhlasovan
                                                                        else {},
                                                                    ),
                                                                    label=DashIconify(
                                                                        icon="twemoji:crossed-swords",
                                                                        style={
                                                                            "opacity": "0.5",
                                                                        }
                                                                        if hlas_pre
                                                                        != odhlasovan
                                                                        else {},
                                                                    ),
                                                                    color="rgba(0,0,0,0)",
                                                                    position="top-end",
                                                                    size=14,
                                                                ),
                                                                label=hlas_pre,
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
                                                    ),
                                                    dmc.Col(
                                                        [
                                                            dmc.Text(
                                                                hlas_pre
                                                                + ": "
                                                                + str(
                                                                    len(
                                                                        s_hlasy[
                                                                            hlas_pre
                                                                        ]
                                                                    )
                                                                ),
                                                                color="dimmed"
                                                                if hlas_pre
                                                                != odhlasovan
                                                                else None,
                                                            )
                                                        ],
                                                        span="content",
                                                    ),
                                                ],
                                                style={"width": "147px"},
                                                justify="flex-end",
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
                                                            avatar_group(
                                                                s_hlasy[hlas_pre],
                                                                {
                                                                    "opacity": "0.5",
                                                                    "background-color": "grey",
                                                                }
                                                                if hlas_pre
                                                                != odhlasovan
                                                                else {},
                                                            )
                                                        ],
                                                        span="content",
                                                    ),
                                                ],
                                                style={"width": "150px"},
                                                justify="flex-start",
                                            )
                                        ],
                                        span="content",
                                    ),
                                ]
                            )
                        ],
                        span="content",
                    )
                    for hlas_pre in sorted(
                        s_hlasy, key=lambda k: len(s_hlasy[k]), reverse=True
                    )
                ]
            )
        ]
    else:
        doplnkove_row = []
    out = dmc.Grid(
        [
            dmc.Col(
                [
                    dmc.Grid([dmc.Col([dmc.Divider()])]) if not first else None,
                    dmc.Grid(
                        [
                            dmc.Col(
                                [
                                    dmc.Text(
                                        "Den " + str(day) + ", Epizoda " + str(episode),
                                        style={"width": "168px"},
                                    )
                                ],
                                span="content",
                            )
                        ]
                        + [
                            dmc.Col(
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
                                                                        dmc.Indicator(
                                                                            dmc.Avatar(
                                                                                src=players[
                                                                                    hlas_pre
                                                                                ][
                                                                                    "profile_picture"
                                                                                ],
                                                                                radius="sm",
                                                                                size="sm",
                                                                                style={
                                                                                    "opacity": "0.5",
                                                                                    "background-color": "grey",
                                                                                }
                                                                                if hlas_pre
                                                                                != odhlasovan
                                                                                else {},
                                                                            ),
                                                                            label=DashIconify(
                                                                                icon="twemoji:crossed-swords",
                                                                                style={
                                                                                    "opacity": "0.5",
                                                                                }
                                                                                if hlas_pre
                                                                                != odhlasovan
                                                                                else {},
                                                                            ),
                                                                            color="rgba(0,0,0,0)",
                                                                            position="top-end",
                                                                            size=14,
                                                                        ),
                                                                        label=hlas_pre,
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
                                                            ),
                                                            dmc.Col(
                                                                [
                                                                    dmc.Text(
                                                                        hlas_pre
                                                                        + ": "
                                                                        + str(
                                                                            len(
                                                                                p_hlasy[
                                                                                    hlas_pre
                                                                                ]
                                                                            )
                                                                        ),
                                                                        color="dimmed"
                                                                        if hlas_pre
                                                                        != odhlasovan
                                                                        else None,
                                                                    )
                                                                ],
                                                                span="content",
                                                            ),
                                                        ],
                                                        style={"width": "147px"},
                                                        justify="flex-end",
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
                                                                    avatar_group(
                                                                        p_hlasy[
                                                                            hlas_pre
                                                                        ],
                                                                        {
                                                                            "opacity": "0.5",
                                                                            "background-color": "grey",
                                                                        }
                                                                        if hlas_pre
                                                                        != odhlasovan
                                                                        else {},
                                                                    )
                                                                ],
                                                                span="content",
                                                            ),
                                                        ],
                                                        style={"width": "150px"},
                                                        justify="flex-start",
                                                    )
                                                ],
                                                span="content",
                                            ),
                                        ]
                                    )
                                ],
                                span="content",
                            )
                            for hlas_pre in sorted(
                                p_hlasy, key=lambda k: len(p_hlasy[k]), reverse=True
                            )
                        ]
                    ),
                ]
                + doplnkove_row
            )
        ]
    )
    return out


def layout(utm_source=None, utm_medium=None, utm_campaign=None):
    return [
        dmc.Header(
            height=60,
            children=[
                dmc.Grid(
                    [
                        dmc.Col(
                            [
                                dmc.MediaQuery(
                                    dmc.Container(
                                        [
                                            dmc.Text(
                                                "SURVIVOR 2023", weight=500, size=20
                                            ),
                                        ],
                                        style={
                                            "padding": "0px",
                                            "padding-left": "10px",
                                        },
                                    ),
                                    largerThan="sm",
                                    styles={"display": "none"},
                                ),
                                dmc.MediaQuery(
                                    dmc.Container(
                                        [
                                            dmc.Text(
                                                "Survivor Česko & Slovensko 2023 - Statistiky",
                                                weight=500,
                                                size=20,
                                            ),
                                        ],
                                        style={
                                            "padding": "0px",
                                            "padding-left": "30px",
                                        },
                                    ),
                                    smallerThan="sm",
                                    styles={"display": "none"},
                                ),
                            ],
                            span="content",
                        ),
                        dmc.Col(
                            [
                                dmc.MediaQuery(
                                    dmc.Container(
                                        [
                                            dmc.Grid(
                                                [
                                                    dmc.Col(
                                                        [
                                                            dmc.ActionIcon(
                                                                DashIconify(
                                                                    icon="radix-icons:blending-mode",
                                                                    width=30,
                                                                ),
                                                                size="lg",
                                                                id="color-scheme-toggle",
                                                            ),
                                                        ],
                                                        span="content",
                                                        style={"padding": "0px"},
                                                    ),
                                                    dmc.Col(
                                                        [
                                                            html.A(
                                                                dmc.Tooltip(
                                                                    dmc.ActionIcon(
                                                                        DashIconify(
                                                                            icon="mdi:github",
                                                                            width=30,
                                                                        ),
                                                                        size="lg",
                                                                    ),
                                                                    label="Github",
                                                                    position="top",
                                                                    transition="pop",
                                                                ),
                                                                href="https://github.com/martin2097/",
                                                                target="_blank",
                                                            ),
                                                        ],
                                                        span="content",
                                                        style={"padding": "0px"},
                                                    ),
                                                    dmc.Col(
                                                        [
                                                            html.A(
                                                                dmc.Tooltip(
                                                                    dmc.ActionIcon(
                                                                        DashIconify(
                                                                            icon="mdi:linkedin",
                                                                            width=30,
                                                                        ),
                                                                        size="lg",
                                                                    ),
                                                                    label="Linkedin",
                                                                    position="top",
                                                                    transition="pop",
                                                                ),
                                                                href="https://linkedin.com/in/martin-rapavy",
                                                                target="_blank",
                                                            )
                                                        ],
                                                        span="content",
                                                        style={
                                                            "padding": "0px",
                                                            "padding-right": "10px",
                                                        },
                                                    ),
                                                ]
                                            )
                                        ],
                                        style={"padding": "0px"},
                                    ),
                                    largerThan="sm",
                                    styles={"padding-right": "20px"},
                                )
                            ],
                            span="content",
                        ),
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
                                            "Král duelů",
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
                                    [
                                        dmc.Text(
                                            "Statistiky hlasování:",
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
                                        best_players_card(
                                            "Nejvíc obdržených hlasů",
                                            "material-symbols:how-to-vote",
                                            kmenovky_hlasovani_df[
                                                kmenovky_hlasovani_df["TYPE"]
                                                == "Primární"
                                            ]
                                            .iloc[:, 3:]
                                            .stack()
                                            .reset_index()[0]
                                            .str.split(pat=", ")
                                            .explode()
                                            .value_counts()
                                            .rename_axis("unique_values")
                                            .reset_index(name="Počet hlasů")
                                            .set_index("unique_values")
                                            .iloc[0:5],
                                            ["", "Počet hlasů"],
                                            "Hlasů",
                                        ),
                                    ],
                                    xl=4,
                                    sm=6,
                                ),
                                dmc.Col(
                                    [
                                        best_players_card(
                                            "Nejmíň obdržených hlasů",
                                            "game-icons:avoidance",
                                            kmenovky_hlasovani_df[
                                                kmenovky_hlasovani_df["TYPE"]
                                                == "Primární"
                                            ]
                                            .iloc[:, 3:]
                                            .stack()
                                            .reset_index()[0]
                                            .str.split(pat=", ")
                                            .explode()
                                            .value_counts(ascending=True)
                                            .rename_axis("unique_values")
                                            .reset_index(name="Počet hlasů")
                                            .set_index("unique_values")
                                            .iloc[0:5],
                                            ["", "Počet hlasů"],
                                            "Hlasů",
                                        ),
                                    ],
                                    xl=4,
                                    sm=6,
                                ),
                                dmc.Col(
                                    [
                                        best_players_card(
                                            "Nejvíc úspěšných odhlasování",
                                            "mdi:bookmark-success-outline",
                                            df_uspesne_hlasovani.sort_values(
                                                by="Vyhlasování", ascending=False
                                            ).iloc[0:5][["Vyhlasování"]],
                                            ["", "Vyhlasování"],
                                            "Počet",
                                        ),
                                    ],
                                    xl=4,
                                    sm=6,
                                ),
                            ]
                        ),
                        dmc.Grid([
                           dmc.Col([
                               dmc.Center([
                                   html.A(
                                       dmc.Group([
                                           DashIconify(
                                               icon="material-symbols:keyboard-double-arrow-down",
                                               style={
                                                   "color": "#868e96",
                                               },
                                               width=20,
                                               height=20,
                                           ),
                                           dmc.Text("Přehled všech hlasování", color="dimmed", size="md",
                                                    variant="text"),
                                       ], spacing=0),
                                       style={"textTransform": "capitalize", "textDecoration": "none"},
                                       href="#kmenovky-hlasovani",
                                   ),
                               ])
                           ], p=2, pt=4)
                        ]),
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        dmc.Text(
                                            "Skryté imunity a výhody:",
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
                                        best_players_card(
                                            "Nejvíc zahraných imunit",
                                            "material-symbols:token-outline",
                                            pd.DataFrame.from_dict(
                                                players, orient="index"
                                            )
                                            .sort_values(
                                                ["Skryté Imunity"],
                                                ascending=False,
                                            )
                                            .iloc[0:5][["Skryté Imunity"]],
                                            ["", "Skryté Imunity"],
                                            "Imunity",
                                        ),
                                    ],
                                    xl=4,
                                    sm=6,
                                ),
                                dmc.Col(
                                    [
                                        best_players_card(
                                            "Nejvíc zahraných výhod",
                                            "material-symbols:trending-up",
                                            pd.DataFrame.from_dict(
                                                players, orient="index"
                                            )
                                            .sort_values(
                                                ["Výhody"],
                                                ascending=False,
                                            )
                                            .iloc[0:5][["Výhody"]],
                                            ["", "Výhody"],
                                            "Výhody",
                                        ),
                                    ],
                                    xl=4,
                                    sm=6,
                                ),
                                dmc.Col(
                                    [
                                        best_players_card(
                                            "Nejvíc nezapočítaných hlasů",
                                            "mdi:trash-can-outline",
                                            df_nezapocitane_hlasy
                                            .sort_values(
                                                ["cnt"],
                                                ascending=False,
                                            )
                                            .iloc[0:5][["cnt"]],
                                            ["", "Nezapočítané hlasy"],
                                            "Hlasy",
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
                                            style={"height": "286px", "padding": "8px"},
                                            type="always",
                                        ),
                                    ],
                                    style={"padding": "0px"},
                                )
                            ]
                        ),
                        dmc.Drawer(
                            id="player-detail-drawer",
                            padding="md",
                            size="xl",
                            position="right",
                            zIndex=10000,
                        ),
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        dmc.Grid(
                                            [
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            "Počet diváků:",
                                                            size="xl",
                                                            weight=600,
                                                        )
                                                    ],
                                                    span="content"
                                                ),
                                                dmc.Col(
                                                    [
                                                        information_bubble(
                                                            [
                                                                dmc.Text("Skupina 15+"),
                                                                dmc.Space(
                                                                    h=20
                                                                ),
                                                                dmc.Text("Zdroj dat: ATO - Nielsen")
                                                             ], 500)
                                                    ],
                                                    span="content",
                                                    pl=0,
                                                    pt=12,
                                                )
                                            ]
                                        ),
                                        dmc.Grid(
                                            [
                                                dmc.Col(
                                                    [
                                                        dmc.Card(
                                                            [
                                                                dcc.Graph(
                                                                    id="sledovanost",
                                                                    # style={"height": "90vh"},
                                                                    # config={
                                                                    #     "staticPlot": True
                                                                    # },
                                                                    config={
                                                                        "displayModeBar": False,
                                                                        "scrollZoom": False,
                                                                        "doubleClick": False,
                                                                        "showAxisDragHandles": False,
                                                                    },
                                                                )
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
                                    ],
                                    xl=6,
                                ),
                                dmc.Col(
                                    [
                                        dmc.Grid(
                                            [
                                                dmc.Col(
                                                    [
                                                        dmc.Text(
                                                            "Podíl na trhu:",
                                                            size="xl",
                                                            weight=600,
                                                        )
                                                    ],
                                                    span="content",
                                                ),
                                                dmc.Col(
                                                    [
                                                        information_bubble(
                                                            [
                                                                dmc.Text("Skupina 15+"),
                                                                dmc.Space(
                                                                    h=20
                                                                ),
                                                                dmc.Text("Zdroj dat: ATO - Nielsen")
                                                             ], 500)
                                                    ],
                                                    span="content",
                                                    pl=0,
                                                    pt=12,
                                                )
                                            ]
                                        ),
                                        dmc.Grid(
                                            [
                                                dmc.Col(
                                                    [
                                                        dmc.Card(
                                                            [
                                                                dcc.Graph(
                                                                    id="sledovanost-share",
                                                                    # style={"height": "90vh"},
                                                                    # config={
                                                                    #     "staticPlot": True
                                                                    # },
                                                                    config={
                                                                        "displayModeBar": False,
                                                                        "scrollZoom": False,
                                                                        "doubleClick": False,
                                                                        "showAxisDragHandles": False,
                                                                    },
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
                                    ],
                                    xl=6,
                                ),
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
                                                        dmc.Text(
                                                            "Vývoj Power Indexu:",
                                                            size="xl",
                                                            weight=600,
                                                        ),
                                                    ],
                                                    span="content",
                                                ),
                                                dmc.Col(
                                                    [
                                                        dmc.Menu(
                                                            transition="pop",
                                                            shadow="sm",
                                                            radius="lg",
                                                            position="bottom-start",
                                                            # withArrow=True,
                                                            offset=0,
                                                            # arrowSize=10,
                                                            children=[
                                                                dmc.MenuTarget(
                                                                    DashIconify(
                                                                        icon="material-symbols:info-outline",
                                                                        width=25,
                                                                    )
                                                                ),
                                                                dmc.MenuDropdown(
                                                                    dmc.MediaQuery(
                                                                        dmc.Container(
                                                                            [
                                                                                dmc.Text(
                                                                                    "Power Index reprezentuje invertované priemerné relatívne umiestnenie jednotlivých hráčov. To znamená, že hráč, ktorý vyhrá všetky súťaže bude mať Power Index = 1"
                                                                                ),
                                                                                dmc.Space(
                                                                                    h=20
                                                                                ),
                                                                                dmc.Text(
                                                                                    "Aktivní hráči - iba hráči, ktorí sú stále v hre"
                                                                                ),
                                                                                dmc.Text(
                                                                                    "Aktualní forma - zohľadňuje iba výsledky z posledných 5 súťaží"
                                                                                ),
                                                                                dmc.Space(
                                                                                    h=20
                                                                                ),
                                                                                dmc.Text(
                                                                                    color="dimmed",
                                                                                    children="Príklad: Hráč sa zúčastní 3 súťaží, v každej z nich bude 11 súťažiacich. Hráč sa umiestni na 1., 3. a 8. mieste. Za prvú súťaž do výpočtu vstúpi hodnota 1, za druhú 0.8 a za tretiu 0.3. Výslednou hodnotou Power Indexu bude priemer týchto 3 hodnôt teda 0.7.",
                                                                                ),
                                                                                dmc.Text(
                                                                                    color="dimmed",
                                                                                    children="Jednotlivé hodnoty vznikajú vzorcom: 1 - ((umiestnenie - 1) / (počet účastníkov - 1)).",
                                                                                ),
                                                                            ],
                                                                            p=10,
                                                                            style={
                                                                                "max-width": "97vw"
                                                                            },
                                                                        ),
                                                                        largerThan="sm",
                                                                        styles={
                                                                            "max-width": "800px"
                                                                        },
                                                                    )
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                    span="content",
                                                    pl=0,
                                                    pt=12,
                                                ),
                                            ]
                                        )
                                    ],
                                    span="content",
                                    p=8,
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
                                                                dmc.ScrollArea(
                                                                    [
                                                                        dmc.Grid(
                                                                            [
                                                                                dmc.Col(
                                                                                    [
                                                                                        dcc.Graph(
                                                                                            id="power_index_history_heatmap",
                                                                                            config={
                                                                                                "staticPlot": True
                                                                                            },
                                                                                            responsive=True,
                                                                                            style={"height": "650px", "min-width": "820px"}
                                                                                        ),
                                                                                    ],
                                                                                    style={
                                                                                        "padding": "0px",
                                                                                    },
                                                                                )
                                                                            ],
                                                                            justify="center",
                                                                            style={
                                                                                "margin": "0px"
                                                                            },
                                                                        )
                                                                    ],
                                                                )
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
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        dmc.Text(
                                            "Výsledky hlasování na kmenových radách:",
                                            size="xl",
                                            weight=600,
                                            id="kmenovky-hlasovani"
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
                                                kmenovka_hlasovani_item(
                                                    episode,
                                                    day,
                                                    True if i == 0 else False,
                                                )
                                                for episode, day, i in zip(
                                                    kmenovky_hlasovani_df[
                                                        kmenovky_hlasovani_df["TYPE"]
                                                        == "Primární"
                                                    ]["EPISODE"].values,
                                                    kmenovky_hlasovani_df[
                                                        kmenovky_hlasovani_df["TYPE"]
                                                        == "Primární"
                                                    ]["DAY"].values,
                                                    range(
                                                        len(
                                                            kmenovky_hlasovani_df[
                                                                kmenovky_hlasovani_df[
                                                                    "TYPE"
                                                                ]
                                                                == "Primární"
                                                            ]["DAY"].values
                                                        )
                                                    ),
                                                )
                                            ],
                                            withBorder=True,
                                            shadow="sm",
                                            radius="lg",
                                            style={
                                                "padding": "10px",
                                            },
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
                            [
                                dmc.Col(
                                    [dmc.Text("Časová osa:", size="xl", weight=600)],
                                    span="content",
                                ),
                                dmc.Col(
                                    [
                                        dmc.Menu(
                                            transition="pop",
                                            shadow="md",
                                            radius="lg",
                                            position="bottom-end",
                                            # withArrow=True,
                                            offset=0,
                                            # arrowSize=10,
                                            children=[
                                                dmc.MenuTarget(
                                                    dmc.ActionIcon(
                                                        DashIconify(
                                                            icon="material-symbols:filter-alt-outline",
                                                            width=30,
                                                        ),
                                                        size="lg",
                                                    )
                                                ),
                                                dmc.MenuDropdown(
                                                    dmc.MediaQuery(
                                                        dmc.Container(
                                                            [
                                                                dmc.Grid(
                                                                    [
                                                                        dmc.Col(
                                                                            [
                                                                                dmc.Text(
                                                                                    "Typ události",
                                                                                    weight=600,
                                                                                ),
                                                                            ],
                                                                            span="content",
                                                                        ),
                                                                        dmc.Col(
                                                                            [
                                                                                dmc.ActionIcon(
                                                                                    DashIconify(
                                                                                        icon="bi:check-all",
                                                                                        width=25,
                                                                                    ),
                                                                                    id="filter-event-all",
                                                                                    n_clicks=0,
                                                                                )
                                                                            ],
                                                                            span="content",
                                                                            pt=6,
                                                                            pl=0,
                                                                        ),
                                                                    ],
                                                                    # justify="space-between",
                                                                ),
                                                                dmc.Grid(
                                                                    [
                                                                        dmc.Col(
                                                                            [
                                                                                dmc.ChipGroup(
                                                                                    [
                                                                                        dmc.Chip(
                                                                                            x,
                                                                                            value=x,
                                                                                            variant="outline",
                                                                                            color="yellow",
                                                                                        )
                                                                                        for x in event_log_df[
                                                                                            "EVENT_TYPE"
                                                                                        ].unique()
                                                                                    ],
                                                                                    id="filter-event",
                                                                                    value=event_log_df[
                                                                                        "EVENT_TYPE"
                                                                                    ].unique(),
                                                                                    multiple=True,
                                                                                    spacing=5,
                                                                                ),
                                                                            ]
                                                                        )
                                                                    ]
                                                                ),
                                                                dmc.Grid(
                                                                    [
                                                                        dmc.Col(
                                                                            [
                                                                                dmc.Button(
                                                                                    "Filtrovat",
                                                                                    id="event-log-filter-button",
                                                                                    variant="filled",
                                                                                    size="sm",
                                                                                    radius="xl",
                                                                                    color="yellow",
                                                                                    fullWidth=True,
                                                                                    leftIcon=DashIconify(
                                                                                        icon="material-symbols:filter-alt-outline",
                                                                                        width=25,
                                                                                        height=25,
                                                                                    ),
                                                                                ),
                                                                            ]
                                                                        )
                                                                    ]
                                                                ),
                                                            ],
                                                            p=10,
                                                            style={"max-width": "70vw"},
                                                        ),
                                                        largerThan="sm",
                                                        styles={"max-width": "300px"},
                                                    )
                                                ),
                                            ],
                                        ),
                                    ],
                                    span="content",
                                    # pr=20,
                                ),
                            ],
                            justify="space-between",
                        ),
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        dmc.Card(
                                            children=[
                                                dmc.Grid(
                                                    [
                                                        dmc.Col(
                                                            [
                                                                create_event_log(
                                                                    event_log_df.tail(
                                                                        61
                                                                    )
                                                                )
                                                            ],
                                                            id="event-log-output",
                                                        )
                                                    ]
                                                ),
                                                dmc.Grid(
                                                    [
                                                        dmc.Col(
                                                            [
                                                                dmc.Button(
                                                                    "Ukázat vše",
                                                                    id="event-log-more-button",
                                                                    variant="light",
                                                                    size="md",
                                                                    radius="xl",
                                                                    color="gray",
                                                                    fullWidth=True,
                                                                    leftIcon=DashIconify(
                                                                        icon="material-symbols:expand-more-rounded",
                                                                        width=25,
                                                                        height=25,
                                                                    ),
                                                                ),
                                                            ],
                                                            span="auto",
                                                            style={
                                                                "padding-top": "16px"
                                                            },
                                                        )
                                                    ],
                                                    justify="center",
                                                ),
                                            ],
                                            withBorder=True,
                                            shadow="sm",
                                            radius="lg",
                                            p=10,
                                        ),
                                    ]
                                )
                            ]
                        ),
                    ],
                    xl=3,
                    lg=4,
                ),
            ],
            gutterLg=40,
            style={"margin": "0px"},
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
        one_col = (
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
        if current_form:
            for jm in den_vypadnutia:
                if den_vypadnutia[jm] < int(i[4:]):
                    one_col[jm] = np.NaN
        personal_stats_df_pi_history[i] = one_col
    if active_player:
        dff = pd.DataFrame.from_dict(players, orient="index")
        active_players = list(dff[dff["Poradie"].isna()].index)
    else:
        dff = pd.DataFrame.from_dict(players, orient="index")
        active_players = list(dff.index)
    fig_hm = imshow(
        personal_stats_df_pi_history.round(2)
        .filter(items=active_players, axis=0)
        .T[poradie_vypadnutych if not active_player else active_players],
        text_auto=True,  # ".2f",
        range_color=[0, 1],
        color_continuous_scale="RdYlGn",
    )
    fig_hm.update_layout(
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(
            family="Segoe UI",
            size=14,
        ),
        margin=dict(r=0, b=10, t=10, l=0),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        modebar=dict(
            bgcolor="rgba(0, 0, 0, 0)",
            color="rgba(0, 0, 0, 0.3)",
            activecolor="rgba(0, 0, 0, 0.3)",
        ),
        yaxis_title=None,
        xaxis=dict(
            showgrid=False,
            color="#444" if theme["colorScheme"] == "light" else "#FFFFFF",
        ),
        yaxis=dict(
            showgrid=False,
            color="#444" if theme["colorScheme"] == "light" else "#FFFFFF",
        ),
    )
    fig_hm.update_coloraxes(showscale=False)
    return fig_hm


@callback(
    Output("event-log-output", "children"),
    Output("event-log-more-button", "children"),
    Output("event-log-more-button", "leftIcon"),
    Input("event-log-more-button", "n_clicks"),
    Input("event-log-filter-button", "n_clicks"),
    State("filter-event", "value"),
    prevent_initial_call=True,
)
def update_eventlog(more_n_clicks, filter_n_clicks, filtered_events):
    data = event_log_df.copy()
    data = data[data["EVENT_TYPE"].isin(filtered_events)]
    if more_n_clicks is None:
        more_n_clicks = 0
    if more_n_clicks % 2 == 0:
        data = data.tail(61)
        text = "Ukázat vše"
        icon = (
            DashIconify(
                icon="material-symbols:expand-more-rounded", width=25, height=25
            ),
        )
    else:
        text = "Skrýt"
        icon = (
            DashIconify(
                icon="material-symbols:expand-less-rounded", width=25, height=25
            ),
        )
    eventlog = create_event_log(data)
    return eventlog, text, icon


@callback(
    Output("filter-event", "value"),
    Input("filter-event-all", "n_clicks"),
    State("filter-event", "value"),
)
def filter_all_events(n_clicks, current_values):
    if n_clicks == 0:
        raise PreventUpdate
    else:
        if len(current_values) == 0:
            out = event_log_df["EVENT_TYPE"].unique()
        else:
            out = []
        return out


# @callback(
#     Output("event-log-filter-button", "variant"),
#     Input("event-log-filter-button", "n_clicks"),
#     Input("filter-event", "value"),
# )
# def highlight_filter_button(n_clicks_fire_filters, filter_value_change):
#     if ctx.triggered_id is None:
#         raise PreventUpdate
#     if ctx.triggered_id == "event-log-filter-button":
#         return "outline"
#     else:
#         return "filled"


@callback(
    Output("sledovanost", "figure"),
    Output("sledovanost-share", "figure"),
    Input("theme-store", "modified_timestamp"),
    State("theme-store", "data"),
)
def update_line_chart(n_clicks, theme):
    fig_share = line(x=sledovanost_df["EPISODE"], y=sledovanost_df["SHARE"])

    fig_sledovanost = bar(x=sledovanost_df["EPISODE"], y=sledovanost_df["VIEWERS"])

    fig_sledovanost.update_traces(
        marker_color="rgb(207,219,137)",
        hovertemplate="%{x:,.0f}. díl<br>%{y:,.0f} diváků",
    )

    fig_share.update_traces(
        line_color="rgb(3,195,168)",
        hovertemplate="%{x:,.0f}. díl<br>%{y:.2%} podíl",
    )

    fig_sledovanost.add_annotation(
        x=14,
        y=320000,
        xref="x",
        yref="y",
        text="Gender Pravidlo <br> Odstoupení Jirky",
        showarrow=True,
        font=dict(
            family="Segoe UI",
            size=14,
            color="#444" if theme["colorScheme"] == "light" else "#FFFFFF",
        ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#444" if theme["colorScheme"] == "light" else "#FFFFFF",
        ax=30,
        ay=-40,
    )

    fig_share.add_annotation(
        x=14,
        y=0.1536,
        xref="x",
        yref="y",
        text="Gender Pravidlo <br> Odstoupení Jirky",
        showarrow=True,
        font=dict(
            family="Segoe UI",
            size=14,
            color="#444" if theme["colorScheme"] == "light" else "#FFFFFF",
        ),
        align="center",
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#444" if theme["colorScheme"] == "light" else "#FFFFFF",
        ax=30,
        ay=-40,
    )

    fig_share.update_layout(
        height=300,
        # width=1200,
        yaxis_title=None,
        xaxis_title=None,
        dragmode=False,
        yaxis=dict(
            # showgrid=False,
            tickmode="array",
            tickvals=[0.05, 0.1, 0.15],
            gridcolor="whitesmoke" if theme["colorScheme"] == "light" else "#484848",
            gridwidth=0.5,
            zeroline=False,
            color="#444" if theme["colorScheme"] == "light" else "#FFFFFF",
            tickformat=".2%",
            nticks=5,
            range=[0, 0.2],
        ),
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(
            family="Segoe UI",
            size=14,
        ),
        margin=dict(r=0, b=0, t=10, l=0),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        xaxis=dict(
            tickmode="array",
            tickvals=[1, 6, 11, 16, 21, 26, 31, 36, 41],
            ticktext=[
                "1. Díl",
                "6. Díl",
                "11. Díl",
                "16. Díl",
                "21. Díl",
                "26. Díl",
                "31. Díl",
                "36. Díl",
                "41. Díl",
            ],
            showgrid=False,
            zeroline=False,
            color="#444" if theme["colorScheme"] == "light" else "#FFFFFF",
        ),
    )

    fig_sledovanost.update_layout(
        height=300,
        # width=1200,
        yaxis_title=None,
        xaxis_title=None,
        dragmode=False,
        bargap=0.4,
        yaxis=dict(
            # showgrid=False,
            tickmode="array",
            tickvals=[100000, 200000, 300000],
            ticktext=["100 tis.", "200 tis.", "300 tis.", "400 tis."],
            gridcolor="whitesmoke" if theme["colorScheme"] == "light" else "#484848",
            gridwidth=0.2,
            zeroline=False,
            color="#444" if theme["colorScheme"] == "light" else "#FFFFFF",
            nticks=5,
        ),
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(
            family="Segoe UI",
            size=14,
        ),
        margin=dict(r=0, b=10, t=0, l=0),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        xaxis=dict(
            tickmode="array",
            tickvals=[1, 6, 11, 16, 21, 26, 31, 36, 41],
            ticktext=[
                "1. Díl",
                "6. Díl",
                "11. Díl",
                "16. Díl",
                "21. Díl",
                "26. Díl",
                "31. Díl",
                "36. Díl",
                "41. Díl",
            ],
            showgrid=False,
            zeroline=False,
            color="#444" if theme["colorScheme"] == "light" else "#FFFFFF",
        ),
    )
    return fig_sledovanost, fig_share


@callback(
    Output("player-detail-drawer", "opened"),
    Output("player-detail-drawer", "children"),
    Input({"type": "show-player-detail", "subtype": ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def player_detail_drawer_update(n_clicks_opened):
    player = ctx.triggered_id["subtype"]
    hlasy_na_kmenovkach = []
    for den, epizoda, typ, hlas_pro in zip(
        kmenovky_hlasovani_df["DAY"],
        kmenovky_hlasovani_df["EPISODE"],
        kmenovky_hlasovani_df["TYPE"],
        kmenovky_hlasovani_df[player],
    ):
        if str(hlas_pro) != "nan":
            hlasy_na_kmenovkach += [
                dmc.Group(
                    [
                        dmc.Text(
                            "Den "
                            + str(den)
                            + ", Epizoda "
                            + str(epizoda)
                            + (", Opakované" if typ == "Doplňkové" else "")
                        ),
                        dmc.Text(hlas_pro),
                    ],
                    position="apart",
                )
            ]
    out_cont = (
        dmc.ScrollArea(
            [
                dmc.Grid(
                    [
                        dmc.Col(
                            [
                                dmc.Grid(
                                    [
                                        dmc.Col(
                                            [
                                                dmc.Center(
                                                    [
                                                        dmc.Avatar(
                                                            src=players[player][
                                                                "profile_picture"
                                                            ],
                                                            radius="lg",
                                                            size=150,
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
                                                dmc.Center(
                                                    [
                                                        dmc.Text(
                                                            players[player]["Jméno"],
                                                            size="lg",
                                                            weight=600,
                                                        )
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
                                                dmc.Center(
                                                    [
                                                        dmc.Badge(
                                                            (
                                                                "TOP "
                                                                + str(
                                                                    players[player][
                                                                        "Poradie"
                                                                    ]
                                                                )
                                                            )
                                                            if players[player][
                                                                "Poradie"
                                                            ]
                                                            is not None
                                                            else "Ve hře",
                                                            variant="dot"
                                                            if players[player][
                                                                "Poradie"
                                                            ]
                                                            is None
                                                            else "outline",
                                                            color="green"
                                                            if players[player][
                                                                "Poradie"
                                                            ]
                                                            is None
                                                            else "blue",
                                                            size="xl",
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
                                                dmc.Stack(
                                                    [
                                                        dmc.Group(
                                                            [
                                                                dmc.Text("Věk"),
                                                                dmc.Text(
                                                                    players[player][
                                                                        "Věk"
                                                                    ]
                                                                ),
                                                            ],
                                                            position="apart",
                                                        ),
                                                        dmc.Group(
                                                            [
                                                                dmc.Text("Povolání"),
                                                                dmc.Text(
                                                                    players[player][
                                                                        "Povolání"
                                                                    ]
                                                                ),
                                                            ],
                                                            position="apart",
                                                        ),
                                                        dmc.Space(h=20),
                                                        dmc.Text(
                                                            "Herní statistiky",
                                                            weight=600,
                                                            align="center",
                                                        ),
                                                        dmc.Group(
                                                            [
                                                                dmc.Text(
                                                                    "Dní na ostrově"
                                                                ),
                                                                dmc.Text(
                                                                    str(
                                                                        players[player][
                                                                            "Den vypadnutia"
                                                                        ]
                                                                    )
                                                                    if players[player][
                                                                        "Den vypadnutia"
                                                                    ]
                                                                    is not None
                                                                    else "Ve hře"
                                                                ),
                                                            ],
                                                            position="apart",
                                                        ),
                                                        dmc.Group(
                                                            [
                                                                dmc.Text(
                                                                    "Individuálne imunity"
                                                                ),
                                                                dmc.Text(
                                                                    str(
                                                                        players[player][
                                                                            "Imunity"
                                                                        ]
                                                                    )
                                                                ),
                                                            ],
                                                            position="apart",
                                                        ),
                                                        dmc.Group(
                                                            [
                                                                dmc.Text(
                                                                    "Vyhrané duely"
                                                                ),
                                                                dmc.Text(
                                                                    str(
                                                                        players[player][
                                                                            "Duely"
                                                                        ]
                                                                    )
                                                                ),
                                                            ],
                                                            position="apart",
                                                        ),
                                                        dmc.Group(
                                                            [
                                                                dmc.Text(
                                                                    "Účasti na odměnách"
                                                                ),
                                                                dmc.Text(
                                                                    str(
                                                                        players[player][
                                                                            "Odměny"
                                                                        ]
                                                                    )
                                                                ),
                                                            ],
                                                            position="apart",
                                                        ),
                                                        dmc.Group(
                                                            [
                                                                dmc.Text(
                                                                    "Zahrané skryté imunity"
                                                                ),
                                                                dmc.Text(
                                                                    str(
                                                                        players[player][
                                                                            "Skryté Imunity"
                                                                        ]
                                                                    )
                                                                ),
                                                            ],
                                                            position="apart",
                                                        ),
                                                        dmc.Group(
                                                            [
                                                                dmc.Text(
                                                                    "Zahrané výhody"
                                                                ),
                                                                dmc.Text(
                                                                    str(
                                                                        players[player][
                                                                            "Výhody"
                                                                        ]
                                                                    )
                                                                ),
                                                            ],
                                                            position="apart",
                                                        ),
                                                        dmc.Space(h=20),
                                                        dmc.Text(
                                                            "Hlasováni na kmenových radách",
                                                            weight=600,
                                                            align="center",
                                                        ),
                                                    ]
                                                    + hlasy_na_kmenovkach + [
                                                        dmc.Space(h=100),
                                                    ],
                                                    spacing="xs",
                                                )
                                            ],
                                            span="auto",
                                        ),
                                    ],
                                ),
                            ],
                            px=30,
                            pb=30,
                            pt=10,
                        )
                    ]
                )
            ],
            style={"height": "90vh"},
            offsetScrollbars=True,
            type="scroll",
        ),
    )
    return True, out_cont




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
