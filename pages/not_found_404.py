import dash
from dash import html
import dash_mantine_components as dmc
from lib.page_templates import page_template
from lib.utils import mid_col_responsive, gradient_text

dash.register_page(__name__)

layout = page_template(
    mid_col_responsive(
        dmc.Center(
            [
                dmc.Stack(
                    [
                        dmc.Image(
                            src="/assets/surprised-pikachu-trans-bg.png",
                            style={"max-width": "500px"},
                        ),
                        dmc.Text("Oops!", size=45, weight=700),
                        dmc.Text(
                            [
                                gradient_text("404", size=30, weight=600, span=True),
                                " - Page Not Found",
                            ],
                            size=30,
                            weight=600,
                        ),
                    ],
                    align="center",
                    spacing=0,
                )
            ],
            style={"height": "calc(100vh - 43px)"},
        )
    ),
    "en",
)
