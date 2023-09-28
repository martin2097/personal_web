import dash_mantine_components as dmc
from lib.utils import mid_col_responsive
from lib.page_templates import page_template
import dash


def project_card(language, image, title, description, href):
    return dmc.Card(
        children=[
            dmc.CardSection(
                dmc.Image(
                    src=image,
                    height=160,
                )
            ),
            dmc.Stack(
                [
                    dmc.Text(title, weight=500),
                    dmc.Text(
                        description,
                        size="sm",
                        color="dimmed",
                        style={"height": "65px"},
                    ),
                    dmc.Anchor(
                        dmc.Button(
                            "Navštíviť projekt"
                            if language == "sk"
                            else "Visit project",
                            variant="light",
                            fullWidth=True,
                            mt="md",
                            radius="md",
                        ),
                        href=href,
                    ),
                ],
                spacing=5,
                mt=5,
            ),
        ],
        withBorder=True,
        shadow="sm",
        radius="md",
        style={"height": "330px"},
    )


text_strings = {"en": ["Public projects"], "sk": ["Realizované projekty"]}

project_strings = {
    "en": [
        {
            "image": "/assets/survivor-statistky-nahlad.PNG",
            "title": "Survivor statistics",
            "description": "Statistics of Czech & Slovak version of reality show Survivor",
            "href": "/en/survivor-statistics",
        }
    ],
    "sk": [
        {
            "image": "/assets/survivor-statistky-nahlad.PNG",
            "title": "Survivor štatistky",
            "description": "Štatistiky Česko-Slovenskej verzie reality show Survivor",
            "href": "/sk/survivor-statistics",
        }
    ],
}


def layout(language):
    return page_template(
        mid_col_responsive(
            [
                dmc.Stack(
                    [
                        dmc.Divider(
                            label=text_strings[language][0],
                            size="sm",
                            styles={"label": {"font-size": "25px", "font-weight": 600}},
                            mb=10,
                        ),
                        dmc.Grid(
                            [
                                dmc.Col(
                                    [
                                        project_card(
                                            language=language,
                                            image=project["image"],
                                            title=project["title"],
                                            description=project["description"],
                                            href=project["href"],
                                        )
                                        for project in project_strings[language]
                                    ],
                                    sm=6,
                                )
                            ],
                            gutterSm=30,
                            gutter=0,
                            style={"margin": "0px"},
                        ),
                    ],
                    spacing=0,
                    className="animate__animated animate__fadeInUp animate__faster",
                    id="projects-stack",
                )
            ]
        ),
        language,
    )


dash.register_page(
    module="projects-en",
    path="/en/projects",
    redirect_from=["/projects"],
    title="Martin Rapavý - Projects",
    description="I am passionate about data, Python and especially Dash. This is the page with my public projects.",
    image="personal-page-view.png",
    layout=layout("en"),
)

dash.register_page(
    module="projects-sk",
    path="/sk/projects",
    title="Martin Rapavý - Kontaktujte ma",
    description="Zaujímam sa o dáta, Python a obzvlášť o Dash. Toto je stránka s mojimi verejnými projektami.",
    image="personal-page-view.png",
    layout=layout("sk"),
)
