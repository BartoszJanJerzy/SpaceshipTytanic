import plotly.graph_objects as go
import plotly.io as pio
from assets.style import dark_gray, blue_3



def get_probability_graph(
    data: dict = {
        'AdaBoost': 0,
        'LightGBM': 0,
        'SVC': 0, 
        'NeuralNetwork': 0,
        'MeanProbability': 0
    },
    final_proba: float = 0.0
) -> go.Figure:
    pio.templates.default = "plotly_dark"

    good_keys = ['AdaBoost', 'LightGBM', 'SVC', 'NeuralNetwork', 'MeanProbability']
    keys_to_check = list(data.keys())
    good_keys.sort()
    keys_to_check.sort()
    assert good_keys == keys_to_check

    colors = {
        'AdaBoost': 'rgb(222, 226, 230)',
        'LightGBM': 'rgb(173, 181, 189)',
        'SVC': 'rgb(108, 117, 125)', 
        'NeuralNetwork': 'rgb(73, 80, 87)',
        'MeanProbability': 'rgb(52, 58, 64)'
    }

    fig = go.Figure()

    trace = 'Final NN'
    fig.add_trace(go.Bar(
        name=trace,
        x=[trace],
        y=[round(final_proba, 2)],
        text=[round(final_proba, 2)],
        marker_color='rgb(238, 108, 77)',
    ))

    for trace, value in data.items():
        fig.add_trace(go.Bar(
            name=trace,
            x=[trace],
            y=[round(value, 2)],
            legendgroup=1,
            legendgrouptitle_text='Component models',
            width=0.5,
            marker_color=colors[trace],
            text=[round(value, 2)]
        ))

    fig.update_traces(
        marker=dict(
            line=dict(color='white')
        )
    )

    fig.update_yaxes(range=(0,1), gridcolor='rgba(255, 255, 255, 0.3)')
    fig.update_layout(
        legend=dict(groupclick="toggleitem"),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    return fig