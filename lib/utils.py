from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify


def gradient_text(text, **kwargs):
    """
    :param text: The text to display with gradient effect.
    :param kwargs: Additional keyword arguments to pass to the `dmc.Text` component.
    :return: A `dmc.Text` component with the specified text and gradient effect.
    """
    return dmc.Text(
        text,
        variant="gradient",
        gradient={"from": "blue", "to": "teal", "deg": 45},
        **kwargs
    )


def visit_link_icon(link, icon):
    """
    :param link: The URL that the icon should link to.
    :param icon: The name of the icon to be displayed.
    :return: An HTML anchor element with an action icon and a link to the specified URL.
    """
    return html.A(
        dmc.ActionIcon(
            DashIconify(
                icon=icon,
                width=30,
            ),
            size="lg",
            variant="transparent",
        ),
        href=link,
        target="_blank",
    )


def mid_col_responsive(content):
    return (
        dmc.Grid(
            dmc.Col(
                content,
                span=10,
                sm=8,
                xl=6,
                offset=1,
                offsetSm=2,
                offsetXl=3,
                p=0,
                pt=40,
            ),
            m=0,
        ),
    )
