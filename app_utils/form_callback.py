import dash
from dash import html, dcc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
import pandas as pd
import os
import pickle
from plotly.graph_objects import Figure
from app_utils.data_validation import RawData
from app_utils.preprocessor import Preprocessor
from app_utils.prediction_pipeline import PredictionPipeline
from app_utils.probas_graph import get_probability_graph



class FormCallback:

    MODELS_PATH = os.path.join('models', 'values.pickle')

    def __init__(self, app: dash.Dash):
            self.app = app
    
    def run_callbacks(self):
        self._button_disabled()
        self._reset_n_clicks()
        self._save_values()
        self._save_model_data()
        self._update_graph()

    def _button_disabled(self):
        @self.app.callback(
            Output('run-button', 'disabled'),
            [
                Input('age-input', 'value'),
                Input('room-input', 'value'),
                Input('food-input', 'value'),
                Input('shopping-input', 'value'),
                Input('spa-input', 'value'),
                Input('vrdeck-input', 'value'),
                Input('reset-button', 'n_clicks')
            ],
            State('reset-store', 'data')
        )
        def callback(
            age: int,
            room: int,
            food: int,
            shopping: int,
            spa: int,
            vrdeck: int,
            n_clicks: int,
            n_clicks_history: int
        ) -> bool:
            if n_clicks is None:
                n_clicks = 0
            if n_clicks_history is None:
                n_clicks_history = 0

            if n_clicks > n_clicks_history:
                disabled = True
            else:
                values = [age, room, food, shopping, spa, vrdeck]
                disabled = False
                for value in values:
                    if value is None:
                        disabled = True
                        break

            return disabled
    
    def _reset_n_clicks(self) -> int:
        @self.app.callback(
            Output('reset-store', 'data'),
            Input('reset-button', 'n_clicks')
        )
        def reset_storage(n: int) -> bool:
            return n
    
    def _save_values(self):
        @self.app.callback(
            Output('data-store', 'data'),
            Input('run-button', 'n_clicks'),
            [
                State('age-input', 'value'),
                State('room-input', 'value'),
                State('food-input', 'value'),
                State('shopping-input', 'value'),
                State('spa-input', 'value'),
                State('vrdeck-input', 'value'),
                State('destination', 'value'),
                State('home-planet', 'value'),
                State('j-setup', 'value')
            ]
        )
        def callback(
            n_clicks: int,
            age: int,
            room: int,
            food: int,
            shopping: int,
            spa: int,
            vrdeck: int,
            destination: str,
            home_planet: str,
            j_setup: list
        ) -> dict:
            data = {
                'age': age,
                'room': room,
                'food': food,
                'shopping': shopping,
                'spa': spa,
                'vrdeck': vrdeck,
                'destination': destination,
                'home': home_planet,
                'setup': j_setup
            }
            return data

    def _save_model_data(self):
        @self.app.callback(
            Output('model-data-store', 'data'),
            Input('data-store', 'data')
        )
        def callback(data: dict) -> dict:
            raw_df = self.__prepare_data(data)

            with open(self.MODELS_PATH, 'rb') as file:
                values_dict = pickle.load(file)
            
            proc = Preprocessor(
                raw_data = raw_df,
                means_dict=values_dict['means'],
                std_dict=values_dict['std']
            )
            processed_df: pd.DataFrame = proc.get_data()
            
            pipeline = PredictionPipeline(processed_df)
            pipeline.run_model()
            final_proba = pipeline.get_prediction()
            
            probas_data = pipeline.data[pipeline.PROBAS_COLS].loc[0].to_dict()
            probas_data['final'] = final_proba

            return probas_data

    def _update_graph(self):
        @self.app.callback(
            Output('probability-graph-div', 'children'),
            Input('model-data-store', 'data')
        )
        def callback(data: dict) -> Figure:
            try:
                data['AdaBoost'] = data.pop('ada_boost')
                data['SVC'] = data.pop('svc')
                data['LightGBM'] = data.pop('lgbm')
                data['NeuralNetwork'] = data.pop('neural')
                data['MeanProbability'] = data.pop('mean')
                final = data.pop('final')
            except AttributeError:
                raise PreventUpdate

            fig = get_probability_graph(data, final)
            text = html.P(f"The probability that you'll be rescued from a crash is: {round(final *100, 2)}%")
            graph = dcc.Graph(id='probability-graph', figure=fig)

            return [text, graph]

    def __prepare_data(self, data: dict) -> pd.DataFrame:
        def check_setup(value: str, key: str, data: dict) -> bool:
            if data[key] is not None:
                output = True if value in data[key] else False
            else:
                output = False
            
            return output
        
        def check_others(value: str, key: str, data: dict) -> bool:
            if data[key] is not None:
                output = True if value == data[key] else False
            else:
                output = False
            
            return output

        is_g = check_setup('isg', 'setup', data)
        cryo = check_setup('cryo', 'setup', data)
        vip = check_setup('vip', 'setup', data)
        europa = check_others('europa', 'home', data)
        mars = check_others('mars', 'home', data)
        pso = check_others('pso', 'destination', data)
        trappist = check_others('trappist', 'destination', data)

        try:
            df = pd.DataFrame({
                RawData.is_g: [is_g],
                RawData.cryo_sleep: [cryo],
                RawData.vip: [vip],
                RawData.europa: [europa],
                RawData.mars: [mars],
                RawData.pso: [pso],
                RawData.trappist: [trappist],
                RawData.age: [int(data['age'])],
                RawData.room_service: [int(data['room'])],
                RawData.food: [int(data['food'])],
                RawData.shopping: [int(data['shopping'])],
                RawData.spa: [int(data['spa'])],
                RawData.vrdeck: [int(data['vrdeck'])]
            })
        except TypeError:
            raise PreventUpdate

        return RawData.validate(df)

