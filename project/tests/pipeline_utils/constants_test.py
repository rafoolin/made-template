
import unittest

from pipeline_utils.constants import FileFormat


class TestFileFormat(unittest.TestCase):
    def test_toExtension_sdmxcsv(self):
        file_format = FileFormat.SDMXCSV
        extension = file_format.to_extension()
        self.assertEqual(extension, "csv")

    def test_toExtension_tsv(self):
        file_format = FileFormat.TSV
        extension = file_format.to_extension()
        self.assertEqual(extension, "tsv")
        
    # TODO:: Cover this in the enum
    def test_toExtension_invalid_format(self):
        pass

if __name__ == "__main__":
    unittest.main()
