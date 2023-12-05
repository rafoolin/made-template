import unittest
import pandas as pd

from etl.transform.tran_r_vehst_transformer import tran_r_vehst_data_transformer


class TestTranTransformer(unittest.TestCase):
    def test_tran_r_vehst_data_transformer(self) -> None:
        mock_csv_data = pd.DataFrame(
            {
                "DATAFLOW": [1, 2, 3],
                "LAST UPDATE": [1, 2, 3],
                "OBS_VALUE": ["1", "2", "3"],
                "freq": ["a", "a", "b"],
                "unit": ["A", "B", "C"],
            }
        )
        expected_result = pd.DataFrame(
            {
                "n_vehicles": [1, 2],
                "vehicles_unit": ["A", "B"],
            }
        )
        result = tran_r_vehst_data_transformer(mock_csv_data)
        # The extra columns are deleted
        pd.testing.assert_frame_equal(result, expected_result, check_like=True)

    def test_tran_r_vehst_data_transformer_empty(self) -> None:
        mock_csv_data = pd.DataFrame(
            {
                "DATAFLOW": [1, 2, 3],
                "LAST UPDATE": [1, 2, 3],
                "OBS_VALUE": ["1", "2", "3"],
                "freq": ["c", "b", "b"],
                "unit": ["A", "B", "C"],
            }
        )
        result = tran_r_vehst_data_transformer(mock_csv_data)
        # The extra columns are deleted
        # We don't have any annual row in the data-frame
        self.assertTrue(
            result.empty,
            msg='Only annual data is valid on the "freq" column',
        )


if __name__ == "__main__":
    unittest.main()
