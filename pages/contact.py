import dash
import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify
from lib.utils import visit_link_icon, mid_col_responsive
from lib.page_templates import page_template

text_strings = {
    "en": [
        "Contact Me",
        "If you have any questions, comments, or other feedback, don't hesitate to get in touch with me.",
    ],
    "sk": [
        "Kontaktujte ma",
        "V prípade akýchkoľvek otázok, komentárov alebo inej spätnej väzby sa so mnou neváhajte spojiť.",
    ],
}


def layout(language):
    return page_template(
        mid_col_responsive(
            dmc.Center(
                dmc.Stack(
                    [
                        dmc.Text(text_strings[language][0], size=40),
                        dmc.Space(h=40),
                        dmc.Text(text_strings[language][1]),
                        dmc.Space(h=20),
                        dmc.Stack(
                            [
                                dmc.Group(
                                    [
                                        visit_link_icon(
                                            "mailto:rapavy.mato@gmail.com",
                                            "material-symbols:mail",
                                        ),
                                        dmc.Text("rapavy.mato@gmail.com"),
                                    ],
                                ),
                                dmc.Group(
                                    [
                                        visit_link_icon(
                                            "https://linkedin.com/in/martin-rapavy",
                                            "mdi:linkedin",
                                        ),
                                        dmc.Text("/in/martin-rapavy/"),
                                    ],
                                ),
                            ],
                            spacing=0,
                        ),
                    ],
                    spacing=0,
                    align="center",
                    className="animate__animated animate__fadeInUp animate__faster",
                    id="contact-stack",
                ),
                style={"height": "calc(100vh - 60px)"},
            )
        ),
        language,
    )


dash.register_page(
    module="contact-en",
    path="/en/contact",
    redirect_from=["/contact"],
    title="Martin Rapavý - Contact Me",
    description="I am passionate about data, Python and especially Dash. If you have any questions, comments, or other "
    "feedback, don't hesitate to get in touch with me.",
    image="personal-page-view.png",
    layout=layout("en"),
)

dash.register_page(
    module="contact-sk",
    path="/sk/contact",
    title="Martin Rapavý - Kontaktujte ma",
    description="Zaujímam sa o dáta, Python a obzvlášť o Dash. V prípade akýchkoľvek otázok, komentárov alebo inej "
    "spätnej väzby sa so mnou neváhajte spojiť.",
    image="personal-page-view.png",
    layout=layout("sk"),
)
