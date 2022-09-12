import dash_bootstrap_components as dbc
import base64
import os

# colors
dark_gray = 'rgb(41, 50, 65)'
orange = 'rgb(238, 108, 77)'
blue_1 = 'rgb(224, 251, 252)'
blue_2 = 'rgb(152, 193, 217)'
blue_3 = 'rgb(61, 90, 128)'


external_stylesheets = [
    {
        'href': 'https://kit.fontawesome.com/607ca086f9.js',
        'rel': 'stylesheet',
        'integrity': 'sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
        'crossorigin': 'anonymous'
    },
    {
        'rel':'preconnect',
        'href':'https://fonts.gstatic.com'
    },
    {
        'href':'"https://fonts.googleapis.com/css2?family=Montserrat:wght@100&display=swap',
        'rel':'stylesheet'
    },
    dbc.themes.BOOTSTRAP
]


# classes
flex_div = 'flex-div'


background_path = os.path.join(
    os.getcwd(),
    'assets',
    'background.png'
)
encoded_background = base64.b64encode(open(background_path ,"rb").read())

style={
    'background-image': f'url(data:image/png;base64,{encoded_background.decode()}',
    'background-repeat':'no-repeat',
    'background-attachment':'fixed',
    'background-height':'100%'
}