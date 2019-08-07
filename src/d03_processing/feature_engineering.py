import pandas as pd
import numpy as np

def merge_gasoline_asm_datasets(gasoline, astm):
    # turn datasampled to datetime
    gasoline['datesampled'] = pd.to_datetime(gasoline['datesampled'])
    # strip all astm columns of any white space
    for col in astm.columns:
        try:
            astm[col] = astm[col].str.strip()
        except AttributeError:
            pass

    # drop columns
    # gasoline.drop(columns=['zipcode'], inplace=True)
    # drop na values
    gasoline.dropna(subset=['grade'], inplace=True)
    gasoline.dropna(inplace=True)

    # prepare to join ASTM dataset to gasoline_proc set
    gasoline['datesampled_month'] = gasoline['datesampled'].dt.month
    gasoline['datesampled_day'] = gasoline['datesampled'].dt.day
    gasoline['datesampled_month_day'] = gasoline['datesampled_month'].astype('str') + '/' + gasoline['datesampled_day'].astype('str')
    gasoline.rename(columns={'datesampled_month_day':'Date'}, inplace=True)

    # join ASTM and gasoline_proc datasets
    gasoline = gasoline.merge(astm,
                                        how='left',
                                        on='Date'
                                       )
    gasoline.reset_index(inplace=True, drop=True)
    return gasoline
