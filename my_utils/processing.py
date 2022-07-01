import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler



class MyTransformer:
    '''
    Parent class for detail transformers
    '''
    def __init__(self, df: pd.DataFrame, cols: list):
        self.df = df
        self.cols = cols
        self.methods_to_run = []
    
    def run_methods(self):
        for method in self.methods_to_run:
            method()
    
    def get_transformed_df(self) -> pd.DataFrame:
        self.run_methods()
        
        return self.df

    
class BoolTransformer(MyTransformer):
    
    def __init__(self, cols: list, df: pd.DataFrame):
        super().__init__(df, cols)
        self.methods_to_run = [self.to_bool]

    def to_bool(self) -> None:
        for col in self.cols:
            self.df[col] = self.df[col].apply(lambda x: 1 if x  else 0)
            self.df[col] = self.df[col].astype(int)

            
class SpecialBoolTransformer(MyTransformer):
    
    def __init__(self, cols: list, df: pd.DataFrame):
        super().__init__(df, cols)
        self.methods_to_run = [self.to_bool]
        self.special_values = [['G/734/S']]
        self.new_cols = [['is_g734s']]

    def to_bool(self) -> None:
        for col, values, new_col in zip(self.cols, self.special_values, self.new_cols):
            self.df[new_col] = self.df[col].apply(lambda x: 1 if x in values else 0)
            self.df[new_col] = self.df[new_col].astype(int)

            
class DummyTransformer(MyTransformer):
    
    def __init__(self, cols: list, df: pd.DataFrame):
        super().__init__(df, cols)
        self.methods_to_run = [self.my_get_dummies]
        
    def my_get_dummies(self) -> None:
        for col in self.cols:
            dummy_df = pd.get_dummies(self.df[col], drop_first=True)
            frames = [self.df, dummy_df]
            self.df = pd.concat(frames, axis=1)


class LogTransformer(MyTransformer):
    
    def __init__(self, cols: list, df: pd.DataFrame):
        super().__init__(df, cols)
        self.methods_to_run = [self.log_transform]
    
    def log_transform(self):
        for col in self.cols:
            self.df[col] = self.df[col].apply(lambda x: np.log(x) if x>0 else x)
            
            
class NanCategoricalTransformer(MyTransformer):
    def __init__(self, cols: list, df: pd.DataFrame):
        super().__init__(df, cols)
        self.total = len(df)
        self.methods_to_run = [self.deal_with_categorical]
    
    def find_value(self, col: str) -> str:
        # 1 - Get values' frequencies
        freq_df = self.df[col].value_counts().reset_index()
        freq_df['prob'] = freq_df[col] / self.total * 100
        freq_df['prob'] = freq_df['prob'].astype(int)

        # 2 - Get ranges
        probs = freq_df['prob'].to_list()[::-1]
        prev = probs[0]
        ranges = [prev]

        for p in probs[1:]:
            r = p + prev
            ranges.append(r)
            prev = r

        ranges[len(ranges) - 1] = 100
        freq_df['ranges'] = ranges[::-1]

        # 3 - Get value
        prob_dict = freq_df[['ranges', 'index']].set_index('ranges').to_dict()['index']
        result_num = np.random.randint(0, 101)

        for prob in list(prob_dict.keys())[::-1]:
            if result_num <= prob:
                value = prob_dict[prob]
                break

        return value
    
    def deal_with_categorical(self) -> None:
        for col in self.cols:
            value = self.find_value(col)
            self.df[col].fillna(value, inplace=True)
            
            
class NanNumericalTransformer(MyTransformer):
    def __init__(self, cols: list, df: pd.DataFrame):
        super().__init__(df, cols)
        self.total = len(df)
        self.methods_to_run = [self.deal_with_numerical]
    
    def deal_with_numerical(self) -> None:
        for col in self.cols:
            value = self.df[col].median()
            self.df[col].fillna(value, inplace=True)

            
class ZTransformer(MyTransformer):
    
    def __init__(self, cols: list, df: pd.DataFrame):
        super().__init__(df, cols)
        self.methods_to_run = [self.z_transform]
    
    def z_transform(self):
        scaler = StandardScaler()
        self.df[self.cols] = scaler.fit_transform(self.df[self.cols])    

            
def my_pipeline(arg_dict: dict, df: pd.DataFrame) -> pd.DataFrame:
    '''
    arg_dict:
        - keys: transformers inherits from MyTransformer
        - values: cols to transform
    df:
        - pandas DataFrame to process
    '''
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


