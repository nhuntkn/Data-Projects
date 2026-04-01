import pandas as pd
import numpy as np

if 'transformer' not in globals():

    from mage_ai.data_preparation.decorators import transformer

if 'test' not in globals():

    from mage_ai.data_preparation.decorators import test


@transformer

def transform(df, *args, **kwargs):

    df = df.head(20000)

    # 1. Create "Time of day" column

    df['Time'] = df['Time'].str.strip()

    temp_dt = pd.to_datetime(df['Time'], format = '%H:%M:%S', errors = 'coerce')
    time_hour = temp_dt.dt.hour

    time_bins = [0, 6, 9, 15, 18, 24]
    labels = ['Late Night', 'Morning Peak', 'Midday', 'Afternoon Peak', 'Evening']

    df['Time of Day'] = pd.cut(time_hour, bins = time_bins, labels = labels, right = False)
    
    # 2. Convert Time into datetime type

    df['Time'] = temp_dt.dt.strftime('%H:%M:%S')


    # 3. Handle the '-9' as missing/unknown values

    involvement_cols = ['Bus Involvement',

                    'Heavy Rigid Truck Involvement',

                    'Articulated Truck Involvement']



    for col in involvement_cols:

        #Convert to string first to ensure matching

        df[col] = df[col].str.strip()

        #Replace -9 with Unknown

        df[col] = df[col].replace('-9', 'Unknown')



    number_cols = ['Age', 'Speed Limit']



    for col in number_cols:

        df[col] = df[col].replace(-9, np.nan)



    # 4. Remove rows where every single column is the same



    df = df.drop_duplicates()



    # 5. Create "Holiday Flag" and "Weekend Flag" columns

    #uses Y/N as values to indicate if the crash happened on holiday



    df['Holiday Flag'] = df.apply(lambda x : 'Y'

                              if str(x['Christmas Period']).lower() == 'yes'

                              or str(x['Easter Period']).lower() == 'yes'

                              else 'N', axis = 1)

    df['Weekend Flag'] = df.apply(lambda x: 'Y'

                              if str(x['Dayweek']).lower() == 'saturday'

                              or str(x['Dayweek']).lower() == 'sunday'

                              else 'N', axis = 1)



    # 6. Create "Age Group" column

    bins = [0, 16, 25, 39, 59, 74, 120]

    labels = ['0-15', '16-24', '25-39', '40-59', '60-74', '75+']



    df['Age Group'] = pd.cut(df['Age'], bins = bins, labels = labels, right = True)



    # 7. Create dimension tables

    dim_date = df[['Month', 'Year', 'Time', 'Time of Day', 'Holiday Flag', 'Weekend Flag']].drop_duplicates().reset_index(drop = True)
    dim_date.insert(0, 'Date ID', dim_date.index)


    dim_location = df[['State', 'National Road Type', 'National Remoteness Areas 2021', 'SA4 Name 2021', 'National LGA Name 2021']].drop_duplicates().reset_index(drop = True)
    dim_location.insert(0, 'Location ID', dim_location.index)

    dim_person = df[['Gender', 'Age Group', 'Road User']].drop_duplicates().reset_index(drop = True)
    dim_person.insert(0, 'Person ID', dim_person.index)


    dim_scenario = df[['Crash Type', 'Speed Limit', 'Bus Involvement', 'Heavy Rigid Truck Involvement', 'Articulated Truck Involvement']].drop_duplicates().reset_index(drop = True)
    dim_scenario.insert(0, 'Scenario ID', dim_scenario.index)

    # 7. Create fact_fatalities table

    fact_fatalities = df.merge(dim_date, on = ['Month', 'Year', 'Time', 'Time of Day', 'Holiday Flag', 'Weekend Flag'], how = 'left')
    fact_fatalities = fact_fatalities.merge(dim_location, on = ['State', 'National Road Type', 'National Remoteness Areas 2021', 'SA4 Name 2021', 'National LGA Name 2021'], how = 'left')
    fact_fatalities = fact_fatalities.merge(dim_person, on = ['Gender', 'Age Group', 'Road User'], how = 'left')
    fact_fatalities = fact_fatalities.merge(dim_scenario, on = ['Crash Type', 'Speed Limit', 'Bus Involvement', 'Heavy Rigid Truck Involvement', 'Articulated Truck Involvement'], how = 'left')
    
    fact_columns = [
        'Date ID', 
        'Location ID', 
        'Person ID', 
        'Scenario ID', 
        'Crash ID',    
        'Age',          
        'Speed Limit'   
    ]

    fact_fatalities = fact_fatalities[fact_columns]
    
    tables = [dim_date, dim_location, dim_person, dim_scenario, fact_fatalities]

    # Standardize all column names: lowercase and replace spaces with underscores
    for table in tables:
        table.columns = [col.strip().lower().replace(' ', '_') for col in table.columns]


    # Return DataFrames in dictionary format using the new lowercase keys
    return {
        'dim_date': dim_date,
        'dim_location': dim_location,
        'dim_person': dim_person,
        'dim_scenario': dim_scenario,
        'fact_fatalities': fact_fatalities
    }

@test

def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'