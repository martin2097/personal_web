import dash
import dash_mantine_components as dmc
from lib.utils import gradient_text, mid_col_responsive
from lib.page_templates import page_template

text_strings = {
    "en": [
        "Ahoj! My name is",
        "Martin Rapavý.",
        "I am passionate about ",
        "DATA",
        "PYTHON",
        " and especially ",
        "DASH",
        ". My objective is to provide understandable and practical insight based on a ",
        "THOROUGH KNOWLEDGE",
        " of both business and data. I constantly attempt to go the ",
        "EXTRA MILE",
        " to produce the desired outcome. I appreciate ",
        "SHARING",
        " my knowledge and expertise with like-minded others.",
    ],
    "sk": [
        "Ahoj! Volám sa",
        "Martin Rapavý.",
        "Zaujímam sa o ",
        "DÁTA",
        "PYTHON",
        " a obzvlášť o ",
        "DASH",
        ". Mojim cieľom je poskytnúť zrozumiteľný a čo najužitočnejší vhľad do danej problematiky založený na ",
        "DÔKLADNOM POROZUMENÍ",
        " biznisu a dát. Vždy sa snažím ponúknuť niečo ",
        "NAVIAC",
        " pri dosahovaní požadovaných výsledkov. Oceňujem, že sa môžem ",
        "PODELIŤ",
        " o svoje vedomosti a skúsenosti s podobne zmýšľajúcimi ľuďmi.",
    ],
}


def layout(language):
    return page_template(
        mid_col_responsive(
            dmc.Center(
                dmc.Stack(
                    [
                        dmc.Text(text_strings[language][0]),
                        gradient_text(text_strings[language][1], size=40, weight=600),
                        dmc.Text(
                            [
                                text_strings[language][2],
                                gradient_text(
                                    text_strings[language][3],
                                    size=20,
                                    weight=600,
                                    span=True,
                                ),
                                ", ",
                                gradient_text(
                                    text_strings[language][4],
                                    size=20,
                                    weight=600,
                                    span=True,
                                ),
                                text_strings[language][5],
                                gradient_text(
                                    text_strings[language][6],
                                    size=20,
                                    weight=600,
                                    span=True,
                                ),
                                text_strings[language][7],
                                gradient_text(
                                    text_strings[language][8],
                                    size=20,
                                    weight=600,
                                    span=True,
                                ),
                                text_strings[language][9],
                                gradient_text(
                                    text_strings[language][10],
                                    size=20,
                                    weight=600,
                                    span=True,
                                ),
                                text_strings[language][11],
                                gradient_text(
                                    text_strings[language][12],
                                    size=20,
                                    weight=600,
                                    span=True,
                                ),
                                text_strings[language][13],
                            ],
                        ),
                    ],
                    spacing=0,
                    className="animate__animated animate__fadeInUp animate__faster",
                    id="home-stack",
                ),
                style={"height": "calc(100vh - 60px)"},
            )
        ),
        language,
    )


dash.register_page(
    module="home-en",
    path="/en/",
    title="Martin Rapavý - Home",
    description="I am passionate about data, Python and especially Dash. This is my personal platform where I can "
    "showcase my work and share my expertise and experience with the community.",
    image="personal-page-view.png",
    layout=layout("en"),
)

dash.register_page(
    module="home-sk",
    path="/sk/",
    title="Martin Rapavý - Domov",
    description="Zaujímam sa o dáta, Python a obzvlášť o Dash. Toto je môj osobný projekt v ktorom ukazujem svoju prácu"
    " a zdieľam svoje skúsenosti a vedomosti s komunitou.",
    image="personal-page-view.png",
    layout=layout("sk"),
)
