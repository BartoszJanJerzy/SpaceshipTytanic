import pandas as pd
from .my_transformer import MyTransformer



class BoolTransformer(MyTransformer):
    def __init__(self, cols: list, df: pd.DataFrame):
        super().__init__(df, cols)
        self.methods_to_run = [self.to_bool]

    def to_bool(self) -> None:
        for col in self.cols:
            self.df[col].apply(lambda x: 1 if x  else 0)
            self.df[col] = self.df[col].astype(int)