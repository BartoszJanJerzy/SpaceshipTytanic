import dash
from assets.style import external_stylesheets
from app_pages.container import Container
from app_utils.form_callback import FormCallback

# _______________________________________________________________________
# APP
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True
)
server = app.server
container = Container()
container.prepare_page()
app.layout = container.get_page()

# _______________________________________________________________________
# CALLBACKS
FormCallback(app).run_callbacks()

if __name__ == '__main__':
    app.run_server(debug=False)
