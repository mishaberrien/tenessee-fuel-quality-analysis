def volatilty_ASTM_df_creator(routine_csv, ASTM_csv):
    """Takes in the original csvs including the path names as strings for the results and ASTM standards. Saves the final df as 

        Keyword arguments:
        routine_csv -- the name of the csv where all of the annual results are saved,
        ASTM_csv -- the name of the csv where all of the ASTM results are saved
    """

    # Makes the routine data frame to only gasoline and the desired volatility tests
    concat_df = pd.read_csv(routine_csv)
    gasoline_df = concat_df[concat_df.Prod == 'Gasoline']
    gasoline_df.DateSampled = pd.to_datetime(gasoline_df.DateSampled)
    gasoline_date_index_df =gasoline_df.set_index(gasoline_df.DateSampled)
    volitility_df = gasoline_date_index_df[(gasoline_date_index_df.Test == 'Distillation 50%') | (gasoline_date_index_df.Test == 'Vapor Pressure') | (gasoline_date_index_df.Test == 'Vapor-Liquid Ratio')]
    volitility_df['datesampled_month'] = volitility_df['DateSampled'].dt.month
    volitility_df['datesampled_day'] = volitility_df['DateSampled'].dt.day
    volitility_df['datesampled_month_day'] = volitility_df['datesampled_month'].astype('str') + '/' + volitility_df['datesampled_day'].astype('str')
    volitility_df.rename(columns={'datesampled_month_day' : 'Date'}, inplace = True)

    # Reads in the ASTM data which was transfered from the standard to an Excel file
    ASTM_df = pd.read_csv('../../data/01_raw/ASTM_fuel.csv

    # Merge the two together
    volitility_df = volitility_df.merge(ASTM_df, how='left', on='Date')

    volitility_df.to_csv('../../data/03_processed/volatility_gas_ASTM.csv')


def date_results_df_creator(df, test):
    """Takes in the file path of the large combined gasoline and ASTM standards dataframe. It makes the dateStamp in datetime form and on the index. Also takes the test of the specific test to be made into a df

        Keyword arguments:
        df -- the string of where the combined df is stored
        test -- the name of the test results to be tracked by date
    """

    volatility_df = pd.read_csv(df)
    volatility_df['DateSampled'] = pd.to_datetime(volatility_df.DateSampled).apply(lambda x: x.date())
    volatility_df = volatility_df.set_index(volatility_df.DateSampled)
