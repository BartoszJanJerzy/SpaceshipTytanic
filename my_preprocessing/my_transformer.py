import pandas as pd



class MyTransformer:
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