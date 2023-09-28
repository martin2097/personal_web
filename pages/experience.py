import dash
import dash_mantine_components as dmc
from dash import html
from lib.utils import mid_col_responsive
from lib.page_templates import page_template

work_experience = {
    "en": [
        {
            "id": "raiffeisenbank",
            "image": "/assets/rb_logo.jpg",
            "label": "Raiffeisenbank - Credit Policy Manager",
            "description": "July 2018 - Present (Prague)",
            "content": [
                "Managing the Portfolio Quality Report and making it a trustworthy data source that is utilized by many"
                " others",
                "Migrating PQR from Excel to Python using Plotly Dash and building the platform for advanced analytics "
                "around it",
                "Throughout the pandemic, I coordinated the development of an internal application that processed "
                "14 000 applications for postponed payments, finishing the task in only two months",
                "Played an important role in the data integration of EquaBank's risk department and carried over the "
                "reporting following the merger",
                "Creating apps that allow non-technical people to access and manage their data (since Excel is not a "
                "database!)",
                "Organizing Show&Tell sessions for our department to encourage sharing of knowledge and experience",
            ],
        },
    ],
    "sk": [
        {
            "id": "raiffeisenbank",
            "image": "/assets/rb_logo.jpg",
            "label": "Raiffeisenbank - Credit Policy Manager",
            "description": "Júl 2018 - Súčasnosť (Praha)",
            "content": [
                "Správa Portfolio Quality Reportu - široký dátový zdroj využívaný naprieč bankou",
                "Migrácia PQR z Excelu do Pythonu využitím Plotly Dash a vytvorenie platformy na tvorbu pokročilých "
                "analýz",
                "Počas pandémie som koordinoval vývoj internej aplikácie, pomocou ktorej sme sprocesovali 14 000 "
                "žiadostí na odklad splátok. Vývoj trval iba dva mesiace",
                "Zastával som jednu z kľúčových úloh počas integrácie riskových dát z EquaBank a naviazal na "
                "reporting po zlúčení oboch bánk",
                "Tvorba aplikácí ktoré umožňujú netechnickým používateľom tvorbu a správu dát (pretože Excel nie je "
                "databáza!)",
                "Organizácia stretnutí Show&Tell pre naše oddelenie nabádajúce k rozsiahlejšiemu zdieľaniu vedomostí a "
                "skúseností",
            ],
        },
    ],
}

education = {
    "en": [
        {
            "id": "masters",
            "image": "/assets/cuni_logo.jpg",
            "label": "Charles University - Numerical and Computational Mathematics",
            "description": "2017 - 2019 - Master's degree",
            "content": [
                "Thesis: Global krylov methods for solving linear algebraic problems with matrix observations",
                "We studied some new methods for solving systems of linear algebraic equations with multiple right hand"
                " sides",
            ],
        },
        {
            "id": "bachelors",
            "image": "/assets/cuni_logo.jpg",
            "label": "Charles University - Mathematics",
            "description": "2017 - 2019 - Bachelor's degree",
            "content": [
                "Thesis: The choice of the step in trust region methods",
                "Finding a way how to tinker a parameter in a very clever methods used to find a minimum of a function",
            ],
        },
    ],
    "sk": [
        {
            "id": "masters",
            "image": "/assets/cuni_logo.jpg",
            "label": "Karlova Univerzita - Numerická a výpočetná matematika",
            "description": "2017 - 2019 - Magisterské štúdium",
            "content": [
                "Thesis: Global krylov methods for solving linear algebraic problems with matrix observations",
                "We studied some new methods for solving systems of linear algebraic equations with multiple right hand"
                " sides",
            ],
        },
        {
            "id": "bachelors",
            "image": "/assets/cuni_logo.jpg",
            "label": "Karlova Univerzita - Matematika",
            "description": "2017 - 2019 - Bakalárské štúdium",
            "content": [
                "Thesis: The choice of the step in trust region methods",
                "Finding a way how to tinker a parameter in a very clever methods used to find a minimum of a function",
            ],
        },
    ],
}

text_strings = {
    "en": ["Work Experience", "Education"],
    "sk": ["Pracovné skúsenosti", "Vzdelanie"],
}


def create_accordion_label(label, image, description):
    """
    :param label: The label of the accordion label
    :param image: The image source for the avatar
    :param description: The description text for the accordion label
    :return: A dash_mantine_components.AccordionControl object representing the created accordion label
    """
    return dmc.AccordionControl(
        dmc.Grid(
            [
                dmc.Col(
                    [
                        dmc.Avatar(src=image, radius="xl", size="lg"),
                    ],
                    span="content",
                ),
                dmc.Col(
                    [
                        dmc.Text(label),
                        dmc.Text(description, size="sm", weight=400, color="dimmed"),
                    ],
                    span="auto",
                ),
            ]
        )
    )


def create_accordion_content(content_list):
    """
    Creates an accordion panel with a list of contents.

    :param content_list: A list of content items for the accordion panel.
    :type content_list: list
    :return: An accordion panel component with the specified content.
    :rtype: dash_mantine_components.AccordionPanel
    """
    return dmc.AccordionPanel(
        dmc.List(
            [
                dmc.ListItem(dmc.Text([dmc.Text(content, size="sm")]))
                for content in content_list
            ],
            pl=10,
            pr=30,
            pb=10,
        )
    )


def create_accordion(accordion_data):
    """
    Create an accordion component based on the provided accordion data.

    :param accordion_data: A list of dictionaries representing each accordion item. Each dictionary should have the following keys:
        - "label": The label of the accordion item.
        - "image": The image URL for the accordion item.
        - "description": The description of the accordion item.
        - "content": The content (HTML) of the accordion item.
    :return: The created accordion component.
    """
    return [
        dmc.AccordionItem(
            [
                create_accordion_label(
                    acc_item["label"], acc_item["image"], acc_item["description"]
                ),
                create_accordion_content(acc_item["content"]),
            ],
            value=acc_item["id"],
        )
        for acc_item in accordion_data
    ]


def layout(language):
    return page_template(
        mid_col_responsive(
            dmc.Accordion(
                chevronPosition="left",
                variant="filled",
                radius="lg",
                children=[
                    dmc.Divider(
                        label=text_strings[language][0],
                        size="sm",
                        styles={"label": {"font-size": "20px", "font-weight": 600}},
                        mb=10,
                    ),
                ]
                + create_accordion(work_experience[language])
                + [
                    dmc.Divider(
                        label=text_strings[language][1],
                        size="sm",
                        styles={"label": {"font-size": "20px", "font-weight": 600}},
                        mt=20,
                        mb=10,
                    ),
                ]
                + create_accordion(education[language]),
                className="animate__animated animate__fadeInUp animate__faster",
                classNames={
                    "chevron": "animate__animated animate__heartBeat animate__delay-3s"
                },
            )
        ),
        language,
    )


dash.register_page(
    module="experience-en",
    path="/en/experience",
    redirect_from=["/experience"],
    title="Martin Rapavý - Experience",
    description="I am passionate about data, Python and especially Dash. I've been working at a major Czech bank for "
    "the last five years, trying to establish the data culture to meet the most recent standards.",
    image="personal-page-view.png",
    layout=layout("en"),
)

dash.register_page(
    module="experience-sk",
    path="/sk/experience",
    title="Martin Rapavý - Skúsensoti",
    description="Zaujímam sa o dáta, Python a obzvlášť o Dash. Posledných 5 rokov pracujem v jednej z najväčších "
    "českých bánk kde sa snažím rozvíjať dátovú kultúru v súlade s modernými štandardmi.",
    image="personal-page-view.png",
    layout=layout("sk"),
)
