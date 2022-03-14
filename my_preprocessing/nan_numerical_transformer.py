import pandas as pd
import numpy as np
from .my_transformer import MyTransformer



class NanNumericalTransformer(MyTransformer):
    def __init__(self, cols: list, df: pd.DataFrame):
        super().__init__(df, cols)
        self.total = len(df)
        self.methods_to_run = [self.deal_with_numerical]
    
    def deal_with_numerical(self) -> None:
        for col in self.cols:
            value = self.df[col].median()
            self.df[col].fillna(value, inplace=True)