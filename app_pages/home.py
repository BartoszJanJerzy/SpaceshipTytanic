from dash import html, dcc
from assets.style import flex_div

class Home:

    def get_page(self):
        return html.Div(
            id='home',
            className=flex_div,
            children=[
                self.titles,
                self.sections
            ]
        )
    
    @property
    def titles(self):
        return html.Div(
            id='titles',
            children=[
                html.H1(
                    id='title',
                    children='Spaceship Tytanic'
                ),
                html.H2(
                    id='subtitle',
                    children='by Bartosz Wójtowicz'
                )
            ]
        )
        
    
    @property
    def subtitle(self):
        return 
    
    @property
    def sections(self):
        link_class = f'section-link {flex_div}'
        return html.Div(
            id=f'sections',
            className=flex_div,
            children=[
                html.A(
                    className=link_class,
                    id='prediction-section-link',
                    children='Get predictions!',
                    href='#prediction'
                ),
                html.A(
                    className=link_class,
                    id='code-link',
                    children='See the code',
                    href='https://github.com/BartoszJanJerzy/SpaceshipTytanic'
                ),
            ]
        )


