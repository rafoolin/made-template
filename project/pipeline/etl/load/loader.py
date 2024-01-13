import sqlite3
import pandas as pd
import pipeline_utils.utils as util


def merge_data_to_sql(sdg_data, road_data) -> pd.DataFrame:
    """
    Merge data from different sources into a single Pandas DataFrame.

    Parameters:
    - sdg_data (pd.DataFrame): DataFrame containing average CO2 emissions per km from new passenger cars.
    - road_data (pd.DataFrame): New passenger cars by type of motor energy.
    Returns:
    pd.DataFrame: Merged DataFrame containing data from all three sources.
    """
    # Merge based on the time and country code
    merge_on = ["geo", "TIME_PERIOD"]
    merged_data = pd.merge(sdg_data, road_data, on=merge_on, how="inner")
    return merged_data.dropna()


def load_data_to_sql(data_frame: pd.DataFrame, db_name, table_name) -> None:
    """
    Load data to \\data directory and create a SQLITE file.
    """
    cwd = util.get_directory_absolute_path()
    path = f"{cwd}/data/{db_name}.sqlite"
    conn = sqlite3.connect(path)
    data_frame.to_sql(f"{table_name}", conn, index=False, if_exists="replace")
    conn.commit()
    conn.close()
