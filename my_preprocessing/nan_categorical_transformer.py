import pandas as pd
import numpy as np
from .my_transformer import MyTransformer



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