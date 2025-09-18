# from typing import List, Literal
# from src.config.blok_freights import BLOK_FREIGHT_SHEET_ID_MAPPER
# from src.services.freight.af_format import format_af
# from src.services.freight.cn_format import format_cn
# from src.services.freight.eu_format import format_eu
# from src.services.freight.fe_format import format_fe
# from src.services.freight.me_format import format_me
# from src.services.freight.oc_format import format_oc
# from src.services.freight.us_format import format_us
# from src.database.line_rates import delete_test_lines, upsert_test_lines
# from src.config.logger import logger
# from src.services.freight.locals_charges_adder import (
#     ind_export_locals_charges_adder_by_path,
# )
# from src.pipeline.freight_excel_export_pipeline import freight_excel_export_pipeline


# # NOTE: Sheet_id 0 -> US_CAD and Sheet_id 1 -> EU
# def freight_pipeline(do_all: bool = True, sheet_id: Literal[0, 1, 2, 3, 4, 5, 6] = None):

#     sheet_id_list: List[Literal[0, 1, 2, 3, 4, 5, 6]] = [0, 1, 2, 3, 4, 5, 6] if do_all else [sheet_id]

#     # fetch all gsheets to excel
#     freight_excel_export_pipeline()
#     # delete all test liens
#     delete_test_lines()
#     for id in sheet_id_list:
       
#         try:
#             sheet = BLOK_FREIGHT_SHEET_ID_MAPPER[id]
#             path = sheet["path"]
#             code = sheet["code"]
#             norm_path = sheet["norm_path"]
#             denorm_path = sheet["denorm_path"]
#             hapag_path = sheet["hapag_path"]
#             print(f"Sheet ID: {id}")
#             print(f"  Path         : {path}")
#             print(f"  Code         : {code}")
#             print(f"  Norm Path    : {norm_path}")
#             print(f"  Denorm Path  : {denorm_path}")
#             print(f"  Hapag Path   : {hapag_path}")
#             print("-" * 40)
#             # FORMAT
#             if code == "US_CAD":
#                 format_us(
#                     path=path,
#                     normalize_save_path=norm_path,
#                     denormaliz_save_path=denorm_path,
#                 )
#             elif code == "EU":
#                 format_eu(
#                     path=path,
#                     normalize_save_path=norm_path,
#                     denormaliz_save_path=denorm_path,
#                 )
#             elif code == "OC":
#                 format_oc(
#                     path=path,
#                     normalize_save_path=norm_path,
#                     denormaliz_save_path=denorm_path,
#                 )
#             elif code == "ME":
#                 format_me(
#                     path=path,
#                     normalize_save_path=norm_path,
#                     denormaliz_save_path=denorm_path,
#                 )
#             elif code == "FE":
#                 format_fe(
#                     path=path,
#                     normalize_save_path=norm_path,
#                     denormaliz_save_path=denorm_path,
#                 )
#             elif code == "CN":
#                 format_cn(
#                     path=path,
#                     normalize_save_path=norm_path,
#                     denormaliz_save_path=denorm_path,
#                 )
#             elif code == "AF":
#                 format_af(
#                     path=path,
#                     normalize_save_path=norm_path,
#                     denormaliz_save_path=denorm_path,
#                 )

#             lines_record = ind_export_locals_charges_adder_by_path(
#                 normalize_path=norm_path
#             )

#             print("lines_record:", len(lines_record))
#             # upsert into test db
#             upsert_test_lines(lines_record)

#         except Exception as e:
#             logger.info(f"Error occur in services:blok_freights:{e}")
