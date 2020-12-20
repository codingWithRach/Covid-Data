# FUNCTIONS RELATING TO IMPORTING THE DATA FROM THE GOVERNMENT WEBSITE AND TIDYNG IT UP

# import packages
import numpy as np
import pandas as pd

def tidy_column_names(df, col_names):
    # rename the columns to make them easier to work with
    df = df.rename( columns = col_names )

    # convert column names to lowercase 
    df.columns = map(str.lower, df.columns)

    # replace null values with zeros
    # df = df.dropna()
    df = df.fillna(0)

    return df

def get_cases_data():
    # import data from gov.uk
    df = pd.read_csv("https://coronavirus.data.gov.uk/downloads/msoa_data/MSOAs_latest.csv")

    # tidy up column names 
    col_names = {'newCasesBySpecimenDateRollingSum' : 'rollingsum', 'newCasesBySpecimenDateRollingRate':'rollingrate'}
    df = tidy_column_names(df, col_names)

    return df

def get_cases_by_age_data():
    # import data from gov.uk
    df = pd.read_csv("https://coronavirus.data.gov.uk/downloads/demographic/cases/specimenDate_ageDemographic-unstacked.csv")

    # tidy up column names 
    col_names = {}
    for col in df.columns:
        if col.startswith('newCasesBySpecimenDateRollingRate-'):
            col_names[col] = col.replace('newCasesBySpecimenDateRollingRate-', 'rollrate_')
        elif col.startswith('newCasesBySpecimenDateRollingSum-'):
            col_names[col] = col.replace('newCasesBySpecimenDateRollingSum-', 'rollsum_')
        elif col.startswith('newCasesBySpecimenDate-'):
            col_names[col] = col.replace('newCasesBySpecimenDate-', '')
    df = tidy_column_names(df, col_names)

    # some of the data is junk, for example:
    # - the data in the 0 to 59 field is not always the same as that calculated by adding up all the fields in the 0 to 59 date range
    # - the data in the 90+ field is sometimes greater than that n the 60+ field, even though the latter should include the former
    # we will assume that the individual data columns are accurate, and the sums are erroneous
    # therefore, create our own date range columns by summing the individual data columns
    field_prefix = ['', 'rollsum_', 'rollrate_']
    for prefix in field_prefix:
        df[prefix + '0_49'] = df[prefix + '0_4'] + df[prefix + '5_9'] + df[prefix + '10_14'] + df[prefix + '15_19'] + df[prefix + '20_24'] + df[prefix + '25_29'] + df[prefix + '30_34'] + df[prefix + '35_39'] + df[prefix + '40_44'] + df[prefix + '45_49']
        df[prefix + '50_69'] = df[prefix + '50_54'] + df[prefix + '55_59'] + df[prefix + '60_64'] + df[prefix + '65_69']
        df[prefix + '70_89'] = df[prefix + '70_74'] + df[prefix + '75_79'] + df[prefix + '80_84'] + df[prefix + '85_89']

    return df

