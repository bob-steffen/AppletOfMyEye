import dash
import dash_core_components as dcc
import dash_html_components as html

# Make the following dynamic
# angle
# view distance
# width/height of screen
# body height
# head radius
# head x & y


# ALLOWED_TYPES = (
#     "text", "number", "password", "email", "search",
#     "tel", "url", "range", "hidden",
# )

fields = {
    "body height": "number",
    "head x & y": "number",
    "angle": "range",
    "view distance": "range",
    "width/height of screen": "range",
    "head radius": "range",
}

fields_style = {
    'width': '10%',
    'display': 'inline-block'
}

def create_div(text_placeholder, type_input):
    new_div = html.Div(
                children=[
                    html.H5(
                        id=text_placeholder+"1",
                        children=text_placeholder+":",
                        style=fields_style
                    ),
                    dcc.Input(
                        id=f"input_{text_placeholder}",
                        type=type_input,
                        placeholder=f"enter {text_placeholder}",
                        style=fields_style
                    )
                ],
            )
    return new_div

fields_html = [create_div(k, v) for k, v in fields.items()]
fields_html += [html.Div(id="out-all-types")]

app = dash.Dash(__name__)

app.layout = html.Div(
    fields_html
)

if __name__ == '__main__':
    app.run_server(debug=True)
