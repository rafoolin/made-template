import pandas as pd


def tran_r_vehst_data_transformer(dataFrame: pd.DataFrame) -> pd.DataFrame:
    """
    Clean data frame of stock of vehicles by category and NUTS 2 regions data.

    Parameters:
    - dataFrame (pd.DataFrame): The raw data for stock of vehicles by category and NUTS 2 regions
    Returns:
    - pd.DataFrame: Cleaned data
    """
    # Dropping some columns we do not need
    to_drop = ["DATAFLOW", "LAST UPDATE", "OBS_FLAG"]
    dataFrame = dataFrame.drop(to_drop, axis=1)
    # Filter and drop rows that its frequency(freq) is not A|a.
    # This means we only consider annual frequencies!
    filter = dataFrame["freq"].str.contains(r"[A|a]") == False
    dataFrame = dataFrame[~filter]
    # Now that rows are filtered, we drop the column
    dataFrame = dataFrame.drop(["freq"], axis=1)
    # Drop [vehicles] other than [CAR]
    filter = dataFrame["vehicle"].str.contains("CAR") == False
    dataFrame = dataFrame[~filter]
    dataFrame = dataFrame.dropna()
    # Drop vehicle column
    dataFrame = dataFrame.drop(["vehicle"], axis=1)
    # Convert [OBS_VALUE] to contains [int] values
    dataFrame["OBS_VALUE"] = dataFrame["OBS_VALUE"].astype(int)
    dataFrame = dataFrame.rename({"OBS_VALUE": "n_vehicles"}, axis=1)
    dataFrame = dataFrame.rename({"unit": "vehicles_unit"}, axis=1)
    return dataFrame
