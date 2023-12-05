import unittest
from unittest.mock import patch
import pandas as pd

from pipeline_utils.zip_helper import GZipFileHelper
from etl.extract.sdg_extractor import sdg_data_extractor


class TestSDGDataExtractor(unittest.TestCase):
    @patch.object(GZipFileHelper, "download_and_extract_url_file")
    @patch("pandas.read_csv")
    def test_sdg_extractor(self, mock_read_csv, mock_zip_helper):
        mock_zip_helper.return_value = "sdg_file.csv"
        mock_csv_data = pd.DataFrame({"C1": [1, 2], "C2": [3, 4]})
        mock_read_csv.return_value = mock_csv_data
        # Call the sdg_extractor with compressed=True
        result = sdg_data_extractor(compressed=False)
        path = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/sdg_12_30/?format=SDMX-CSV&compressed=False"
        mock_zip_helper.assert_called_once_with(path)
        mock_read_csv.assert_called_once_with("sdg_file.csv")
        self.assertTrue(result.equals(mock_csv_data))


if __name__ == "__main__":
    unittest.main()
