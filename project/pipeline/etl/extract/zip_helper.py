import requests
import logging
import gzip
import os
import shutil


class GZipFileHelper:
    """
    A helper class for downloading and extracting GZip files from a given URL.
    """

    def __init__(self) -> None:
        logging.info("[GZipHelper] started...")

    def __extension_format(self, url):
        """
        Extracts the file format from the given URL query parameters.

        Args:
            url (str): The URL to extract file format from.
        """
        from pipeline_utils.constants.constants import FileFormat

        # Separate the query section of the URL
        query_parameters = url.split("/")[-1].split("&")
        file_format = None
        for param in query_parameters:
            if "format" in param:
                file_format = param.replace("format=", "").lower().strip("?")

        return FileFormat(value=file_format).toExtension()

    def __is_file_compressed(self, url):
        """
        Check whether the requested file from the URL is of type compressed or not.

        Args:
            url (str): The URL to check for compression.

        Returns:
            bool: True if the file is of type compressed, False otherwise.
        """

        query_parameters = url.split("/")[-1].split("&")
        for param in query_parameters:
            if "compressed" in param:
                return True if param.replace("compressed=", "") == "true" else False

        return None

    def download_and_extract_gz(self, url):
        """
        Downloads and extracts a GZip file from the given URL.
        """

        from pipeline_utils import utils
        logging.info("\t [download_and_extract_gz] started...")
        cwd = utils.get_directory_absolute_path()
        logging.info(f"CWD: {cwd}")
        # Separate the query part of the URL
        file_name = url.split("/")[-2].lower()
        file_format = self.__extension_format(url=url)
        is_compressed = self.__is_file_compressed(url=url)

        if is_compressed:
            logging.info("The url downloads a gz file!")
            logging.info(f"file name: {file_name}\n Format: {file_format}")
            output_gzip = f"{cwd}/data/{file_name}.gz"
            # The absolute path to save the GZ file to
            output_data_file = f"{cwd}/data/{file_name}.{file_format}"
            # Download the GZ file and save it to [output_data_file]
            response = requests.get(url, stream=True)
            with open(output_gzip, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            # Extract and save the data source in [data] folder
            with gzip.open(output_gzip, "rb") as f_in:
                with open(output_data_file, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(output_gzip)
        logging.info("\t [download_and_extract_gz] finished!")
