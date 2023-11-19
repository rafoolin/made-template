import pandas as pd
from etl.extract.zip_helper import GZipFileHelper


def tran_r_vehst_data_extractor(compressed=True):
    zip_helper = GZipFileHelper()
    url = f"https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/tran_r_vehst/?format=SDMX-CSV&compressed={compressed}"
    csv_file_path = zip_helper.download_and_extract_url_file(url)
    return pd.read_csv(csv_file_path)
