from dash import html, dcc
from assets.style import flex_div, style
from pages.home import Home
from pages.prediction_form import PredictionForm

class Container:

    def __init__(self):
        self.page = html.Div()
        self.home_page: html.Div = None
        self.prediction_form_page: html.Div = None
        self.info_page: html.Div = None

    def get_page(self):
        return self.page

    def prepare_page(self):
        self.home_page = Home().get_page()
        self.prediction_form_page = PredictionForm().get_page()

        self.page = html.Div(
            id='container',
            children=[
                self.home_page,
                self.prediction_form_page,
                self.info_page
            ],
            style=style
        )