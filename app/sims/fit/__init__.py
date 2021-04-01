# -*- coding: utf-8 -*-
import dash_html_components as html


def ui():
    page = html.Div("")

    return html.Div(
        className="left-card",
        children=page,
        id="fit-body",
    )


fit_body = ui()
