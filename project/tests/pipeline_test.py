import os
import sqlite3
import unittest
from unittest.mock import patch
import pandas as pd
from pipeline.pipeline import Pipeline
from pipeline_utils.utils import get_directory_absolute_path


class TestPipeline(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_sdg_data = pd.DataFrame(
            {
                "DATAFLOW": [
                    "ESTAT:SDG_12_30(1.0)",
                    "ESTAT:SDG_12_30(1.0)",
                    "ESTAT:SDG_12_30(1.0)",
                    "ESTAT:SDG_12_30(1.0)",
                    "ESTAT:SDG_12_30(1.0)",
                    "ESTAT:SDG_12_30(1.0)",
                    "ESTAT:SDG_12_30(1.0)",
                ],
                "LAST UPDATE": [
                    "13/03/23 23:00:00",
                    "13/03/23 23:00:00",
                    "13/03/23 23:00:00",
                    "13/03/23 23:00:00",
                    "13/03/23 23:00:00",
                    "13/03/23 23:00:00",
                    "13/03/23 23:00:00",
                ],
                "freq": ["A", "A", "A", "A", "A", "A", "A"],
                "geo": ["AT", "AT", "AT", "AT", "AT", "AT", "AT"],
                "TIME_PERIOD": [2000, 2001, 2002, 2003, 2004, 2005, 2006],
                "OBS_VALUE": [168.0, 165.6, 164.4, 163.8, 161.9, 162.1, 163.7],
                "OBS_FLAG": ["", "", "", "", "", "", ""],
            }
        )

        self.mock_sdg_data_cleaned = pd.DataFrame(
            {
                "freq": ["A", "A", "A", "A", "A", "A", "A"],
                "geo": ["AT", "AT", "AT", "AT", "AT", "AT", "AT"],
                "TIME_PERIOD": [2000, 2001, 2002, 2003, 2004, 2005, 2006],
                "OBS_VALUE": [168.0, 165.6, 164.4, 163.8, 161.9, 162.1, 163.7],
                "OBS_FLAG": ["", "", "", "", "", "", ""],
            }
        )

        self.mock_road_data = pd.DataFrame(
            {
                "DATAFLOW": [
                    "ESTAT:SDG_12_30(1.0)",
                    "ESTAT:SDG_12_30(1.0)",
                    "ESTAT:SDG_12_30(1.0)",
                    "ESTAT:SDG_12_30(1.0)",
                    "ESTAT:SDG_12_30(1.0)",
                    "ESTAT:SDG_12_30(1.0)",
                    "ESTAT:SDG_12_30(1.0)",
                ],
                "LAST UPDATE": [
                    "13/03/23 23:00:00",
                    "13/03/23 23:00:00",
                    "13/03/23 23:00:00",
                    "13/03/23 23:00:00",
                    "13/03/23 23:00:00",
                    "13/03/23 23:00:00",
                    "13/03/23 23:00:00",
                ],
                "freq": ["A", "A", "A", "A", "A", "A", "A"],
                "unit": ["NR", "NR", "NR", "NR", "NR", "NR", "NR"],
                "mot_nrg": ["ALT", "ALT", "ALT", "ALT", "ALT", "ALT", "ALT"],
                "geo": ["AT", "AT", "AT", "AT", "AT", "AT", "AT"],
                "TIME_PERIOD": [2000, 2001, 2002, 2003, 2004, 2005, 2006],
                "OBS_VALUE": [3757, 4935, 5703, 4114, 1285, 2074, 2389],
                "OBS_FLAG": ["", "", "", "", "", "", ""],
            }
        )

        self.expected_result = pd.DataFrame(
            {
                "geo": ["AT", "AT", "AT", "AT", "AT", "AT", "AT"],
                "n_passenger_cars": [3757, 4935, 5703, 4114, 1285, 2074, 2389],
                "emitted_co2": [168, 165, 164, 163, 161, 162, 163],
                "mot_nrg": ["ALT", "ALT", "ALT", "ALT", "ALT", "ALT", "ALT"],
            }
        )
        self.db_name = "pipeline"
        self.table_name = "co2_cars"
        cwd = get_directory_absolute_path()
        self.db_path = f"{cwd}/data/{self.db_name}.sqlite"

    def test_run_pipeline(self) -> None:
        Pipeline().run_pipeline()
        self.assertTrue(os.path.exists(self.db_path))

    @patch("etl.extract.sdg_extractor.sdg_data_extractor")
    @patch("etl.extract.road_eqr_carpda_extractor.road_eqr_carpda_data_extractor")
    def test_data_after_run_pipeline(
        self,
        mock_road_extractor,
        mock_sdg_extractor,
    ) -> None:
        # Set mocks
        mock_sdg_extractor.return_value = self.mock_sdg_data
        mock_road_extractor.return_value = self.mock_road_data
        Pipeline().run_pipeline()
        # Check calls
        mock_sdg_extractor.assert_called_once()
        mock_road_extractor.assert_called_once()
        # Connection
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM {self.table_name}"
        result = pd.read_sql_query(query, conn)
        pd.testing.assert_frame_equal(
            result.drop("time_period", axis=1),
            self.expected_result,
            check_like=True,
            check_dtype=False,
        )
        conn.commit()
        conn.close()

    def tearDown(self) -> None:
        if os.path.exists(self.db_path):
            os.remove(self.db_path)


if __name__ == "__main__":
    unittest.main()
