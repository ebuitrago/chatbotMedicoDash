# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 08:48:50 2020

@author: ebuit
Inspired in examples taken from:
    https://dash.plotly.com/dash-core-components/input
    https://stackoverflow.com/questions/51407191/python-dash-get-value-from-input-text
    https://github.com/AdamSpannbauer/app_rasa_chat_bot/blob/master/dash_demo_app.py
"""

import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc

import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intenciones.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

tableau = 'https://public.tableau.com/profile/sonia.ardila#!/vizhome/Pacientes_Dashboard/Dashboard1?publish=yes'



"""
-----------------------------------------------------
# Funciones requeridas para el chatbot
-----------------------------------------------------
"""
# Función para preprocesamiento
def clean_up_sentence(sentence):
    # Tokenizar el patrón - dividir las palabras en un arreglo
    sentence_words = nltk.word_tokenize(sentence, 'spanish')
    # Crear una forma orta para cada palabra
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# Retornar el arreglo del bag-of-words: 0 or 1 para cada palabra en la bolsa que exista en la oracióm
def bow(sentence, words, show_details=True):
    # tokeinzar el patrón
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matriz con N palabras, matriz de vocabulario
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                # asignar 1 si la palabra actual esta en la posición de vocabulario
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

# Función para predicción
def predict_class(sentence, model):
    # filtrar predicciones por debajo e un umbral
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # ordenar por probabilidad
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

# Función para obtener entrada de texto
def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['respuestas'])
            break
    return result

# Función para responder
def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res




"""
-----------------------------------------------------
Aplicación dash
-----------------------------------------------------
"""


app = dash.Dash(__name__)

app.layout = html.Div([
                        # Selector title
    html.H1(
        "Elison: tu amigo en el diagnóstico de riesgo cardiovascular",
        id="title",
        style={
            "text-align": "left",
            "font-weight": "bold",
            "display": "block",
            "color": "black"},
    ),
    dcc.Textarea(
        id='textarea-conversacion',
        value='¡Bienvenido! Soy Elison.\
            \n Te ayudaré en la prevención de riesgo cardiovascular.',
        style={'width': '50%', 'height': 200},
    ),
    dcc.Input(
        id='input-usuario',
        value='',
        type='text',
        children='value',
        style={'width': '50%', 'height': 60},
    ),
    html.Div(
         html.Button('Enviar tu respuesta a Elison', id='input-usuario-button', n_clicks=0),
        ),
    html.Div(
         html.H3(
                "Elison recomienda:",
                id="title_recomendacion",
                style={
                    "text-align": "left",
                    "font-weight": "bold",
                    "display": "block",
                    "color": "green"},
        ),
    ),
    dcc.Link('¿Quieres aprender sobre estadísticas de riesgo cardiovascular? Sigue este enlace para visualizar algunas gráficas que he preparado para ti.', href=tableau),
])


@app.callback(
    Output('textarea-conversacion', 'value'),
    Input('input-usuario-button', 'n_clicks'),
    State('input-usuario', 'value')
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        value = str(chatbot_response(value))
    else:
        value='¡Hola! Soy Elison. \nTe ayudaré en la prevención de riesgo cardiovascular.'
    return value



@app.callback(
    Output('input-usuario', 'value'),
    [Input('textarea-conversacion', 'value')]
)
def clear_input(_):
    return ''



if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port='8051', debug=True)
