import unittest
import pandas as pd

from etl.transform.road_eqr_carpda_transformer import road_eqr_carpda_data_transformer


class TestRoadTransformer(unittest.TestCase):
    def test_road_eqr_carpda_data_transformer(self) -> None:
        mock_csv_data = pd.DataFrame(
            {
                "DATAFLOW": [1, 2, 3],
                "LAST UPDATE": [1, 2, 3],
                "OBS_VALUE": ["1", "2", "3"],
                "freq": ["a", "a", "b"],
                "unit": ["NR", "NR", "C"],
            }
        )
        expected_result = pd.DataFrame(
            {
                "n_passenger_cars": [1, 2],
            }
        )
        result = road_eqr_carpda_data_transformer(mock_csv_data)
        # The extra columns are deleted
        pd.testing.assert_frame_equal(result, expected_result, check_like=True)

    def test_road_eqr_carpda_data_transformer_empty(self) -> None:
        mock_csv_data = pd.DataFrame(
            {
                "DATAFLOW": [1, 2, 3],
                "LAST UPDATE": [1, 2, 3],
                "OBS_VALUE": ["1", "2", "3"],
                "freq": ["c", "b", "b"],
                "unit": ["A", "B", "C"],
            }
        )
        result = road_eqr_carpda_data_transformer(mock_csv_data)
        # The extra columns are deleted
        # We don't have any annual row in the data-frame
        self.assertTrue(
            result.empty,
            msg='Only annual data is valid on the "freq" column',
        )


if __name__ == "__main__":
    unittest.main()
