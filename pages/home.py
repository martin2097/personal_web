import dash
import dash_mantine_components as dmc
from lib.utils import gradient_text, mid_col_responsive

dash.register_page(
    __name__,
    path="/",
    title="Martin Rapavý - Home",
    description="I am passionate about data, Python and especially Dash. This is my personal platform where I can "
    "showcase my work and share my expertise and experience with the community.",
    image="personal-page-view.png",
)

layout = mid_col_responsive(
    dmc.Center(
        dmc.Stack(
            [
                dmc.Text("Ahoj! My name is"),
                gradient_text("Martin Rapavý.", size=40, weight=600),
                dmc.Text(
                    [
                        "I am passionate about ",
                        gradient_text(
                            "DATA",
                            size=20,
                            weight=600,
                            span=True,
                        ),
                        ", ",
                        gradient_text(
                            "PYTHON",
                            size=20,
                            weight=600,
                            span=True,
                        ),
                        " and especially ",
                        gradient_text(
                            "DASH",
                            size=20,
                            weight=600,
                            span=True,
                        ),
                        ". My objective is to provide understandable and practical insight based on a ",
                        gradient_text(
                            "THOROUGH KNOWLEDGE",
                            size=20,
                            weight=600,
                            span=True,
                        ),
                        " of both business and data. I constantly attempt to go the ",
                        gradient_text(
                            "EXTRA MILE",
                            size=20,
                            weight=600,
                            span=True,
                        ),
                        " to produce the desired outcome. I appreciate ",
                        gradient_text(
                            "SHARING",
                            size=20,
                            weight=600,
                            span=True,
                        ),
                        " my knowledge and expertise with like-minded others.",
                    ],
                ),
            ],
            spacing=0,
            className="animate__animated animate__fadeInUp animate__faster",
            id="home-stack",
        ),
        style={"height": "calc(100vh - 43px)"},
    )
)
