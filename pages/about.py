import dash
import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify
from lib.utils import visit_link_icon, mid_col_responsive
from lib.page_templates import page_template

text_strings = {
    "en": [
        "Who am I?",
        "My name is Martin, and I enjoy making other people's lives easier. It may be data insight presented in a "
        "user-friendly way, or it could be teaching them how to do it themselves. ",
        "Python has been my primary tool for this for the last few years. It all started with Dash, and it's still my "
        "favorite to this day. It allows me to deliver the most insight from data in a way that is accessible even to "
        "non-technical users.",
        "I also want to give something back because I have learnt so much from others. I am involved in the "
        "Dash community and also organize educational events for my coworkers.",
        "My Talents",
        "Technical Skills:",
        "Soft Skills:",
        "Strong Problem Solving",
        "Managing Changes",
        "Influencing Others",
        "Empathetic",
        "Eager Learner",
    ],
    "sk": [
        "Kto som?",
        "Volám sa Martin a baví ma ostatným uľahčovať život. Či už sa jedná o prehľady dát prezentované používateľsky "
        "prívetivým spôsobom alebo učenie iných, ako si to pripraviť sami. ",
        "V posledných rokoch bol mojím hlavným nástrojom Python. Všetko to začalo Dashom, ktorý dodnes ostáva tým "
        "najobľúbenejším. Umožňuje mi poskytnúť čo najviac informácií z dát spôsobom, ktorý je prístupný aj "
        "netechnickým používateľom.",
        "Pretože som sa toho veľa naučil od ostatných, snažím sa svoje vedomosti predávať ďalej. Som súčasťou "
        "Dash komunity a organizujem vzdelávacie aktivity pre svojich kolegov.",
        "Moje schopnosti",
        "Technické:",
        "Mäkké:",
        "Dôsledné riešenie problémov",
        "Riadenie zmien",
        "Pozitívny vplyv na druhých",
        "Empatia",
        "Záujem o učenie sa nových vecí",
    ],
}


def layout(language):
    return page_template(
        mid_col_responsive(
            dmc.Stack(
                [
                    dmc.Divider(
                        label=text_strings[language][0],
                        size="sm",
                        styles={"label": {"font-size": "25px", "font-weight": 600}},
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
                                                            src="/assets/profile_pic.jpg",
                                                            style={
                                                                "background": "linear-gradient(45deg, rgb(25, 113, 194) 0%, rgb(9, 146, 104) 100%)"
                                                            },
                                                            styles={
                                                                "image": {
                                                                    "opacity": 0.5
                                                                }
                                                            },
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
                                boxWrapperProps={"style": {"width": "100%"}},
                            ),
                            dmc.Col(
                                [
                                    dmc.Text(text_strings[language][1]),
                                    dmc.Space(h=25),
                                    dmc.Text(text_strings[language][2]),
                                    dmc.Space(h=25),
                                    dmc.Text(text_strings[language][3]),
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
                                                            src="/assets/profile_pic.jpg",
                                                            style={
                                                                "background": "linear-gradient(45deg, rgb(25, 113, 194) 0%, rgb(9, 146, 104) 100%)"
                                                            },
                                                            styles={
                                                                "image": {
                                                                    "opacity": 0.5
                                                                }
                                                            },
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
                                boxWrapperProps={"style": {"width": "275px"}},
                            ),
                        ],
                        m=0,
                    ),
                    dmc.Divider(
                        label=text_strings[language][4],
                        size="sm",
                        styles={"label": {"font-size": "25px", "font-weight": 600}},
                        my=10,
                    ),
                    dmc.Grid(
                        [
                            dmc.Col(
                                [
                                    dmc.Text(text_strings[language][5], mb=5),
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
                                                    icon="akar-icons:python-fill",
                                                    width=24,
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
                                                    icon="akar-icons:python-fill",
                                                    width=24,
                                                ),
                                            ),
                                            dmc.ListItem(
                                                "SQL",
                                                icon=DashIconify(
                                                    icon="material-symbols:database",
                                                    width=24,
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
                                    dmc.Text(text_strings[language][6], mb=5),
                                    dmc.List(
                                        [
                                            dmc.ListItem(text_strings[language][7]),
                                            dmc.ListItem(text_strings[language][8]),
                                            dmc.ListItem(text_strings[language][9]),
                                            dmc.ListItem(text_strings[language][10]),
                                            dmc.ListItem(text_strings[language][11]),
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
                mb=100,
            )
        ),
        language,
    )


dash.register_page(
    module="about-en",
    path="/en/about",
    redirect_from=["/about"],
    title="Martin Rapavý - About Me",
    description="I am passionate about data, Python and especially Dash. I also enjoy making other people's lives "
    "easier. It may be data insight presented in a user-friendly way, or it could be teaching them how to do it "
    "themselves.",
    image="personal-page-view.png",
    layout=layout("en"),
)

dash.register_page(
    module="about-sk",
    path="/sk/about",
    title="Martin Rapavý - O mne",
    description="Zaujímam sa o dáta, Python a obzvlášť o Dash. Okrem toho rád ostatným uľahčujem život. Či už sa jedná "
    "o prehľady dát prezentované používateľsky prívetivým spôsobom alebo učenie iných, ako si to pripraviť "
    "sami.",
    image="personal-page-view.png",
    layout=layout("sk"),
)
