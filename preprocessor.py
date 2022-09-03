import pandas as pd
from data_validation import RawData


class Preprocessor:

    BOOL_COLS = ["is_g734s", "CryoSleep", "VIP", "Europa", "Mars", "PSO J318.5-22", "TRAPPIST-1e"]
    COLS_TO_NORMALIZE = ['Age', 'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']

    def __init__(
        self,
        raw_data: pd.DataFrame,
        means_dict: dict,
        std_dict: dict
    ):
        self.raw_data = RawData.validate(raw_data)
        self.means_dict = means_dict
        self.std_dict = std_dict
        self.preprocessed_data = self.raw_data.copy()

    def get_data(self):
        self._to_int_01()
        self._normalize()

        return self.preprocessed_data

    def _to_int_01(self):
        for col in self.BOOL_COLS:
            self.preprocessed_data[col] = self.preprocessed_data[col].apply(lambda x: int(x))
    
    def _normalize(self):
        for col in self.COLS_TO_NORMALIZE:
            self.preprocessed_data[col] = (self.preprocessed_data[col] - self.means_dict[col]) / self.std_dict[col]
