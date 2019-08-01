def volatilty_ASTM_df_creator(routine_csv, ASTM_csv):
    """Takes in the original csvs including the path names as strings for the results and ASTM standards

        Keyword arguments:
        routine_csv -- the name of the csv where all of the annual results are saved,
        cursor -- the name of the csv where all of the ASTM results are saved
    """

    volatility_df = pd.read_csv(routine_csv)
    volatility_df['DateSampled'] = pd.to_datetime(volatility_df.DateSampled).apply(lambda x: x.date())
    volatility_df = volatility_df.set_index(volatility_df.DateSampled)
