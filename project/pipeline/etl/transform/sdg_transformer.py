import pandas as pd


def sdg_data_transformer(data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Clean data frame of average CO2 emissions per km from new passenger cars data.

    Parameters:
    - dataFrame (pd.DataFrame): The raw data for average CO2 emissions per km from new passenger cars
    Returns:
    - pd.DataFrame: Cleaned data
    """
    # Dropping some columns we do not need
    to_drop = ["DATAFLOW", "LAST UPDATE", "OBS_FLAG"]
    to_drop_filter = data_frame.filter(to_drop)
    data_frame.drop(to_drop_filter, axis=1, inplace=True)
    # Filter and drop rows that its frequency(freq) is not A|a.
    # This means we only consider annual frequencies!
    if "freq" in data_frame.columns:
        frame_filter = data_frame["freq"].str.contains("A", case=False) == False
        data_frame = data_frame[~frame_filter]
        # Now that rows are filtered, we drop the column
        data_frame = data_frame.drop(["freq"], axis=1)
    data_frame.dropna(inplace=True)
    if "OBS_VALUE" in data_frame.columns:
        # Convert [OBS_VALUE] to [int] values
        data_frame["OBS_VALUE"] = data_frame["OBS_VALUE"].astype(int)
        data_frame.rename({"OBS_VALUE": "emitted_co2"}, axis=1, inplace=True)

    if "TIME_PERIOD" in data_frame.columns:
        # Convert [TIME_PERIOD] to [datetime] values
        data_frame["TIME_PERIOD"] = data_frame["TIME_PERIOD"].astype(str)
        data_frame["TIME_PERIOD"] = pd.to_datetime(data_frame["TIME_PERIOD"], format='%Y')
    # Reset indexes after changing and dropping rows
    data_frame = data_frame.reset_index(drop=True)
    return data_frame
