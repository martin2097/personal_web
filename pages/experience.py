import dash
import dash_mantine_components as dmc
from dash import html
from lib.utils import mid_col_responsive

dash.register_page(__name__, title="Martin Rapavý - Experience")

work_experience = [
    {
        "id": "raiffeisenbank",
        "image": "/assets/rb_logo.jpg",
        "label": "Raiffeisenbank - Credit Policy Manager",
        "description": "July 2018 - Present (Prague)",
        "content": [
            "Managing the Portfolio Quality Report and making it a trustworthy data source that is utilized by many "
            "others",
            "Migrating PQR from Excel to Python using Plotly Dash and building the platform for advanced analytics "
            "around it",
            "Throughout the pandemic, I coordinated the development of an internal application that processed 14 000 "
            "applications for postponed payments, finishing the task in only two months",
            "Played an important role in the data integration of EquaBank's risk department and carried over the "
            "reporting following the merger",
            "Creating apps that allow non-technical people to access and manage their data (since Excel is not a "
            "database!)",
            "Organizing Show&Tell sessions for our department to encourage sharing of knowledge and experience",
        ],
    },
]

education = [
    {
        "id": "masters",
        "image": "/assets/cuni_logo.jpg",
        "label": "Charles University - Numerical and Computational Mathematics",
        "description": "2017 - 2019 - Master's degree",
        "content": [
            "Thesis: Global krylov methods for solving linear algebraic problems with matrix observations",
            "We studied some new methods for solving systems of linear algebraic equations with multiple right hand "
            "sides",
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
]


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


layout = mid_col_responsive(
    dmc.Accordion(
        chevronPosition="left",
        variant="filled",
        radius="lg",
        children=[
            dmc.Divider(
                label="Work Experience",
                size="sm",
                styles={"label": {"font-size": "20px", "font-weight": 600}},
                mt=20,
                mb=10,
            ),
        ]
        + create_accordion(work_experience)
        + [
            dmc.Divider(
                label="Education",
                size="sm",
                styles={"label": {"font-size": "20px", "font-weight": 600}},
                mt=20,
                mb=10,
            ),
        ]
        + create_accordion(education),
        className="animate__animated animate__fadeInUp animate__faster",
        classNames={
            "chevron": "animate__animated animate__heartBeat animate__delay-3s"
        },
    )
)
