import pandas as pd
from sklearn.cluster import KMeans



def my_pipeline(arg_dict: dict, df: pd.DataFrame) -> pd.DataFrame:
    for T, cols in zip(arg_dict.keys(), arg_dict.values()):
        transformer = T(cols, df)
        df = transformer.get_transformed_df()
    
    return df


def add_cluster_feature_train(df: pd.DataFrame, cols: list, k: int = 3) -> list:
    X = df[cols]

    kmeans = KMeans(n_clusters=3)
    kmeans.fit(X)
    y = kmeans.predict(X)
    
    return y, kmeans


def add_cluster_feature(df: pd.DataFrame, cols: list, kmeans: KMeans) -> pd.Series:
    X = df[cols]
    y = kmeans.predict(X)
    
    return y