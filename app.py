import dash
import dash_core_components as dcc
import dash_html_components as html

# TODO: Make the following dynamic
# angle
# view distance
# width/height of screen
# body height
# head radius
# head x & y

# THESE ARE THE FIELD TYPES THAT DASH SUPPORTS:
# ALLOWED_TYPES = (
#     "text", "number", "password", "email", "search",
#     "tel", "url", "range", "hidden",
# )

def create_table_row(title, value):
    title_id = title.split(" ")
    title_id = "-".join(title_id)

    tbody = html.Tbody(
        children=[
            html.Tr(
                children=[
                    html.Th(scope="row", children=[title]),
                    html.Td(
                        id=title_id,
                        children=[
                            dcc.Input(
                                id=f"input_{title}",
                                type=value,
                                placeholder=f"enter {title}"
                            )
                        ]
                    )
                ]
            ),
        ]
    )

    return tbody

fields = {
    "body height": "number",
    "head x": "number",
    "head y": "number",
    "angle": "range",
    "view distance": "range",
    "width/height of screen": "range",
    "head radius": "range",
}

tbodies = [create_table_row(k, v) for k, v in fields.items()]

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.Table(
            id='variable-table',
            children=[
                html.Thead(
                    children=[
                        html.Tr(
                            children=[
                                html.Th(scope="col", children=[html.H3(children="Parameter")]),
                                html.Th(scope="col", children=[html.H3(children="Value")])
                            ]
                        ) #end Tr
                    ]
                ), #end Thead
                *tbodies
            ]
        ) # end table
    ],
    style={'display': 'inline-block'}
) # end div

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)

























# NOTES:
# "Pixel Pitch (um)"
# "Diameter of Hogel (mm)"
# "View Distance (mm)"
# "Lossless Projection Depth (mm)"
# "Angular Resolution"

# id='pixel-pitch-id',
# id='hogel-diameter-id',
# id='view-distance-id',
# id='lossless-depth-id',
# id='angular-resolution-id',

# def create_dynamic_form(text_placeholder, type_input):
    # new_div = html.Div(
    #             children=[
                    # html.H5(
                    #     id=text_placeholder+"1",
                    #     children=text_placeholder+":",
                    #     style=fields_style
                    # ),
    #                 dcc.Input(
    #                     id=f"input_{text_placeholder}",
    #                     type=type_input,
    #                     placeholder=f"enter {text_placeholder}",
    #                     style=fields_style
    #                 )
    #             ],
    #         )
    # return new_div

# fields_style = {
#     'width': '10%',
#     'display': 'inline-block'
# }

# fields_html = [create_dynamic_form(k, v) for k, v in fields.items()]
# fields_html += [html.Div(id="out-all-types")]


# def create_param_val_pair(param, val):
#     param_id = param.split(" ")
#     param_id = "-".join(param_id)

#     tbody = html.Tbody(
#         children=[
#             html.Tr(
#                 children=[
#                     html.Th(scope="row", children=[param]),
#                     html.Td(
#                         id=param_id,
#                         children=[val]
#                     )
#                 ]
#             ),
#         ]
#     )

#     return tbody