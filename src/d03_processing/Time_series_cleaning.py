import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

def volatilty_ASTM_df_creator(routine_csv, ASTM_csv):
    """Takes in the original csvs including the path names as strings for the results and ASTM standards. Saves the final df as volatility_gas_ASTM.csv in the processed data folder.

        Keyword arguments:
        routine_csv -- the name of the csv where all of the annual results are saved,
        ASTM_csv -- the name of the csv where all of the ASTM results are saved
    """

    # Makes the routine data frame to only gasoline and the desired volatility tests
    concat_df = pd.read_csv(routine_csv)
    gasoline_df = concat_df[concat_df.Prod == 'Gasoline']
    #print(gasoline_df.head())
    gasoline_df.DateSampled = pd.to_datetime(gasoline_df.DateSampled)
    gasoline_date_index_df = gasoline_df.set_index(gasoline_df.DateSampled)
    #
    gasoline_date_index_df[(gasoline_date_index_df.Test == 'Distillation 50%') | (gasoline_date_index_df.Test == 'Vapor Pressure') | (gasoline_date_index_df.Test == 'Vapor-Liquid Ratio')]
    #print(gasoline_date_index_df.head())
    full_volitility_df = gasoline_date_index_df.copy()
    #print(full_volitility_df.head())
    full_volitility_df['datesampled_month'] = full_volitility_df['DateSampled'].dt.month
    full_volitility_df['datesampled_day'] = full_volitility_df['DateSampled'].dt.day
    full_volitility_df['datesampled_month_day']=full_volitility_df['datesampled_month'].astype('str')+'/'+full_volitility_df['datesampled_day'].astype('str')
    full_volitility_df.rename(columns={'datesampled_month_day' : 'Date'}, inplace = True)

    #Clean up the results columns
    full_volitility_df['Results_cleaned']


    # Reads in the ASTM data which was transfered from the standard to an Excel file
    ASTM_df = pd.read_csv('../../data/01_raw/ASTM_fuel.csv')
    #ASTM_df = ASTM_df.set_index(ASTM_df.Date)
    # Merge the two together
    new_volitility_df = full_volitility_df.merge(ASTM_df, how='left', on='Date')

    # Save to csv
    # volitility_df.to_csv('../../data/03_processed/volatility_gas_ASTM_function.csv')

    return new_volitility_df


def date_results_df_creator(df, test_name):
    """Takes in the file path of the large combined gasoline and ASTM standards dataframe. It makes the dateStamp in datetime form and on the index. Also takes the test of the specific test to be made into a df. It also takes the test specific limits to eliminate any outliers most likely caused by data entry errors.

        Keyword arguments:
        df -- the string of where the combined df is stored
        test_name -- the name of the test results to be tracked by date
    """

    volatility_df = df.copy()
    volatility_df['DateSampled'] = pd.to_datetime(volatility_df.DateSampled).apply(lambda x: x.date())
    volatility_df = volatility_df.set_index(volatility_df.DateSampled)
    volatility_results_df = volatility_df[['Test','Result']]
    volatility_results_df['Result'] = volatility_results_df.Result.replace('  ', np.nan)
    volatility_results_df['Result'] = volatility_results_df.Result.replace(' ', np.nan)
    volatility_results_df['Result'] = volatility_results_df.Result.replace('', np.nan)
    volatility_results_df = volatility_results_df.dropna()
    volatility_results_df['temp'] = volatility_results_df.Result.astype('float')
    volatility_results_df.drop('Result', axis=1, inplace = True)
    volatility_results_floats_df = volatility_results_df.dropna()

    test_df = volatility_results_floats_df[volatility_results_floats_df.Test == test_name]
    test_df.rename(columns={"temp": "Result_deg_C"}, inplace = True)
    testing_df = test_df.drop(columns=['Test'])

    if test_name == 'Distillation 50%':
        testing_df = testing_df[testing_df.Result_deg_C <= 225]
    elif test_name == 'Vapor-Liquid Ratio':
        testing_df = testing_df[(testing_df.Result_deg_C < 150) & (testing_df.Result_deg_C > 30)]
    elif test_name == 'Vapor Pressure':
        testing_df = testing_df[testing_df.Result_deg_C < 175]
    else:
        print('not a valid volaitlity test name')

    return testing_df

def stationarity_check(TS, title):
    """Takes in a data frame and a title for a graph. The function will tell the user if the time series is stationary with the Dicky-Fuller test. It gives the F-score and critical values.

        Keyword arguments:
        TS -- a dataframe where the index is Timeseries and there is only one more numerical column besides the index
        title -- a string of what the title of the graph should be
    """

    # Calculate rolling statistics
    rolmean = TS.rolling(window = 8, center = False).mean()
    rolstd = TS.rolling(window = 8, center = False).std()

    # Perform the Dickey Fuller Test
    dftest = adfuller(TS['Result_deg_C']) # change the passengers column as required

    #Plot rolling statistics:
    fig = plt.figure(figsize=(12,6))
    orig = plt.plot(TS, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title(title)
    plt.savefig(f'../../results/Images/{title}.png')
    plt.show(block=False)


    # Print Dickey-Fuller test results
    print ('Results of Dickey-Fuller Test:')

    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print (dfoutput)

    return None

def seasonal_decomp_graphs(df, title):
    """Takes in a data frame and a title for a graph. The function will give a graph of the time series and decompose it into its trend, seasonality, and noise. Then graph all 4 components

        Keyword arguments:
        df -- a dataframe where the index is Timeseries and there is only one more numerical column besides the index. It must have a frequency specified and have no empty or null values. Upsample or downsample to fill in empty date values.
        title -- a string of what the title of the graph should be
    """
    # Get the frequency set up to buisness days
    dated_vapor = pd.DataFrame(df)
    dated_vapor.index = pd.to_datetime(dated_vapor.index, format = '%Y/%m/%d')
    dated_vapor = dated_vapor.asfreq('d')
    resampled_vapor_pessure = dated_vapor.resample(rule = 'B')
    resampled_vapor_pessure = resampled_vapor_pessure.fillna(method = 'pad')
    resampled_vapor_pessure.dropna(inplace=True)

    # Gather the trend, seasonality and noise of decomposed object

    decomposition = seasonal_decompose(df, freq = 260)
    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid

    # Plot gathered statistics
    plt.figure(figsize=(12,8))
    plt.subplot(411)
    plt.title(title)
    plt.plot(Vapor_Pressure.groupby('DateSampled').max() , label='Original', color="blue")
    plt.legend(loc='best')

    plt.subplot(412)
    plt.plot(trend, label='Trend', color="blue")
    plt.legend(loc='best')

    plt.subplot(413)
    plt.plot(seasonal,label='Seasonality', color="blue")
    plt.legend(loc='best')

    plt.subplot(414)
    plt.plot(residual, label='Residuals', color="blue")
    plt.legend(loc='best')

    plt.tight_layout()
