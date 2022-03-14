import pandas as pd
from sklearn.preprocessing import StandardScaler
from .my_transformer import MyTransformer



class ZTransformer(MyTransformer):
    def __init__(self, cols: list, df: pd.DataFrame):
        super().__init__(df, cols)
        self.methods_to_run = [self.z_transform]
    
    def z_transform(self):
        scaler = StandardScaler()
        self.df[self.cols] = scaler.fit_transform(self.df[self.cols])