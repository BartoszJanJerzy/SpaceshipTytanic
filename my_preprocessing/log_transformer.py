import pandas as pd
import numpy as np
from .my_transformer import MyTransformer



class LogTransformer(MyTransformer):
    def __init__(self, cols: list, df: pd.DataFrame):
        super().__init__(df, cols)
        self.methods_to_run = [self.log_transform]
    
    def log_transform(self):
        for col in self.cols:
            self.df[col] = self.df[col].apply(lambda x: np.log(x) if x>0 else x)