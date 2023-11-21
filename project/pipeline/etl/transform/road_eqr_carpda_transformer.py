import pandas as pd


def road_eqr_carpda_data_transformer(dataFrame: pd.DataFrame) -> pd.DataFrame:
    """
    Clean data frame of new passenger cars by type of motor energy data.

    Parameters:
    - dataFrame (pd.DataFrame): The raw data for new passenger cars by type of motor energy
    Returns:
    - pd.DataFrame: Cleaned data
    """
    # Dropping some columns we do not need
    to_drop = ["DATAFLOW", "LAST UPDATE", "OBS_FLAG"]
    dataFrame = dataFrame.drop(to_drop, axis=1)
    # Filter and drop rows that it's frequency(freq) is not A|a.
    # This means we only consider annual frequencies!
    filter = dataFrame["freq"].str.contains(r"[A|a]") == False
    dataFrame = dataFrame[~filter]
    # Now that rows are filtered, we drop the column
    dataFrame = dataFrame.drop(["freq"], axis=1)
    # Drop NA rows
    dataFrame = dataFrame.dropna()
    # Convert [OBS_VALUE] to contains [int] values
    dataFrame["OBS_VALUE"] = dataFrame["OBS_VALUE"].astype(int)
    dataFrame = dataFrame.rename({"OBS_VALUE": "n_passengers"}, axis=1)
    dataFrame = dataFrame.rename({"unit": "passengers_unit"}, axis=1)
    return dataFrame
