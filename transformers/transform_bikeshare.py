import pandas as pd
import calendar


if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, data_2, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    bikeshare_df = data_2.copy()

    bikeshare_df = bikeshare_df.drop_duplicates().reset_index(drop=True)

    def week_of_month(dt):
        year = dt.year
        month = dt.month
        day = dt.day
        cal = calendar.monthcalendar(year, month)
        week_number = (day - 1) // 7 + 1
        return week_number

    start_date = pd.to_datetime('2024-01-01')
    end_date = pd.to_datetime('2024-02-01')
    # Create a DataFrame for the date dimension
    dim_date = pd.DataFrame({'date': pd.date_range(start_date, end_date, freq='H')})
    dim_date['date_id'] = dim_date['date'].dt.strftime('%Y%m%d%H')
    dim_date['date_iso_format'] = dim_date['date'].apply(lambda x: x.isoformat())
    dim_date['year_number'] = dim_date['date'].dt.year
    dim_date['quarter_number'] = dim_date['date'].dt.quarter
    dim_date['month_number'] = dim_date['date'].dt.month
    dim_date['monthName'] = dim_date['date'].dt.strftime('%B')
    dim_date['day_number'] = dim_date['date'].dt.day
    dim_date['hour_number'] = dim_date['date'].dt.hour
    dim_date['day_Name'] = dim_date['date'].dt.strftime('%A')
    dim_date['weekofMonth'] = dim_date['date'].apply(week_of_month)
    dim_date['weekofYear'] = dim_date['date'].dt.strftime('%U')

    new_order = ['date_id', 'date_iso_format','year_number','month_number','quarter_number','day_number','hour_number','day_Name','weekofMonth','weekofYear','monthName']
    dim_date = dim_date[new_order]

    dim_bike = bikeshare_df[['bike_id', 'bike_type']].drop_duplicates().reset_index(drop=True)


    unique_catergory = bikeshare_df['trip_route_category'].unique()
    dim_category= pd.DataFrame(unique_catergory, columns= ['trip_route_category'])
    dim_category['trip_category_id'] = range(1, len(unique_catergory) + 1)
    dim_category = dim_category[['trip_category_id', 'trip_route_category']]

    unique_passholder_type = bikeshare_df['passholder_type'].unique()
    dim_passholdertype= pd.DataFrame(unique_passholder_type, columns= ['passholder_type'])
    dim_passholdertype['passholdertype_id'] = range(1, len(unique_passholder_type) + 1)
    dim_passholdertype = dim_passholdertype[['passholdertype_id', 'passholder_type']]

    station_df = data.copy()
    columnstoDrop = ['Day of Go_live_date','Unnamed: 8', 'Unnamed: 7',
                 'Unnamed: 9','Unnamed: 10','Unnamed: 11','Unnamed: 12','Unnamed: 13','Unnamed: 14','Unnamed: 15','Unnamed: 16','Unnamed: 17']
    station_df.drop(columns= columnstoDrop, inplace = True)
    new_order = ['Station_ID', 'Station_Name','Latitude','Longitude','Status']
    station_df = station_df[new_order]
    station_df = station_df.dropna()

    bikeshare_df['fact_id'] = range(1, len(bikeshare_df) + 1)
    bikeshare_df['start_time_id'] =  pd.to_datetime(bikeshare_df['start_time']).dt.strftime('%Y%m%d%H%M').astype('int64')
    bikeshare_df['end_time_id']  = pd.to_datetime(bikeshare_df['end_time']).dt.strftime('%Y%m%d%H%M').astype('int64')

    fact_bike =bikeshare_df.merge(dim_passholdertype, on='passholder_type') \
                .merge(dim_category, on='trip_route_category') \
                .merge(dim_bike, on='bike_id') \
                [['fact_id','duration', 'passholdertype_id', 'trip_category_id','bike_id','start_time_id','end_time_id','start_station','end_station']]

    new_column_names = {'start_station':'start_station_id', 'end_station': 'end_station_id'}
    fact_bike = fact_bike.rename(columns=new_column_names)
    new_order = ['fact_id', 'duration','bike_id','start_station_id','end_station_id','trip_category_id','start_time_id','end_time_id','passholdertype_id']
    fact_bike = fact_bike[new_order]
    
    return {"dim_date":dim_date.to_dict(orient="dict"),"dim_bike":dim_bike.to_dict(orient="dict"),
    "dim_category":dim_category.to_dict(orient="dict"),
    "dim_passholdertype":dim_passholdertype.to_dict(orient="dict"),
    "station_df":station_df.to_dict(orient="dict"),
    "fact_bike":fact_bike.to_dict(orient="dict")}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
