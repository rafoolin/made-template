import pandas as pd


def tran_r_vehst_data_transformer(data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Clean data frame of stock of vehicles by category and NUTS 2 regions data.

    Parameters:
    - dataFrame (pd.DataFrame): The raw data for stock of vehicles by category and NUTS 2 regions
    Returns:
    - pd.DataFrame: Cleaned data
    """
    # Dropping some columns we do not need
    to_drop = ["DATAFLOW", "LAST UPDATE", "OBS_FLAG"]
    to_drop_filter = data_frame.filter(to_drop)
    data_frame = data_frame.drop(to_drop_filter, axis=1)
    # Filter and drop rows that its frequency(freq) is not A|a.
    # This means we only consider annual frequencies!
    if "freq" in data_frame.columns:
        frame_filter = data_frame["freq"].str.contains(r"[A|a]") == False
        data_frame = data_frame[~frame_filter]
        # Now that rows are filtered, we drop the column
        data_frame = data_frame.drop(["freq"], axis=1)
    # Drop [vehicles] other than [CAR]
    if "vehicle" in data_frame.columns:
        frame_filter = data_frame["vehicle"].str.contains("CAR") == False
        data_frame = data_frame[~frame_filter]
        # Drop vehicle column
        data_frame = data_frame.drop(["vehicle"], axis=1)
    data_frame = data_frame.dropna()
    # Convert [OBS_VALUE] to contains [int] values
    if "OBS_VALUE" in data_frame.columns:
        data_frame["OBS_VALUE"] = data_frame["OBS_VALUE"].astype(int)
        data_frame = data_frame.rename({"OBS_VALUE": "n_vehicles"}, axis=1)
    if "unit" in data_frame.columns:
        data_frame = data_frame.rename({"unit": "vehicles_unit"}, axis=1)
    # Reset indexes after changing and dropping rows
    data_frame = data_frame.reset_index(drop=True)
    if "TIME_PERIOD" in data_frame.columns:
        # Convert [TIME_PERIOD] to [datetime] values
        data_frame["TIME_PERIOD"] = data_frame["TIME_PERIOD"].astype(str)
        data_frame["TIME_PERIOD"] = pd.to_datetime(data_frame["TIME_PERIOD"], format='%Y')
    # Reset indexes after changing and dropping rows
    data_frame = data_frame.reset_index(drop=True)
    return data_frame
