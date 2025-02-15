""" Exercise-2
Deadline: 
	22.11.2023 - 29.11.2023
"""
import pathlib
import pandas as pd
import sqlalchemy as sql


class Pipeline:
    def __extract(self, url: str, download_csv=False):
        """
        Load the data source by URL.

        Parameters:
        - url (str): URL of the CSV data source
        - download_csv (bool, optional): Flag indicating whether to save the downloaded file to "data/"
        directory or not.

        Returns:
        - DataFrame: A DataFrame containing the CSV data.
        """
        self.data_frame = pd.read_csv(url, sep=";", decimal=",")
        if download_csv:
            cwd = pathlib.Path(__file__).parent
            print(f"Current working directory: {cwd}")
            csv_file_name = url.lower().split("/")[-1]
            scv_file_path = f"{cwd.parent}/data/{csv_file_name}"
            self.data_frame.to_csv(scv_file_path, sep=";", decimal=",")
            print(f"CSV is saved into {scv_file_path}")
        return self.data_frame

    def __transform(self):
        """
        Transform and clean data sources in this project
        """
        print("Transforming the data source...")
        # 01- Drop [Status] column
        self.data_frame.drop(["Status"], axis=1, inplace=True)
        # 02- Drop rows with invalid values on [Verkehr] column
        # Valid values are ["FV", "RV", "nur DPN"]
        # Only the exact values even subset of it is not OK. For example RVV is invalid
        valid_traffic = self.data_frame["Verkehr"].isin(["FV", "RV", "nur DPN"])
        self.data_frame = self.data_frame[valid_traffic]
        # 03- Drop rows with invalid range on [Laenge], [Breite] columns
        valid_long_lat = self.data_frame["Laenge"].between(-90, 90) & self.data_frame[
            "Breite"
        ].between(-90, 90)
        self.data_frame = self.data_frame[valid_long_lat]
        # 04- Drop rows not having the following pattern on [IFOPT] column
        # Pattern: <exactly two characters>:<any amount of numbers>:<any amount of numbers><optionally another colon followed by any amount of numbers>
        regex_pattern = r"\w{2}:\d*:\d*(:\d*){0,1}"
        valid_traffic = self.data_frame["IFOPT"].str.match(regex_pattern, na=False)
        self.data_frame = self.data_frame[valid_traffic]
        # 05- Drop empty cells
        self.data_frame.dropna(inplace=True)
        print("Transforming the data source Finished!")

    def __load(self):
        """
        Save the transformed data frame into one SQLITE file.
        """
        engine = sql.create_engine(f"sqlite:///trainstops.sqlite")
        print("Saving merged data in a SQLITE DB...")
        table_name = "trainstops"
        # 06 - Assign data types
        self.data_types = {
            "EVA_NR": sql.Integer,
            "DS100": sql.Text,
            "IFOPT": sql.Text,
            "NAME": sql.Text,
            "Verkehr": sql.Text,
            "Laenge": sql.Float,
            "Breite": sql.Float,
            "Betreiber_Name": sql.Text,
            "Betreiber_Nr": sql.Integer,
        }
        self.data_frame = self.data_frame.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",
            dtype=self.data_types,
            index=False,
        )
        print("Saving transformed data in a SQLITE DB Finished!")

    def run_pipeline(self, url: str):
        """
        Run the pipeline for this project

        Parameters:
        - url (str): URL of the CSV data source
        """
        self.__extract(url=url)
        self.__transform()
        self.__load()


if __name__ == "__main__":
    URL = "https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV"
    RETRY_THRESHOLD = 5
    ATTEMPTS = 1
    while ATTEMPTS < RETRY_THRESHOLD:
        try:
            Pipeline().run_pipeline(url=URL)
            break
        except Exception as e:
            ATTEMPTS += 1
            print(f"Something went wrong! {e}")
            print(f"Try #{ATTEMPTS} in progress...")
    if ATTEMPTS == 5:
        print(f"\nLOOK!! I tried to run the pipeline {RETRY_THRESHOLD} times!")
        print("It's your turn to check the code!")
