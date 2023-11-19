
import  etl.extract.sdg_extractor as sdg
import  etl.extract.geo_extractor as geo
import  etl.extract.tran_r_vehst_extractor as tran
import  etl.extract.road_eqr_carpda_extractor as road

# TODO:: Cover try-catch and print/log
sdg_data_frame = sdg.sdg_data_extractor()
geo_data_frame = geo.geo_data_extractor()
tran_data_frame = tran.tran_r_vehst_data_extractor()
road_data_frame = road.road_eqr_carpda_data_extractor()

