import dash
import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify
from lib.utils import visit_link_icon, mid_col_responsive

dash.register_page(
    __name__,
    title="Martin Rapavý - Contact Me",
    description="I am passionate about data, Python and especially Dash. If you have any questions, comments, or other "
    "feedback, don't hesitate to get in touch with me.",
    image="personal-page-view.png",
)

layout = mid_col_responsive(
    dmc.Center(
        dmc.Stack(
            [
                dmc.Text("Contact Me", size=50),
                dmc.Space(h=40),
                dmc.Text(
                    "If you have any questions, comments, or other feedback, don't hesitate to get in touch with me.",
                ),
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
        style={"height": "calc(100vh - 43px)"},
    )
)
