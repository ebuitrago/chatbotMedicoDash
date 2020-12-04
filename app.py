# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 08:48:50 2020

@author: ebuit
Inspired in examples taken from:
    https://dash.plotly.com/dash-core-components/input
    https://stackoverflow.com/questions/51407191/python-dash-get-value-from-input-text
    https://github.com/AdamSpannbauer/app_rasa_chat_bot/blob/master/dash_demo_app.py
"""
# import dash_core_components as dcc
# import dash_html_components as html
# import dash
# from dash.dependencies import Input, Output

# app = dash.Dash(__name__)
# app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


# ALLOWED_TYPES = (
#     "text",
# )


# app.layout = html.Div(
#     [
#         dcc.Input(
#             id="input_{}".format(_),
#             type=_,
#             placeholder="input type {}".format(_),
#         )
#         for _ in ALLOWED_TYPES
#     ]
#     + [html.Div(id="out-all-types")]
# )


# @app.callback(
#     Output("out-all-types", "children"),
#     [Input("input_{}".format(_), "value") for _ in ALLOWED_TYPES],
# )
# def cb_render(*vals):
#     return " | ".join((str(val) for val in vals if val))


# if __name__ == "__main__":
#     app.run_server(debug=True)



# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Output, State, Input

# if __name__ == '__main__':
#     app = dash.Dash()

    # app.layout = html.Div([
    #     dcc.Input(id='username', value='Initial Value', type='text'),
    #     html.Button(id='submit-button', type='submit', children='Submit'),
    #     html.Div(id='output_div')
    # ])
    
#     app.layout = html.Div([
#     html.H3('Elison: el chatbot para prevención de riesgo cardiovascular', style={'text-align': 'center'}),
#     html.Div([
#         html.Div([
#             html.Table([
#                 html.Tr([
#                     # text input for user message
#                     html.Td([dcc.Input(id='msg_input', value='hello', type='text')],
#                             style={'valign': 'middle'}),
#                     # message to send user message to bot backend
#                     html.Td([html.Button('Send', id='submit-button', type='submit')],
#                             style={'valign': 'middle'})
#                 ])
#             ])],
#             style={'width': '325px', 'margin': '0 auto'}),
#         html.Br(),
#         html.Div(id='conversation')],
#         id='screen',
#         style={'width': '400px', 'margin': '0 auto'})
# ])
       

    # @app.callback(Output('output_div', 'children'),
    #               [Input('submit-button', 'n_clicks')],
    #               [State('username', 'value')],
    #               )
    # def update_output(clicks, input_value):
    #     if clicks is not None:
            
#     #         print(clicks, input_value)

# if __name__ == "__main__":
#     app.run_server(debug=True)




import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
from utils import *

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Textarea(
        id='textarea-conversacion',
        value='¡Bienvenido! Soy Elison.\
            \n Te ayudaré en la prevención de riesgo cardiovascular.\
            \n ¿Cuál es tu nombre?',
        style={'width': '60%', 'height': 200},
    ),
    
    dcc.Textarea(
        id='textarea-usuario',
        value='Textarea content initialized\nwith multiple lines of text',
        style={'width': '60%', 'height': 100},
    ),
    html.Div(
         html.Button('Submit', id='textarea-usuario-button', n_clicks=0),
        )
    # html.Div(id='textarea-usuario-output', style={'whiteSpace': 'pre-line'})
])

@app.callback(
    Output('textarea-conversacion', 'value'),
    Input('textarea-usuario-button', 'n_clicks'),
    State('textarea-usuario', 'value')
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        res = chatbot_response(value),
        return res


if __name__ == '__main__':
    app.run_server(debug=True)

