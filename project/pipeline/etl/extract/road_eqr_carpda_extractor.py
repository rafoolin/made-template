import pandas as pd
from pipeline_utils.zip_helper import GZipFileHelper


def road_eqr_carpda_data_extractor(compressed=True):
    zip_helper = GZipFileHelper()
    url = f"https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/road_eqr_carpda/?format=SDMX-CSV&compressed={compressed}"
    csv_file_path = zip_helper.download_and_extract_url_file(url)
    return pd.read_csv(csv_file_path)
