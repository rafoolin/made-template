import unittest
from unittest.mock import patch
import pandas as pd

from pipeline_utils.zip_helper import GZipFileHelper
from etl.extract.road_eqr_carpda_extractor import road_eqr_carpda_data_extractor


class TestRoadDataExtractor(unittest.TestCase):
    @patch.object(GZipFileHelper, "download_and_extract_url_file")
    @patch("pandas.read_csv")
    def test_road_eqr_carpda_data_extractor(self, mock_read_csv, mock_zip_helper):
        mock_zip_helper.return_value = "road_file.csv"
        mock_csv_data = pd.DataFrame({"C1": [1, 2], "C2": [3, 4]})
        mock_read_csv.return_value = mock_csv_data
        # Call the road_eqr_carpda_data_extractor with compressed=True
        result = road_eqr_carpda_data_extractor(compressed=False)
        path = f"https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/road_eqr_carpda/?format=SDMX-CSV&compressed=False"
        mock_zip_helper.assert_called_once_with(path)
        mock_read_csv.assert_called_once_with("road_file.csv")
        self.assertTrue(result.equals(mock_csv_data))


if __name__ == "__main__":
    unittest.main()
