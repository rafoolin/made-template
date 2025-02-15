import pandas as pd
from pipeline_utils.zip_helper import GZipFileHelper


def geo_data_extractor(compressed=True):
    """
    Extracts geographic data from the data source URL. This is an abbr mapper to its meaning.

    Parameters:
    - compressed (bool, optional): Flag indicating whether the file is compressed. Both are possible from the data provider.
      When True (default), the function assumes the file is compressed and uses GZip decompression.
      When False, the file is assumed to be uncompressed.

    Returns:
    - DataFrame: A DataFrame containing the extracted data.
    """
    zip_helper = GZipFileHelper()
    url = f"https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/codelist/ESTAT/GEO/?compressed={compressed}&format=TSV&lang=en"
    tsv_file_path = zip_helper.download_and_extract_url_file(url)
    return pd.read_csv(tsv_file_path, sep="\t", header=0, names=['abbr', 'geo_full_name'])
