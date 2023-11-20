import etl.extract.sdg_extractor as sdg_e
import etl.extract.geo_extractor as geo_e
import etl.extract.tran_r_vehst_extractor as tran_e
import etl.extract.road_eqr_carpda_extractor as road_e
import etl.transform.road_eqr_carpda_transformer as road_t
import etl.transform.tran_r_vehst_transformer as tran_t
import etl.transform.sdg_transformer as sdg_t
import etl.load.loader as loader


class pipeline:
    def __extract(self):
        # TODO:: Cover try-catch and print/log
        self.sdg = sdg_e.sdg_data_extractor()
        self.geo = geo_e.geo_data_extractor()
        self.tran = tran_e.tran_r_vehst_data_extractor()
        self.road = road_e.road_eqr_carpda_data_extractor()

    def __transform(self):
        self.cleaned_road = road_t.road_eqr_carpda_data_transformer(self.road)
        self.cleaned_tran = tran_t.tran_r_vehst_data_transformer(self.tran)
        self.cleaned_sdg = sdg_t.sdg_data_transformer(self.sdg)

    def __merge(self):
        self.merged_data = loader.mergeDataToSQL(
            sdg_data=self.cleaned_sdg,
            road_data=self.cleaned_road,
            tran_data=self.cleaned_tran,
        )

    def __load(self):
        loader.loadDataToSQL(
            data_frame=self.merged_data,
            db_name="pipeline",
            table_name="co2_cars",
        )

    def run_pipeline(self):
        # Extract
        self.__extract()
        # Transform
        self.__transform()
        # Merge
        self.__merge()
        # Load
        self.__load()


if __name__ == "__main__":
    pipeline().run_pipeline()
