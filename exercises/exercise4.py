""" Exercise-4
Deadline: 
	17.01.2024 - 24.01.2024
"""
from urllib.request import urlretrieve
import pathlib
import os
import zipfile
import sqlalchemy as sql
import pandas as pd


class ZipHelper:
    """
    ZipHelper class to download and extract zip files.
    """

    def __init__(self, url: str, logging: bool = False):
        """
        Initialize the ZipHelper class.

        Parameters:
        - logging (bool): Whether to print the logs or not
        - url (str): url to download the zip file from
        """
        # The url to download the zip file from
        self.url = url
        self.logging = logging
        # Current working directory
        self.cwd = pathlib.Path(__file__).parent
        if self.logging:
            print(f"Current working directory: {self.cwd}")
        # Directory to extract the zip file to
        self.data_directory = f"{self.cwd.parent}/data"
        # Zip file name is the last part of the url
        zip_file_name = self.url.split("/")[-1]
        # The path to save the downloaded zip file into
        self.local_zip_filename = f"{self.data_directory}/{zip_file_name}"
        if self.logging:
            print(f"Local zip filename: {self.local_zip_filename}")

    def __download(self) -> str:
        """
        Download the zip file from the url and return the filename

        Returns:
            str: filename of the zip file
        """
        urlretrieve(url=self.url, filename=self.local_zip_filename)
        return self.local_zip_filename

    def extract(self) -> list:
        """
        Extract the zip file and return list of extracted files names

        Returns:
            str: filename of the extracted files(paths)
        """
        # Download the zip file
        self.__download()
        # Extract the zip file
        with zipfile.ZipFile(self.local_zip_filename, "r") as ref:
            ref.extractall(self.data_directory)
        # Extracted files
        extracted_files = ref.namelist()
        # Print the extracted files
        if self.logging:
            print("Extracted files:", end=" ")
            print(*extracted_files, sep=", ")
        return [os.path.join(self.data_directory, file) for file in extracted_files]


class Pipeline:
    """
    Pipeline class to extract, transform the data, and then load it into a database.
    """

    def __init__(self, logging: bool = False):
        """
        Initialize the pipeline class.

        Parameters:
        - logging (bool): Whether to print the logs or not
        """
        self.logging = logging

    def __extract(self, url: str, csv_file_name: str) -> None:
        """
        Load the data source by URL.

        Parameters:
        - url (str): URL of the Zip containing a CSV data source
        - csv_file_name (str): Name of the CSV file in the Zip
        """
        zip_helper = ZipHelper(logging=self.logging, url=url)
        # Download the zip files and extract it
        files = zip_helper.extract()
        # Find the CSV file
        csv_file_path_list = [file for file in files if csv_file_name in file]
        if len(csv_file_path_list) == 0:
            raise FileNotFoundError(
                f'CSV file "{csv_file_name}" not found in the zip file'
            )
        csv_file_path = csv_file_path_list[0]
        if self.logging:
            print(f"CSV file path: {csv_file_path}")
        # Only read some of the columns
        columns_to_read = [
            "Geraet",
            "Hersteller",
            "Model",
            "Monat",
            "Temperatur in °C (DWD)",
            "Batterietemperatur in °C",
            "Geraet aktiv",
        ]
        # Set types
        columns_types = {
            "Geraet": "Int64",
            "Hersteller": "string",
            "Model": "string",
            "Monat": "Int64",
            "Temperatur in °C (DWD)": "float",
            "Batterietemperatur in °C": "float",
            "Geraet aktiv": "string",
        }
        # Read the CSV file
        self.data_frame = pd.read_csv(
            csv_file_path,
            sep=";",
            decimal=",",
            index_col=False,
            usecols=columns_to_read,
            dtype=columns_types,
            on_bad_lines="skip",
            keep_default_na=True,
        )

        if self.logging:
            print(self.data_frame["Temperatur in °C (DWD)"])

    def __celsius_to_fahrenheit(self, celsius: float) -> float:
        """
        Convert Celsius to Fahrenheit.

        Parameters:
        - celsius (float): Temperature in Celsius

        Returns:
        - float: Temperature in Fahrenheit
        """
        return celsius * 1.8 + 32.0

    def __transform(self):
        """
        Transform and clean data sources in this project
        """
        if self.logging:
            print("Transforming the data source...")
        # 01- Rename columns
        new_cols = {
            "Temperatur in °C (DWD)": "Temperatur",
            "Batterietemperatur in °C": "Batterietemperatur",
        }
        self.data_frame = self.data_frame.rename(columns=new_cols)
        if self.logging:
            print("Renamed columns:", self.data_frame.columns)
        # 02- Transform temperatures in Celsius to Fahrenheit
        # Formula: (TemperatureInCelsius * 9/5) + 32
        # keep the same column names
        # 02|01- Temperatur
        self.data_frame["Temperatur"] = self.__celsius_to_fahrenheit(
            self.data_frame["Temperatur"]
        )
        # 02|02- Batterietemperatur
        self.data_frame["Batterietemperatur"] = self.__celsius_to_fahrenheit(
            self.data_frame["Batterietemperatur"]
        )
        if self.logging:
            print("\nTransformed data frame:\n", self.data_frame)

    def __validate_data(self):
        """
        Validate the data frame and remove invalid rows
        """
        if self.logging:
            print("Validating the data...")

        # 01- Drop rows with missing values
        self.data_frame.dropna(inplace=True)
        # 02- Drop rows if "Geraet" is NOT over 0
        self.data_frame = self.data_frame[self.data_frame["Geraet"] > 0]
        # 03- Drop rows if "Monat" is NOT between 1 and 12
        self.data_frame = self.data_frame[self.data_frame["Monat"].between(1, 12)]

    def __load(self):
        """
        Save the transformed data frame into one SQLITE file.
        """
        table_name = "temperatures"
        engine = sql.create_engine(f"sqlite:///{table_name}.sqlite")
        if self.logging:
            print("Saving merged data in a SQLITE DB...")
        # 01 - Assign data types
        self.data_types = {
            "Geraet": sql.Integer,
            "Hersteller": sql.Text,
            "Model": sql.Text,
            "Monat": sql.Integer,
            "Temperatur": sql.Float,
            "Batterietemperatur": sql.Float,
            "Geraet aktiv": sql.Text,
        }
        if self.logging:
            print("Saving transformed data in a SQLITE DB ...")
        self.data_frame.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",
            dtype=self.data_types,
            index=False,
        )
        if self.logging:
            print("Saving into database is done!")

    def run_pipeline(self, url: str) -> None:
        """
        Run the pipeline to extract, transform and load the data from the url.

        Parameters:
        - url (str): URL of the data source
        """
        try:
            self.__extract(url=url, csv_file_name="data.csv")
            self.__transform()
            self.__validate_data()
            self.__load()

        except FileNotFoundError as error:
            print(error)

        except Exception as error:
            print(error)


if __name__ == "__main__":
    ZIP_URL = "https://www.mowesta.com/data/measure/mowesta-dataset-20221107.zip"
    RETRY_THRESHOLD = 5
    ATTEMPTS = 1
    while ATTEMPTS < RETRY_THRESHOLD:
        try:
            Pipeline(logging=False).run_pipeline(url=ZIP_URL)
            break
        except Exception as e:
            ATTEMPTS += 1
            print(f"Something went wrong! {e}")
            print(f"Try #{ATTEMPTS} in progress...")
    if ATTEMPTS == 5:
        print(f"\nLOOK!! I tried to run the pipeline {RETRY_THRESHOLD} times!")
        print("It's your turn to check the code!")
