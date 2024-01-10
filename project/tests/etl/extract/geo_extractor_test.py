import unittest
from unittest.mock import patch
import pandas as pd

from pipeline_utils.zip_helper import GZipFileHelper
from etl.extract.geo_extractor import geo_data_extractor


class TestGeoDataExtractor(unittest.TestCase):
    @patch.object(GZipFileHelper, "download_and_extract_url_file")
    @patch("pandas.read_csv")
    def test_geo_data_extractor(self, mock_read_csv, mock_zip_helper):
        mock_zip_helper.return_value = "geo_file.tsv"
        mock_csv_data = pd.DataFrame({"abbr": [1, 2], "geo_full_name": [3, 4]})
        mock_read_csv.return_value = mock_csv_data
        # Call the geo_data_extractor with compressed=True
        result = geo_data_extractor(compressed=False)
        path = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/codelist/ESTAT/GEO/?compressed=False&format=TSV&lang=en"
        mock_zip_helper.assert_called_once_with(path)
        mock_read_csv.assert_called_once_with("geo_file.tsv", sep="\t", header=0, names=['abbr', 'geo_full_name'])
        self.assertTrue(result.equals(mock_csv_data))


if __name__ == "__main__":
    unittest.main()
