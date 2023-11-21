import etl.extract.sdg_extractor as sdg_e
import etl.extract.geo_extractor as geo_e
import etl.extract.tran_r_vehst_extractor as tran_e
import etl.extract.road_eqr_carpda_extractor as road_e
import etl.transform.road_eqr_carpda_transformer as road_t
import etl.transform.tran_r_vehst_transformer as tran_t
import etl.transform.sdg_transformer as sdg_t
import etl.load.loader as loader
import logging


class pipeline:
    def __extract(self):
        """
        Extract data sources in this project
        """
        print("Extracting SDG data source...")
        self.sdg = sdg_e.sdg_data_extractor()
        print("Extracting SDG data source Finished!")

        print("Extracting GEO data source...")
        self.geo = geo_e.geo_data_extractor()
        print("Extracting GEO data source Finished!")

        print("Extracting Tran_r_vhest data source...")
        self.tran = tran_e.tran_r_vehst_data_extractor()
        print("Extracting Tran_r_vhest data source Finished!")

        print("Extracting Road_eqr_catpda data source...")
        self.road = road_e.road_eqr_carpda_data_extractor()
        print("Extracting Road_eqr_catpda data source Finished!")

    def __transform(self):
        """
        Transform and clean data sources in this project
        """
        print("Transforming Road_eqr_catpda data source...")
        self.cleaned_road = road_t.road_eqr_carpda_data_transformer(self.road)
        print("Transforming Road_eqr_catpda data source Finished!")

        print("Transforming tran_r_vehst data source...")
        self.cleaned_tran = tran_t.tran_r_vehst_data_transformer(self.tran)
        print("Transforming tran_r_vehst data source Finished!")

        print("Transforming SDG data source...")
        self.cleaned_sdg = sdg_t.sdg_data_transformer(self.sdg)
        print("Transforming SDG data source Finished!")

    def __merge(self):
        """
        Merge data sources in this project into one data frame
        """

        print("Merging data sources...")
        self.merged_data = loader.mergeDataToSQL(
            sdg_data=self.cleaned_sdg,
            road_data=self.cleaned_road,
            tran_data=self.cleaned_tran,
        )
        print("Merging data sources Finished!")

    def __load(self):
        """
        Save the merged data frame into one SQLITE file.
        """

        print("Saving merged data in a SQLITE DB...")
        loader.loadDataToSQL(
            data_frame=self.merged_data,
            db_name="pipeline",
            table_name="co2_cars",
        )
        print("Saving merged data in a SQLITE DB Finished!")

    # TODO:: Need better error handling, more specific one with a retry approach
    def run_pipeline(self):
        """
        Run the pipeline for this project
        """
        # Extract
        try:
            self.__extract()
        except Exception as e:
            logging.error(f"Error: {e}")
            print("Something went wrong...")
            return

        # Transform
        # TODO:: rafoolin/made-template#14
        try:
            self.__transform()
        except Exception as e:
            logging.error(f"Error: {e}")
            print("Something went wrong...")
            return

        # Merge
        try:
            self.__merge()
        except Exception as e:
            logging.error(f"Error: {e}")
            print("Something went wrong...")

            return

        # Load
        try:
            self.__load()
        except Exception as e:
            logging.error(f"Error: {e}")
            print("Something went wrong...")

            return


if __name__ == "__main__":
    pipeline().run_pipeline()
