import unittest
import pandas as pd

from etl.transform.sdg_transformer import sdg_data_transformer


class TestSdgTransformer(unittest.TestCase):
    def test_sdg_data_transformer(self):
        mock_csv_data = pd.DataFrame(
            {
                "DATAFLOW": [1, 2, 3],
                "LAST UPDATE": [1, 2, 3],
                "OBS_VALUE": [1, 2, 3],
                "freq": ["a", "a", "b"],
            }
        )
        expected_result = pd.DataFrame({"emitted_co2": [1, 2]})
        result = sdg_data_transformer(mock_csv_data)
        # The extra columns are deleted
        pd.testing.assert_frame_equal(result, expected_result, check_like=True)

    def test_sdg_data_transformer_empty(self):
        mock_csv_data = pd.DataFrame(
            {
                "DATAFLOW": [1, 2, 3],
                "LAST UPDATE": [1, 2, 3],
                "OBS_VALUE": [1, 2, 3],
                "freq": ["c", "b", "b"],
            }
        )
        result = sdg_data_transformer(mock_csv_data)
        # The extra columns are deleted
        # We don't have any annual row in the data-frame
        self.assertTrue(
            result.empty,
            msg='Only annual data is valid on the "freq" column',
        )


if __name__ == "__main__":
    unittest.main()
