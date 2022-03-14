import pandas as pd



def my_pipeline(arg_dict: dict, df: pd.DataFrame) -> pd.DataFrame:
    for T, cols in zip(arg_dict.keys(), arg_dict.values()):
        transformer = T(cols, df)
        df = transformer.get_transformed_df()
    
    return df