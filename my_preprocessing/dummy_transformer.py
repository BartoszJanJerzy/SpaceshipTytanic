import pandas as pd
from .my_transformer import MyTransformer



class DummyTransformer(MyTransformer):
    def __init__(self, cols: list, df: pd.DataFrame):
        super().__init__(df, cols)
        self.methods_to_run = [self.my_get_dummies]
        
    def my_get_dummies(self) -> None:
        for col in self.cols:
            dummy_df = pd.get_dummies(self.df[col], drop_first=True)
            frames = [self.df, dummy_df]
            self.df = pd.concat(frames, axis=1)