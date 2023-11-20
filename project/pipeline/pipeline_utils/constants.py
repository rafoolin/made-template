from enum import Enum


class FileFormat(Enum):
    """
    FileFormat - An enumeration representing different file formats.

    Values:

    SDMXCSV: Represents the CSV file format.
    
    TSV: Represents the TSV file format.
    """

    SDMXCSV = "sdmx-csv"
    TSV = "tsv"

    def toExtension(self):
        """
        Converts the enum value to its corresponding file extension.

        Returns:
            str: The file extension associated with the enum value.
        """

        if self == FileFormat.SDMXCSV:
            return "csv"
        if self == FileFormat.TSV:
            return "tsv"
