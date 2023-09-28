import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import html
import dash
from lib.utils import mid_col_responsive

from markdown2dash import parse
import frontmatter
from pathlib import Path
from lib.page_templates import page_template


def blog_card(language, image, title, description, href):
    return dmc.Anchor(
        dmc.Card(
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
                    ],
                    spacing=5,
                    mt=5,
                ),
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            style={"height": "330px"},
        ),
        href=href,
        underline=False,
    )


def blog_layout(title, date, author, content, language):
    return page_template(
        html.Div(
            mid_col_responsive(
                [
                    dmc.Stack(
                        [
                            dmc.Text(title, size=45, weight=600),
                            dmc.Group(
                                [
                                    DashIconify(
                                        icon="mdi:calendar", height=16, width=16
                                    ),
                                    dmc.Text(
                                        date,
                                        size=12,
                                    ),
                                    dmc.Avatar(
                                        src="/assets/surprised-pikachu.png",
                                        size=16,
                                        radius="xl",
                                        ml=10,
                                    ),
                                    dmc.Text(author, size=12),
                                ],
                                spacing=5,
                            ),
                        ],
                        spacing=0,
                        mb=25,
                    )
                ]
                + parse(content),
            ),
            style={"margin-bottom": "100px"},
        ),
        language,
    )


directory = "blog"
files = Path(directory).glob("**/*.md")

all_blogs = {"en": {}, "sk": {}}

for file in files:
    metadata, content = frontmatter.parse(file.read_text(encoding="utf-8"))

    layout = blog_layout(
        metadata["title"],
        metadata["date"],
        metadata["author"],
        content,
        metadata["language"],
    )

    dash.register_page(
        metadata["title"],
        "/" + metadata["language"] + "/blog" + metadata["path"],
        name=metadata["title"],
        title="Martin Rapavý - " + metadata["title"],
        description=metadata["abstract"],
        image=metadata["image"],
        layout=layout,
    )

    all_blogs[metadata["language"]][metadata["path"]] = {
        "date": metadata["date"],
        "title": metadata["title"],
        "abstract": metadata["abstract"],
        "image": metadata["image"],
    }


text_strings = {
    "en": [
        "Newest posts",
    ],
    "sk": [
        "Novinky",
    ],
}


def blog_home_layout(language):
    return page_template(
        dmc.Grid(
            dmc.Col(
                [
                    dmc.Stack(
                        [
                            dmc.Divider(
                                label=text_strings[language][0],
                                size="sm",
                                styles={
                                    "label": {"font-size": "25px", "font-weight": 600}
                                },
                                mt=20,
                            ),
                            dmc.ScrollArea(
                                dmc.Grid(
                                    [
                                        dmc.Col(
                                            blog_card(
                                                language,
                                                image=all_blogs[language][post][
                                                    "image"
                                                ],
                                                title=all_blogs[language][post][
                                                    "title"
                                                ],
                                                description=all_blogs[language][post][
                                                    "abstract"
                                                ],
                                                href="/" + language + "/blog" + post,
                                            ),
                                            span=7,
                                            sm=4,
                                            xl=3,
                                            className="card-hghlght",
                                        )
                                        for post in all_blogs[language]
                                    ],
                                    columns=10,
                                    m=0,
                                    className="content",
                                )
                            ),
                        ],
                        spacing=5,
                    )
                ],
                span=10,
                offset=1,
                p=0,
            ),
            m=0,
        ),
        language,
    )


dash.register_page(
    module="blog-en",
    path="/en/blog",
    redirect_from=["/blog"],
    title="Martin Rapavý - Blog",
    description="I am passionate about data, Python and especially Dash. This is my platform to share my knowledge and"
    " my experience with yout.",
    image="personal-page-view.png",
    layout=blog_home_layout("en"),
)

dash.register_page(
    module="blog-sk",
    path="/sk/blog",
    title="Martin Rapavý - Blog",
    description="Zaujímam sa o dáta, Python a obzvlášť o Dash. Toto je moja platforma na ktorej chcem s vami zdieľať "
    "svoje znalosti a skúsenosti.",
    image="personal-page-view.png",
    layout=blog_home_layout("sk"),
)
