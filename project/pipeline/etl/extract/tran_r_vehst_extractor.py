import pandas as pd
from pipeline_utils.zip_helper import GZipFileHelper


def tran_r_vehst_data_extractor(compressed=True):
    """
    Extracts stock of vehicles by category and NUTS 2 regions data from the data source URL.

    Parameters:
    - compressed (bool, optional): Flag indicating whether the file is compressed. Both are possible from the data provider.
      When True (default), the function assumes the file is compressed and uses GZip decompression.
      When False, the file is assumed to be uncompressed.

    Returns:
    - DataFrame: A DataFrame containing the extracted data.
    """
    zip_helper = GZipFileHelper()
    url = f"https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/tran_r_vehst/?format=SDMX-CSV&compressed={compressed}"
    csv_file_path = zip_helper.download_and_extract_url_file(url)
    return pd.read_csv(csv_file_path)
