import pandas as pd
import glob
import functools
import numpy as np

def concatenate_and_save_intermediate_files(file_name_pattern, new_csv_name):

    """
    Summary:
    Loads multiple datasets from 01_raw folder with matching name pattern and saves concatenated
    file to 02_intermediate folder.

    Parameters:

    file_name_pattern (str): this is the name pattern of the files being loaded into the dataspace
    Ex: For these files in 01_raw folder (data_1.csv, data_2.csv, data_3.csv), the file_name_pattern would
    be data_*

    new_csv_name (str): name of new csv document. Ex: df_new

    Returns:
    CSV - new concatenated CSV is saved to 02_intermediate folder

    """

    df = pd.concat([pd.read_csv(f, skiprows = 2) for f in glob.glob('../../data/01_raw/{}.csv'.format(file_name_pattern))])
    return df.to_csv('../../data/02_intermediate/{}.csv'.format(new_csv_name), index=False)

def clean_dataset_intermediate_1(routine):

    routine.dropna(subset=['Prod'], inplace=True)
    routine['DateSampled'] = pd.to_datetime(routine['DateSampled'])
    routine['DateSampled'] = pd.DatetimeIndex(routine['DateSampled']).normalize()
    routine.drop(['DateTested'], axis=1, inplace=True)
    routine.drop(['HSID'], axis=1, inplace=True)
    routine.drop(['Gallons'], axis=1, inplace=True)
    routine.dropna(subset=['FacilityName'], inplace=True)
    routine['Compliance'] = routine['Compliance'].str.replace(' ', 'None')
    routine['Compliance'] = routine['Compliance'].str.replace('Select', 'None')
    routine['Compliance'] = routine['Compliance'].replace(np.nan, 'None')

    return routine

def clean_dataset_intermediate_2(dataframe):
    dataframe = dataframe.loc[dataframe['Prod']=='Gasoline']

    dataframe = dataframe.loc[(dataframe['Compliance']=='Y')
                                       |(dataframe['Compliance']=='N')]
    dataframe['DateSampled'] = pd.to_datetime(dataframe['DateSampled'])
    # Let's reduce the number of tests to the three that we are interested in testing
    dataframe = dataframe.loc[(dataframe['Test']=='Distillation 50%')
                            | (dataframe['Test']=='Vapor Pressure')
                            | (dataframe['Test']=='Vapor-Liquid Ratio')]
    # Let's keep the first duplicates
    dataframe.drop_duplicates(inplace=True)
    dataframe.reset_index(drop=True, inplace=True)
    # create multilevel index
    dataframe.set_index(['Sample', 'Test'], inplace=True)
    # unstack on the inner undex (test)
    dataframe = dataframe.unstack(level=1)

    prod = dataframe['Prod']
    # let's create a dataframe for each product
    prod.drop(['Distillation 50%', 'Vapor Pressure'], inplace=True, axis=1)
    prod.reset_index(inplace=True)
    prod.rename(columns={'Vapor-Liquid Ratio':'prod'}, inplace=True)

    datesampled = dataframe['DateSampled']
    datesampled.drop(['Distillation 50%', 'Vapor Pressure'], inplace=True, axis=1)
    datesampled.reset_index(inplace=True)
    datesampled.rename(columns={'Vapor-Liquid Ratio':'datesampled'}, inplace=True)

    grade = dataframe['Grade']

    grade.drop(['Distillation 50%', 'Vapor Pressure'], inplace=True, axis=1)
    grade.reset_index(inplace=True)
    grade.rename(columns={'Vapor-Liquid Ratio':'grade'}, inplace=True)

    supplier = dataframe['Supplier']

    supplier.drop(['Distillation 50%', 'Vapor Pressure'], inplace=True, axis=1)
    supplier.reset_index(inplace=True)
    supplier.rename(columns={'Vapor-Liquid Ratio':'supplier'}, inplace=True)

    facilityname = dataframe['FacilityName']

    facilityname.drop(['Distillation 50%', 'Vapor Pressure'], inplace=True, axis=1)
    facilityname.reset_index(inplace=True)
    facilityname.rename(columns={'Vapor-Liquid Ratio':'facilityname'}, inplace=True)

    siteaddress = dataframe['SiteAddress']

    siteaddress.drop(['Distillation 50%', 'Vapor Pressure'], inplace=True, axis=1)
    siteaddress.reset_index(inplace=True)
    siteaddress.rename(columns={'Vapor-Liquid Ratio':'siteaddress'}, inplace=True)

    units = dataframe['Units']
    units.reset_index(inplace=True)
    units.rename(
        columns={'Distillation 50%':'units_dist_50',
                 'Vapor Pressure':'units_vap_pressure',
                 'Vapor-Liquid Ratio':'units_vap_liq_pressure'}, inplace=True)

    method = dataframe['Method']

    method.reset_index(inplace=True)
    method.rename(
        columns={'Distillation 50%':'method_dist_50',
                 'Vapor Pressure':'method_vap_pressure',
                 'Vapor-Liquid Ratio':'method_vap_liq_pressure'}, inplace=True)

    result = dataframe['Result']

    result.reset_index(inplace=True)
    result.rename(
        columns={'Distillation 50%':'result_dist_50',
                 'Vapor Pressure':'result_vap_pressure',
                 'Vapor-Liquid Ratio':'result_vap_liq_pressure'}, inplace=True)

    minresults = dataframe['MinResult']

    minresults.reset_index(inplace=True)
    minresults.rename(
        columns={'Distillation 50%':'minresults_dist_50',
                 'Vapor Pressure':'minresults_vap_pressure',
                 'Vapor-Liquid Ratio':'minresults_vap_liq_pressure'}, inplace=True)

    maxresults = dataframe['MaxResult']

    maxresults.reset_index(inplace=True)
    maxresults.rename(
        columns={'Distillation 50%':'maxresults_dist_50',
                 'Vapor Pressure':'maxresults_vap_pressure',
                 'Vapor-Liquid Ratio':'maxresults_vap_liq_pressure'}, inplace=True)

    compliance = dataframe['Compliance']

    compliance.reset_index(inplace=True)
    compliance.rename(
        columns={'Distillation 50%':'compliance_dist_50',
                 'Vapor Pressure':'compliance_vap_pressure',
                 'Vapor-Liquid Ratio':'compliance_vap_liq_pressure'}, inplace=True)

    df = [prod, datesampled, grade, supplier, facilityname,
                   siteaddress, units, method, result, minresults, maxresults, compliance]

    df_merged = functools.reduce(lambda  left,right: pd.merge(left,right,on=['Sample'],
                                                how='outer'), df)

    return df_merged
