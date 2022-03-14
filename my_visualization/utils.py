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