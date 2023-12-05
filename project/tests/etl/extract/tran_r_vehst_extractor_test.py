import unittest
from unittest.mock import patch
import pandas as pd

from pipeline_utils.zip_helper import GZipFileHelper
from etl.extract.tran_r_vehst_extractor import tran_r_vehst_data_extractor


class TestTranDataExtractor(unittest.TestCase):
    @patch.object(GZipFileHelper, "download_and_extract_url_file")
    @patch("pandas.read_csv")
    def test_sdg_extractor(self, mock_read_csv, mock_zip_helper):
        mock_zip_helper.return_value = "tran_file.csv"
        mock_csv_data = pd.DataFrame({"C1": [1, 2], "C2": [3, 4]})
        mock_read_csv.return_value = mock_csv_data
        # Call the tran_extractor with compressed=True
        result = tran_r_vehst_data_extractor(compressed=False)
        path = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/tran_r_vehst/?format=SDMX-CSV&compressed=False"
        mock_zip_helper.assert_called_once_with(path)
        mock_read_csv.assert_called_once_with("tran_file.csv")
        self.assertTrue(result.equals(mock_csv_data))


if __name__ == "__main__":
    unittest.main()
