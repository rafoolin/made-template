import logging
from termcolor import colored

import etl.extract.sdg_extractor as sdg_e
import etl.extract.geo_extractor as geo_e
import etl.extract.unit_extractor as unit_e
import etl.extract.tran_r_vehst_extractor as tran_e
import etl.extract.road_eqr_carpda_extractor as road_e
import etl.transform.road_eqr_carpda_transformer as road_t
import etl.transform.tran_r_vehst_transformer as tran_t
import etl.transform.sdg_transformer as sdg_t
import etl.load.loader as loader


class Pipeline:
    def __extract(self):
        """
        Extract data sources in this project
        """
        print(colored("Extracting SDG data source...", "green"))
        self.sdg = sdg_e.sdg_data_extractor()
        print(colored("Extracting SDG data source Finished!", "green"))

        print(colored("Extracting GEO data source...", "green"))
        self.geo = geo_e.geo_data_extractor()
        print(colored("Extracting GEO data source Finished!", "green"))

        print(colored("Extracting unit data source...", "green"))
        self.unit = unit_e.unit_data_extractor()
        print(colored("Extracting unit data source Finished!", "green"))

        print(colored("Extracting Tran_r_vhest data source...", "green"))
        self.tran = tran_e.tran_r_vehst_data_extractor()
        print(colored("Extracting Tran_r_vhest data source Finished!", "green"))

        print(colored("Extracting Road_eqr_catpda data source...", "green"))
        self.road = road_e.road_eqr_carpda_data_extractor()
        print(colored("Extracting Road_eqr_catpda data source Finished!", "green"))

    def __transform(self):
        """
        Transform and clean data sources in this project
        """
        print(colored("Transforming Road_eqr_catpda data source...", "green"))
        self.cleaned_road = road_t.road_eqr_carpda_data_transformer(self.road)
        print(colored("Transforming Road_eqr_catpda data source Finished!", "green"))

        print(colored("Transforming tran_r_vehst data source...", "green"))
        self.cleaned_tran = tran_t.tran_r_vehst_data_transformer(self.tran)
        print(colored("Transforming tran_r_vehst data source Finished!", "green"))

        print(colored("Transforming SDG data source...", "green"))
        self.cleaned_sdg = sdg_t.sdg_data_transformer(self.sdg)
        print(colored("Transforming SDG data source Finished!", "green"))

    def __merge(self):
        """
        Merge data sources in this project into one data frame
        """

        print(colored("Merging data sources...", "green"))
        self.merged_data = loader.merge_data_to_sql(
            sdg_data=self.cleaned_sdg,
            road_data=self.cleaned_road,
            tran_data=self.cleaned_tran,
        )
        # Convert column names to lowercase
        self.merged_data.columns = self.merged_data.columns.str.lower()
        print(colored("Merging data sources Finished!", "green"))

    def __load(self):
        """
        Save the merged data frame into one SQLITE file.
        """

        print(colored("Saving merged data in a SQLITE DB...", "green"))
        loader.load_data_to_sql(
            data_frame=self.merged_data,
            db_name="pipeline",
            table_name="co2_cars",
        )
        print(colored("Saving merged data in a SQLITE DB Finished!", "green"))

    # TODO:: Need better error handling, more specific one with a retry approach
    def run_pipeline(self):
        """
        Run the pipeline for this project and generates data a clean source
        """
        # Extract
        try:
            self.__extract()
        except Exception as e:
            logging.error(f"Error: {e}")
            print(
                colored(
                    "Something went wrong while extracting the data-sources...",
                    "red",
                )
            )
            return

        # Transform
        # TODO:: rafoolin/made-template#14
        try:
            self.__transform()
        except Exception as e:
            logging.error(f"Error: {e}")
            print(
                colored(
                    "Something went wrong while transforming the data-sources...",
                    "red",
                )
            )
            return

        # Merge
        try:
            self.__merge()
        except Exception as e:
            logging.error(f"Error: {e}")
            print(
                colored(
                    "Something went wrong while merging the data-sources...",
                    "red",
                )
            )

            return

        # Load
        try:
            self.__load()
        except Exception as e:
            logging.error(f"Error: {e}")
            print(
                colored(
                    "Something went wrong while loading the merged data-source...",
                    "red",
                )
            )

            return


if __name__ == "__main__":
    Pipeline().run_pipeline()
