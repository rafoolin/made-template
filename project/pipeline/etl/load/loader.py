import pandas as pd
import sqlite3


def mergeDataToSQL(sdg_data, road_data, tran_data) -> pd.DataFrame:
    # Merge based on the time and country code
    merge_on = ["geo", "TIME_PERIOD"]
    sdg_tran_data = pd.merge(sdg_data, tran_data, on=merge_on, how="inner")
    merged_data = pd.merge(road_data, sdg_tran_data, on=merge_on, how="inner")
    return merged_data.dropna()


def loadDataToSQL(data_frame: pd.DataFrame, db_name, table_name):
    import pipeline_utils.utils as util

    cwd = util.get_directory_absolute_path()
    path = f"{cwd}/data/{db_name}.sqlite"
    conn = sqlite3.connect(path)
    data_frame.to_sql(f"{table_name}", conn, index=False, if_exists="replace")
    conn.commit()
    conn.close()
