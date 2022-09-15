from dash import html, dcc
import dash_bootstrap_components as dbc
from assets.style import flex_div
from app_utils.probas_graph import get_probability_graph



class PredictionForm:

    def get_page(self):
        return html.Div(
            id='prediction',
            className=flex_div,
            children=[
                self.form,
                self.result
            ]
        )
    
    @property
    def form(self):
        form_element = 'form-element'
        bold = 'bold'
        return dbc.Form(
            id='form',
            className=flex_div,
            children=[
                dcc.Store(id='reset-store'),
                dcc.Store(id='data-store'),
                dcc.Store(id='model-data-store'),

                dbc.Label("Destination", class_name=bold, html_for='destination'),
                dbc.RadioItems(
                    options=[
                        {"label": "PSO J318.5-22", "value": 'pso'},
                        {"label": "TRAPPIST-1e", "value": 'trappist'}
                    ],
                    id="destination",
                    className=form_element,
                    switch=True
                ),
                
                dbc.Label("Home planet", class_name=bold, html_for='home-planet'),
                dbc.RadioItems(
                    options=[
                        {"label": "Europa", "value": 'europa'},
                        {"label": "Mars", "value": 'mars'}
                    ],
                    id="home-planet",
                    className=form_element,
                    switch=True
                ),
                
                dbc.Label("Journey setup", class_name=bold, html_for='j-setup'),
                dbc.Checklist(
                    options=[
                        {"label": "Cabin G/734/s", "value": 'isg'},
                        {"label": "CryoSleep", "value": 'cryo'},
                        {"label": "VIP", "value": 'vip'},
                    ],
                    id="j-setup",
                    className=form_element,
                    switch=True
                ),

                self.__get_number_input('age', 'Age', 79, min=1),
                self.__get_number_input('room', 'RoomService [$]', 14327),
                self.__get_number_input('food', 'FoodCourt [$]', 29813),
                self.__get_number_input('shopping', 'ShoppingMall [$]', 23492),
                self.__get_number_input('spa', 'Spa [$]', 22408),
                self.__get_number_input('vrdeck', 'VRDeck [$]', 24133),
                
                dbc.Button(
                    'Predict',
                    className='form-element-button',
                    id='run-button',
                    color='success',
                    disabled=True
                ),
                dbc.Button(
                    'Reset',
                    className='form-element-button',
                    id='reset-button',
                    type='reset',
                    color='warning',
                    value='reset'
                )
            ]
        )

    @property
    def result(self):
        return html.Div(
            id='probability-graph-div',
            children=[
                html.P("The probability that you'll be rescued from a crash is: ..."),
                dcc.Graph(
                    id='probability-graph',
                    figure=get_probability_graph()
                )
            ]
        )

    def __get_number_input(
        self,
        html_id: str,
        label: str,
        max: int,
        min: int = 0,
        form_element='form-element-number',
        bold='bold'
    ):
        return html.Div(
            id=html_id,
            className=form_element,
            children=[
                dbc.Label(label, className=bold, html_for=f'{html_id}-input'),
                dbc.Input(
                    id=f'{html_id}-input',
                    type='number',
                    min=min,
                    max=max
                ),
            ]
        )