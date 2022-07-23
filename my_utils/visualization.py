import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go



def show_cat_feature(col, df):
    unique_values = df[col].nunique()
    df_graph = df[col].value_counts().reset_index()
    
    fig = px.bar(
        df_graph,
        x = 'index',
        y = col,
    )
    fig.update_layout(
        title = f'Frequencies of {col} ({unique_values} unique values)',
        xaxis_title = col,
        yaxis_title = None,
        width = 700,
        height = 300
    )
    fig.show(renderer='notebook')


def show_histogram(col: str, df: pd.DataFrame):
    fig = px.histogram(
        df,
        x = col
    )
    fig.update_layout(
        title = f'Histogram of {col}',
        width = 700,
        height = 400,
    )
    fig.show(render='notebook')

    
def show_log_transform(df: pd.DataFrame, col: str):
    df_graph = df[col].apply(lambda x: np.log(x) if x>0 else x)
    show_histogram(col, df_graph)


def show_segments(df: pd.DataFrame, colors: list, cols: list, height: int):
    fig = go.Figure()

    for i in range(3):
        fig.add_trace(go.Bar(
            name = i,
            x = df.loc[i][1:],
            y = cols,
            orientation = 'h',
            marker_color = colors[i]
        ))


    fig.update_layout(
        title = 'Segments visualization',
        height = height
    )

    fig.show(render='notebook')


def get_3d_ensemble_fig(
    df: pd.DataFrame,
    x: str = 'ada_boost',
    y: str ='svc',
    z: str ='lgbm',
    color: str ='y',
    marker_size: int =3,
    height: int =900
):
    fig = px.scatter_3d( df, x=x, y=y, z=z, color=color)
    fig.update_traces(marker_size=marker_size)
    fig.update_layout(height=height)
    return fig


def show_history_graph(df: pd.DataFrame, trace1: str, trace2: str):
    trace1_data = df[trace1].to_list()
    trace2_data = df[trace2].to_list()
    x = df.index

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        name=trace1,
        x=x,
        y=trace1_data,
        mode='lines'
    ))
    fig.add_trace(go.Scatter(
        name=trace2,
        x=x,
        y=trace2_data,
        mode='lines',
        line_dash='dot'
    ))
    fig.update_yaxes(range=(0,1))
    fig.update_layout(
        title=f'{trace1} and {trace2}',
        width=700,
        height=500
    )
    fig.show()


def show_ensemble_features(df: pd.DataFrame, feature_names: list, data_type):
    data = df.sort_values('y', ignore_index=True)
    x = data.index

    fig = go.Figure()
    fig.add_trace(go.Scattergl(
        name='Target',
        x=x,
        y=data['y'],
        mode='markers'
    ))

    for feature in feature_names:
        fig.add_trace(go.Scattergl(
            name=feature,
            x=x,
            y=data[feature],
            mode='markers',
            marker=dict(size=2)
        ))
    
    fig.add_hline(
        y=0.5,
        line_dash='dash',
        line_color='black',
        annotation_text='0.5'
    )
    fig.update_layout(
        title=f'Target and proabs from models for {data_type} data',
        height=700
    )
    fig.show()