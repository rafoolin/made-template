import pandas as pd
from etl.extract.zip_helper import GZipFileHelper


def geo_data_extractor(compressed=True):
    zip_helper = GZipFileHelper()
    url = f"https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/codelist/ESTAT/GEO/?compressed={compressed}&format=TSV&lang=en"
    tsv_file_path = zip_helper.download_and_extract_url_file(url)
    return pd.read_csv(tsv_file_path, sep='\t', header=0)


