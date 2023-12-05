import os
import sqlite3
import unittest
import pandas as pd

from etl.load import loader
from pipeline_utils.utils import get_directory_absolute_path


class TestLoader(unittest.TestCase):
    def setUp(self) -> None:
        self.db_name = "test_db"
        self.table_name = "test_table"
        cwd = get_directory_absolute_path()
        self.db_path = f"{cwd}/data/{self.db_name}.sqlite"

    def test_merge_data_to_sql(self):
        mock_data_1 = pd.DataFrame(
            {
                "geo": ["A", "B"],
                "TIME_PERIOD": [2023, 2022],
                "D1": [1, 2],
            }
        )
        mock_data_2 = pd.DataFrame(
            {
                "geo": ["A", "B"],
                "TIME_PERIOD": [2023, 2010],
                "D2": [3, 4],
            }
        )
        mock_data_3 = pd.DataFrame(
            {
                "geo": ["A", "B"],
                "TIME_PERIOD": [2023, 2029],
                "D3": [5, 6],
            }
        )

        expected_result = pd.DataFrame(
            {
                "geo": ["A"],
                "TIME_PERIOD": [2023],
                "D1": [1],
                "D2": [3],
                "D3": [5],
            },
        )

        result = loader.merge_data_to_sql(
            sdg_data=mock_data_1,
            road_data=mock_data_2,
            tran_data=mock_data_3,
        )
        # The extra columns are deleted and are DFs are merged
        pd.testing.assert_frame_equal(result, expected_result, check_like=True)

    def test_load_data_to_sql(self):
        mock_data = pd.DataFrame({"geo": ["A", "B"], "TIME_PERIOD": [2023, 2022]})
        loader.load_data_to_sql(
            data_frame=mock_data,
            db_name=self.db_name,
            table_name=self.table_name,
        )
        self.assertTrue(os.path.exists(self.db_path))

    def test_correct_data_in_sql(self):
        mock_data = pd.DataFrame({"geo": ["A", "B"], "TIME_PERIOD": [2023, 2022]})
        loader.load_data_to_sql(
            data_frame=mock_data,
            db_name=self.db_name,
            table_name=self.table_name,
        )
        expected_result = pd.DataFrame({"geo": ["A", "B"], "TIME_PERIOD": [2023, 2022]})
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM {self.table_name}"
        result = pd.read_sql_query(query, conn)
        pd.testing.assert_frame_equal(result, expected_result, check_like=True)
        conn.commit()
        conn.close()

    def tearDown(self) -> None:
        if os.path.exists(self.db_path):
            os.remove(self.db_path)


if __name__ == "__main__":
    unittest.main()
