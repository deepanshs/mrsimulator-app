# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

from app import app


SIDEBAR_TAB_NAME = [
    "info",
    "spin_systems",
    "methods",
    "features",
    "fit_report",
    "spectrum",
]


def home():
    """Home tab."""
    icon = html.I(className="fas fa-home fa-lg", title="Home")
    return html.Li(html.Span(icon), id="view-info", className="active")


def spin_system():
    """Spin System tab."""
    icon = html.I(className="fac fa-spin-systems fa-lg", title="Spin Systems")
    return html.Li(html.Span(icon), id="view-spin_systems")


def method():
    """Method tab."""
    icon = html.I(className="fas fa-cube fa-lg", title="Methods")
    return html.Li(html.Span(icon), id="view-methods")


def features():
    """Features tab."""
    icon = html.I(className="fas fa-stream fa-lg", title="Features")
    return html.Li(html.Span(icon), id="view-features")


def fit_report():
    """Fitting report tab."""
    icon = html.I(className="fac fa-chi-squared fa-lg", title="Fit Report")
    return html.Li(html.Span(icon), id="view-fit_report")


def spectrum():
    """Spectrum tab."""
    icon = html.I(className="fac fa-spectrum fa-lg", title="Spectrum")
    return html.Li(html.Span(icon), id="view-spectrum")


def settings():
    """Utility settings tab."""
    icon = html.I(className="fas fa-cog fa-lg", title="Settings")
    return html.Li(html.Span(icon), id="advance-setting")


# toggle active class name for the tabs (home, spin system, method)

app.clientside_callback(
    f"""function () {{
        let trig = dash_clientside.callback_context.triggered.map(t => t["prop_id"]);
        let trig_id = trig[0].split('.')[0].split('-')[1];

        let target = [], tab = [];
        for (item of {SIDEBAR_TAB_NAME}) {{
            target.push((trig_id === item) ? 'left-card active' : 'left-card');
            tab.push((trig_id === item) ? 'active' : null);
        }}

        // Hide the spectrum view if view-fit_report cliked, otherwise reshow
        if (trig_id == 'fit_report') {{
            target[target.length - 1] = "left-card inactive";
        }} else {{
            document.getElementById('view-spectrum').classList.remove('inactive');
        }}

        return target.concat(tab);
    }}""",
    *[Output(f"{item}-body", "className") for item in SIDEBAR_TAB_NAME],
    *[Output(f"view-{item}", "className") for item in SIDEBAR_TAB_NAME],
    *[Input(f"view-{item}", "n_clicks") for item in SIDEBAR_TAB_NAME],
    prevent_initial_call=True,
)

# app.clientside_callback(
#     """function (n, classnames) {
#         let active = classnames.includes('active');
#         let target = [];
#         target.push((!active) ? 'left-card active' : 'left-card');
#         target.push((!active) ? 'active' : null);
#         return target;
#     }""",
#     [
#         Output(f"{item}-body", "className"),
#         Output(f"view-{item}", "className"),
#     ],
#     Input(f"view-{item}", "n_clicks"),
#     State(f"{item}-body", "className"),
#     prevent_initial_call=True,
# )


def sidebar_tabs():
    """Includes
    1. Home
    2. Spin system
    3. Method
    4. Features
    5. Fit report
    6. Spectrum
    """
    content = [home(), method(), spin_system(), features(), fit_report(), spectrum()]
    return html.Ul(content, className="sidebar")


def advanced_settings_modal():
    """Modal window for when settings button is clicked"""

    def number_of_sidebands():
        """Number of sidebands: label [Input]"""
        title = dbc.Label("Number of sidebands")
        field = dbc.Input(
            type="number", value=64, min=1, max=4096, step=1, id="number_of_sidebands"
        )
        return dbc.Row([dbc.Col(title), dbc.Col(field)])

    def integration_density():
        """Integration density: label [Input]"""
        title = dbc.Label("Integration density")
        field = dbc.Input(
            type="number", value=70, min=1, max=4096, step=1, id="integration_density"
        )
        return dbc.Row([dbc.Col(title), dbc.Col(field)])

    def integration_volume():
        """Integration Volume: label [Dropdown]"""
        title = dbc.Label("Integration volume")
        options = [
            {"label": "Octant", "value": "octant"},
            {"label": "Hemisphere", "value": "hemisphere"},
        ]
        field = dcc.Dropdown(
            id="integration_volume",
            options=options,
            value="octant",
            clearable=False,
            searchable=False,
        )
        return dbc.Row([dbc.Col(title), dbc.Col(field)])

    def integration_info():
        """Text field displaying number of crystallite orientations."""
        app.clientside_callback(
            """function (density, vol) {
                let ori = (density + 1) * (density + 2)/2;
                if (vol === 'octant') { return `Averaging over ${ori} orientations.`; }
                return `Averaging over ${ori*4} orientations.`;
            }""",
            Output("integration_points_info", "children"),
            Input("integration_density", "value"),
            Input("integration_volume", "value"),
            prevent_initial_call=False,
        )

        return dbc.Col(dbc.FormText(id="integration_points_info"))

    def body():
        """Modal body"""
        form = [
            integration_density(),
            integration_volume(),
            integration_info(),
            number_of_sidebands(),
        ]
        return dbc.FormGroup(form)

    def footer():
        """Modal footer is a close button"""
        return dbc.Button(
            "Close", id="close_setting", color="dark", className="ml-auto", outline=True
        )

    modal = [
        dbc.ModalHeader("Advanced setting"),  # title
        dbc.ModalBody(body()),  # modal body
        dbc.ModalFooter(footer()),  # modal footer
    ]

    modal_ui = dbc.Modal(
        modal, id="modal_setting", role="document", className="modal-dialogue"
    )

    # callback for toggling modal window visibility
    app.clientside_callback(
        """function (n1, n2, is_open) { return !is_open; }""",
        Output("modal_setting", "is_open"),
        Input("advance-setting", "n_clicks"),
        Input("close_setting", "n_clicks"),
        State("modal_setting", "is_open"),
        prevent_initial_call=True,
    )

    return modal_ui


def utility_tabs():
    """Includes
    1. [Home, Spin System, Method]
    2. Settings
    """
    return html.Ul([settings(), advanced_settings_modal()], className="sidebar button")


def ui():
    """The sidbar UI"""
    content = html.Div([sidebar_tabs(), utility_tabs()], className="view-tools")
    return html.Div(content, className="sidebar-master")


sidebar = ui()
