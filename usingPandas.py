import pandas as pd
import json

def convert_to_dataframe(data:json ) -> pd.DataFrame:
    df = pd.DataFrame(data["data"])
    return df

